from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sqlite3
import uuid
import os

app = FastAPI(title="Agent DashKit API", version="1.0.0")

# API Key Authentication
API_KEY = os.getenv("DASHKIT_API_KEY", str(uuid.uuid4()))
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

print(f"Your DashKit API Key: {API_KEY}")
print("Keep this key secure and use it for all API requests")

# Database setup
def get_db():
    conn = sqlite3.connect("dashkit.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database
with sqlite3.connect("dashkit.db") as conn:
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
    components = db.execute("SELECT * FROM components ORDER BY position, created_at").fetchall()
    result = []
    for comp in components:
        comp_dict = dict(comp)
        comp_dict["data"] = eval(comp_dict["data"])  # Safe since we control the input
        result.append(comp_dict)
    return result

# Frontend
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    with open("../frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
