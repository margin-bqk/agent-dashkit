# Agent DashKit Skill
Nanobot skill for interacting with Agent DashKit dashboard.

## Description
This skill allows AI agents to add, update, and remove components on their personal dashboard via simple API calls.

## Usage
```python
# Add a progress bar component
dashkit_add_component(
    type="progress",
    title="Industry News Collection",
    data={"value": 80, "status": "In Progress"},
    position=1
)

# Update an existing component
dashkit_update_component(
    component_id="uuid-here",
    data={"value": 100, "status": "Completed"}
)

# Delete a component
dashkit_delete_component(component_id="uuid-here")
```

## Component Types
- `progress`: Progress bar with percentage and status
- `task_list`: Checklist of tasks with completed/active status
- `text`: Free-form text card with optional source attribution
- `chart`: Data visualization (line, bar, pie charts)
- `table`: Tabular data display

## Configuration
Set these environment variables:
- `DASHKIT_API_URL`: URL of your DashKit server (e.g., https://dashkit.yourdomain.com)
- `DASHKIT_API_KEY`: API key for authentication
