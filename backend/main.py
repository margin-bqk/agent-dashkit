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
            span INTEGER DEFAULT 1,
            position INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add span column if not exists (for existing databases)
    try:
        conn.execute("ALTER TABLE components ADD COLUMN span INTEGER DEFAULT 1")
    except:
        pass  # Column already exists
    
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
    type: str  # progress, task_list, text, chart, table, timer, markdown, iframe, calendar
    title: str
    data: Dict[str, Any]
    span: Optional[int] = 1  # 1, 2, or 3 columns
    position: Optional[int] = 0

class ComponentUpdate(BaseModel):
    title: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    span: Optional[int] = None
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
        INSERT INTO components (id, type, title, data, span, position)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (component_id, component.type, component.title, str(component.data), component.span, component.position))
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

@app.get("/api/templates")
async def get_templates():
    """
    Get predefined component templates for AI agents.
    These templates provide sample data structures for common use cases.
    """
    return {
        "templates": [
            {
                "id": "progress-default",
                "type": "progress",
                "title": "Project Progress",
                "description": "Track project completion percentage",
                "data": {"value": 0, "status": "Not Started"},
                "span": 1
            },
            {
                "id": "task-list-default",
                "type": "task_list",
                "title": "Task List",
                "description": "Track multiple tasks with completion status",
                "data": {"tasks": [
                    {"name": "Task 1", "completed": False},
                    {"name": "Task 2", "completed": False},
                    {"name": "Task 3", "completed": False}
                ]},
                "span": 1
            },
            {
                "id": "text-announcement",
                "type": "text",
                "title": "Announcement",
                "description": "Display important announcements or notes",
                "data": {"content": "Your announcement text here", "source": "Source name"},
                "span": 1
            },
            {
                "id": "chart-line-default",
                "type": "chart",
                "title": "Line Chart",
                "description": "Display data as a line chart",
                "data": {
                    "chartType": "line",
                    "data": {
                        "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                        "datasets": [{"label": "Data", "data": [12, 19, 3, 5, 2], "borderColor": "#3b82f6", "backgroundColor": "rgba(59, 130, 246, 0.1)"}]
                    }
                },
                "span": 2
            },
            {
                "id": "chart-bar-default",
                "type": "chart",
                "title": "Bar Chart",
                "description": "Display data as a bar chart",
                "data": {
                    "chartType": "bar",
                    "data": {
                        "labels": ["A", "B", "C", "D"],
                        "datasets": [{"label": "Values", "data": [10, 25, 15, 30], "backgroundColor": ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b"]}]
                    }
                },
                "span": 2
            },
            {
                "id": "chart-pie-default",
                "type": "chart",
                "title": "Pie Chart",
                "description": "Display data as a pie chart",
                "data": {
                    "chartType": "pie",
                    "data": {
                        "labels": ["Category A", "Category B", "Category C"],
                        "datasets": [{"data": [30, 50, 20], "backgroundColor": ["#3b82f6", "#8b5cf6", "#10b981"]}]
                    }
                },
                "span": 1
            },
            {
                "id": "table-simple",
                "type": "table",
                "title": "Data Table",
                "description": "Display tabular data",
                "data": {
                    "headers": ["Column 1", "Column 2", "Column 3"],
                    "rows": [["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"], ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]]
                },
                "span": 2
            },
            {
                "id": "timer-counter",
                "type": "timer",
                "title": "Counter",
                "description": "Display a count-up number",
                "data": {"value": 0, "label": "Count"},
                "span": 1
            },
            {
                "id": "timer-days",
                "type": "timer",
                "title": "Days Counter",
                "description": "Count days since a start date",
                "data": {"value": 0, "label": "Days"},
                "span": 1
            },
            {
                "id": "markdown-readme",
                "type": "markdown",
                "title": "README",
                "description": "Render markdown content",
                "data": {
                    "content": "# Welcome\n\nThis is **bold** and *italic* text.\n\n- List item 1\n- List item 2\n\n```python\nprint('Hello world')\n```"
                },
                "span": 2
            },
            {
                "id": "iframe-website",
                "type": "iframe",
                "title": "External Website",
                "description": "Embed an external website",
                "data": {"url": "https://example.com"},
                "span": 2
            },
            {
                "id": "calendar-month",
                "type": "calendar",
                "title": "Calendar",
                "description": "Display a monthly calendar",
                "data": {
                    "month": "March 2026",
                    "days": list(range(1, 32)),
                    "highlighted": [1, 15]
                },
                "span": 2
            }
        ]
    }

# Frontend
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    with open("../frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
