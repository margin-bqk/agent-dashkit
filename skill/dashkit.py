import os
import requests
from typing import Dict, Any, Optional

DASHKIT_API_URL = os.getenv("DASHKIT_API_URL", "http://localhost:8000")
DASHKIT_API_KEY = os.getenv("DASHKIT_API_KEY", "")

def _get_headers() -> Dict[str, str]:
    return {
        "X-API-Key": DASHKIT_API_KEY,
        "Content-Type": "application/json"
    }

def dashkit_add_component(
    component_type: str,
    title: str,
    data: Dict[str, Any],
    position: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Add a new component to the dashboard.
    
    Args:
        component_type: Type of component (progress, task_list, text, chart, table)
        title: Component title
        data: Component data (structure depends on component type)
        position: Position order on the dashboard (lower numbers appear first)
    
    Returns:
        Response dict with success status and component_id
    """
    if not DASHKIT_API_KEY:
        return {"success": False, "error": "DASHKIT_API_KEY not set"}
    
    payload = {
        "type": component_type,
        "title": title,
        "data": data,
        "position": position
    }
    
    try:
        response = requests.post(
            f"{DASHKIT_API_URL}/api/components",
            headers=_get_headers(),
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def dashkit_update_component(
    component_id: str,
    title: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    position: Optional[int] = None
) -> Dict[str, Any]:
    """
    Update an existing component on the dashboard.
    
    Args:
        component_id: ID of the component to update
        title: New title (optional)
        data: New data (optional, structure depends on component type)
        position: New position (optional)
    
    Returns:
        Response dict with success status
    """
    if not DASHKIT_API_KEY:
        return {"success": False, "error": "DASHKIT_API_KEY not set"}
    
    payload = {}
    if title is not None:
        payload["title"] = title
    if data is not None:
        payload["data"] = data
    if position is not None:
        payload["position"] = position
    
    if not payload:
        return {"success": False, "error": "No update data provided"}
    
    try:
        response = requests.put(
            f"{DASHKIT_API_URL}/api/components/{component_id}",
            headers=_get_headers(),
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def dashkit_delete_component(component_id: str) -> Dict[str, Any]:
    """
    Delete a component from the dashboard.
    
    Args:
        component_id: ID of the component to delete
    
    Returns:
        Response dict with success status
    """
    if not DASHKIT_API_KEY:
        return {"success": False, "error": "DASHKIT_API_KEY not set"}
    
    try:
        response = requests.delete(
            f"{DASHKIT_API_URL}/api/components/{component_id}",
            headers=_get_headers(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}
