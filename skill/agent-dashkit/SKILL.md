---
name: Agent DashKit
slug: agent-dashkit
version: 0.1.0
description: Manage personal dashboard components, support progress bars, checklists, charts and other visualizations
changelog: Initial release, support component CRUD, 5 basic component types
metadata: {"emoji": "📊", "requires": {"python": ["requests"]}}
---

## When to Use
- When you need to visually display task progress, data statistics, and analysis results to users
- When you need to real-time update running status, to-do items, industry news and other information
- When you need to centrally display scattered task outputs on a unified panel

## Core Rules
1. Prioritize reusing and updating existing components, avoid frequent creation and deletion of the same type
2. Position numbers start from 1, sorted by importance from top to bottom, left to right
3. Text component content should not exceed 500 characters, truncate and provide detail link if longer
4. API key is read from environment variable `DASHKIT_API_KEY`, hardcoding in scripts is prohibited
5. Send Telegram notification to users after important data updates
6. Maximum 3 components of the same type can be displayed simultaneously, old components should be cleaned or reused

## Quick Reference
| Content | Corresponding File |
|---------|--------------------|
| Detailed API Documentation | `docs/api-reference.md` |
| Component Data Schemas | `docs/component-schemas.md` |
| Deployment & Configuration Guide | `docs/deployment-guide.md` |

## Usage
```python
# Add a progress bar component
dashkit_add_component(
    type="progress",
    title="Industry News Collection Progress",
    data={"value": 80, "max": 100},
    position=1
)

# Update existing component
dashkit_update_component(
    component_id="abc123",
    data={"value": 100}
)

# Get all components
components = dashkit_get_components()

# Delete component
dashkit_delete_component(component_id="abc123")
```