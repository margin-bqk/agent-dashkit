from fastapi import FastAPI, HTTPException, Depends, status, Request, Form
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import sqlite3
import uuid
import os
import json
from pathlib import Path
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use default values

app = FastAPI(title="Agent DashKit API", version="1.0.0")
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configuration from environment variables
API_KEY = os.getenv("DASHKIT_API_KEY", str(uuid.uuid4()))
DASHKIT_PASSWORD = os.getenv("DASHKIT_PASSWORD", "")
PORT = int(os.getenv("DASHKIT_PORT", "8000"))
DB_PATH = os.getenv("DASHKIT_DB_PATH", "dashkit.db")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

print(f"Agent DashKit v0.2.0")
print(f"API Key: {API_KEY}")
print(f"Password Protection: {'Enabled' if DASHKIT_PASSWORD else 'Disabled'}")
print(f"Server Port: {PORT}")
print("=" * 50)

# Database setup
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database
with sqlite3.connect(DB_PATH) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS components (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            data TEXT NOT NULL,
            position INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Create password_sessions table for web auth
    conn.execute("""
        CREATE TABLE IF NOT EXISTS password_sessions (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP DEFAULT (datetime('now', '+1 day'))
        )
    """)
    conn.commit()

# Models
class ComponentCreate(BaseModel):
    type: str  # progress, task_list, text, chart, table
    title: str
    data: Dict[str, Any]
    position: Optional[int] = 0

class ComponentUpdate(BaseModel):
    title: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    position: Optional[int] = None

# Dependencies
async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key

# Password session dependency for frontend
async def get_password_session(request: Request, db = Depends(get_db)):
    # If no password is set, allow access
    if not DASHKIT_PASSWORD:
        return True
    
    # Check for session cookie
    session_id = request.cookies.get("dashkit_session")
    if session_id:
        session = db.execute(
            "SELECT * FROM password_sessions WHERE session_id = ? AND expires_at > datetime('now')",
            (session_id,)
        ).fetchone()
        if session:
            return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Password required",
        headers={"WWW-Authenticate": "Basic"}
    )

# API Routes
@app.post("/api/auth/login")
async def login(password: str = Form(...), db = Depends(get_db)):
    """Authenticate dashboard password and create session"""
    if not DASHKIT_PASSWORD:
        return {"success": True, "message": "No password configured"}
    
    if password != DASHKIT_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    session_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO password_sessions (session_id) VALUES (?)",
        (session_id,)
    )
    db.commit()
    
    response = JSONResponse({"success": True, "message": "Authenticated"})
    response.set_cookie(
        key="dashkit_session",
        value=session_id,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax"
    )
    return response

@app.post("/api/auth/logout")
async def logout(request: Request, db = Depends(get_db)):
    """Logout and delete session"""
    session_id = request.cookies.get("dashkit_session")
    if session_id:
        db.execute("DELETE FROM password_sessions WHERE session_id = ?", (session_id,))
        db.commit()
    
    response = JSONResponse({"success": True, "message": "Logged out"})
    response.delete_cookie("dashkit_session")
    return response

@app.get("/api/auth/status")
async def auth_status(request: Request, db = Depends(get_db)):
    """Check if user is authenticated"""
    if not DASHKIT_PASSWORD:
        return {"authenticated": True, "password_protected": False}
    
    session_id = request.cookies.get("dashkit_session")
    if session_id:
        session = db.execute(
            "SELECT * FROM password_sessions WHERE session_id = ? AND expires_at > datetime('now')",
            (session_id,)
        ).fetchone()
        if session:
            return {"authenticated": True, "password_protected": True}
    
    return {"authenticated": False, "password_protected": True}

# API Routes
@app.post("/api/components", dependencies=[Depends(get_api_key)])
async def create_component(component: ComponentCreate, db = Depends(get_db)):
    component_id = str(uuid.uuid4())
    db.execute("""
        INSERT INTO components (id, type, title, data, position)
        VALUES (?, ?, ?, ?, ?)
    """, (component_id, component.type, component.title, str(component.data), component.position))
    db.commit()
    
    return {"success": True, "component_id": component_id}

@app.put("/api/components/{component_id}", dependencies=[Depends(get_api_key)])
async def update_component(component_id: str, update: ComponentUpdate, db = Depends(get_db)):
    component = db.execute("SELECT * FROM components WHERE id = ?", (component_id,)).fetchone()
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    update_data = update.dict(exclude_unset=True)
    if "data" in update_data:
        update_data["data"] = str(update_data["data"])
    
    set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
    values = list(update_data.values()) + [component_id]
    
    db.execute(f"UPDATE components SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values)
    db.commit()
    
    return {"success": True}

@app.delete("/api/components/{component_id}", dependencies=[Depends(get_api_key)])
async def delete_component(component_id: str, db = Depends(get_db)):
    db.execute("DELETE FROM components WHERE id = ?", (component_id,))
    db.commit()
    return {"success": True}

@app.get("/api/components")
async def get_components(db = Depends(get_db)):
    """Get all components on the dashboard"""
    components = db.execute("SELECT * FROM components ORDER BY position, created_at").fetchall()
    result = []
    for comp in components:
        comp_dict = dict(comp)
        comp_dict["data"] = eval(comp_dict["data"])  # Safe since we control the input
        result.append(comp_dict)
    return result

@app.get("/api/export")
async def export_components(db = Depends(get_db)):
    """Export all components as JSON backup"""
    components = db.execute("SELECT * FROM components ORDER BY position, created_at").fetchall()
    result = {
        "version": "0.2.0",
        "exported_at": "",
        "components": []
    }
    
    for comp in components:
        comp_dict = dict(comp)
        comp_dict["data"] = eval(comp_dict["data"])
        result["components"].append(comp_dict)
    
    # Add timestamp
    result["exported_at"] = datetime.now().isoformat()
    
    return result

# Frontend
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    with open("../frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
