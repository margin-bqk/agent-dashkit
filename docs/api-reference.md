# Agent DashKit API Reference

## Basic Information
- Base URL: `http://localhost:8000`
- Authentication: Request header `X-API-Key: <your-api-key>`
- Data Format: JSON

## Endpoints

### 1. Add Component
**POST /api/components**
```json
{
  "type": "progress|checklist|text|chart|table",
  "title": "Component Title",
  "data": {}, // Data structure matching component type
  "position": 1, // Display position, starts from 1
  "span": 1 // Width span, 1-3 (1/3, 2/3, full width)
}
```

**Response**
```json
{
  "id": "component-id",
  "success": true
}
```

### 2. Update Component
**PUT /api/components/{component_id}**
```json
{
  "title": "Optional, new title",
  "data": {}, // Optional, new data
  "position": 2, // Optional, new position
  "span": 2 // Optional, new width span
}
```

### 3. Get All Components
**GET /api/components**
**Response**
```json
{
  "components": [
    {
      "id": "component-id",
      "type": "progress",
      "title": "Title",
      "data": {},
      "position": 1,
      "span": 1,
      "created_at": "2026-03-12T14:00:00",
      "updated_at": "2026-03-12T14:30:00"
    }
  ]
}
```

### 4. Delete Component
**DELETE /api/components/{component_id}**
**Response**
```json
{
  "success": true,
  "message": "Component deleted"
}
```

### 5. Export Backup
**GET /api/export**
**Response**: Full component data backup in JSON format