#!/usr/bin/env python3
"""
Agent DashKit Skill
Interact with Agent DashKit dashboard API to manage components
"""

import os
import requests
from typing import Dict, List, Optional, Any

# Configuration
BASE_URL = os.getenv("DASHKIT_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("DASHKIT_API_KEY", "")

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def dashkit_add_component(
    type: str,
    title: str,
    data: Dict[str, Any],
    position: int,
    span: int = 1
) -> Optional[str]:
    """
    Add a new component to the dashboard
    
    Args:
        type: Component type (progress, checklist, text, chart, table, timer, markdown)
        title: Component title
        data: Component data matching the type schema
        position: Display position (starts from 1)
        span: Width span (1-3, default: 1)
    
    Returns:
        Component ID if successful, None otherwise
    """
    if not API_KEY:
        print("Error: DASHKIT_API_KEY environment variable not set")
        return None
    
    payload = {
        "type": type,
        "title": title,
        "data": data,
        "position": position,
        "span": span
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/components",
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("id")
    except Exception as e:
        print(f"Error adding component: {str(e)}")
        return None

def dashkit_update_component(
    component_id: str,
    title: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    position: Optional[int] = None,
    span: Optional[int] = None
) -> bool:
    """
    Update an existing component
    
    Args:
        component_id: ID of the component to update
        title: Optional new title
        data: Optional new data
        position: Optional new position
        span: Optional new width span
    
    Returns:
        True if successful, False otherwise
    """
    if not API_KEY:
        print("Error: DASHKIT_API_KEY environment variable not set")
        return False
    
    payload = {}
    if title is not None:
        payload["title"] = title
    if data is not None:
        payload["data"] = data
    if position is not None:
        payload["position"] = position
    if span is not None:
        payload["span"] = span
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/components/{component_id}",
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error updating component: {str(e)}")
        return False

def dashkit_get_components() -> Optional[List[Dict[str, Any]]]:
    """
    Get all components from the dashboard
    
    Returns:
        List of components if successful, None otherwise
    """
    if not API_KEY:
        print("Error: DASHKIT_API_KEY environment variable not set")
        return None
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/components",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("components", [])
    except Exception as e:
        print(f"Error getting components: {str(e)}")
        return None

def dashkit_delete_component(component_id: str) -> bool:
    """
    Delete a component from the dashboard
    
    Args:
        component_id: ID of the component to delete
    
    Returns:
        True if successful, False otherwise
    """
    if not API_KEY:
        print("Error: DASHKIT_API_KEY environment variable not set")
        return False
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/components/{component_id}",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error deleting component: {str(e)}")
        return False

def dashkit_export_backup() -> Optional[Dict[str, Any]]:
    """
    Export all components as a backup
    
    Returns:
        Backup data if successful, None otherwise
    """
    if not API_KEY:
        print("Error: DASHKIT_API_KEY environment variable not set")
        return None
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/export",
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error exporting backup: {str(e)}")
        return None

# Export functions for skill use
__all__ = [
    "dashkit_add_component",
    "dashkit_update_component",
    "dashkit_get_components",
    "dashkit_delete_component",
    "dashkit_export_backup"
]
