# Agent DashKit
A lightweight, agent-friendly dashboard framework that lets AI agents build and customize their own dashboards like building blocks.

## Features
- 🧱 **Block-based components**: Agents can add/remove/update components via simple API calls
- 🔌 **Zero-config frontend**: Auto-generates beautiful dashboard UI without manual coding
- 🔐 **Secure API**: Token-based authentication, password protection support
- 📊 **Built-in component types**: Progress bars, task lists, text cards, charts, data tables, and more
- 🤖 **Agent-native**: Designed to be controlled entirely by AI agents, no human intervention needed
- 💾 **Data safety**: Export components as JSON backup
- ⚙️ **Environment configuration**: Configure via .env file

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: HTML + Tailwind CSS + Alpine.js (no build step required)
- Data storage: SQLite (lightweight, no external dependencies)
- Deployment: Standalone server, can be exposed via Cloudflare Tunnel/NGINX

## Project Structure
```
agent-dashkit/
├── backend/          # FastAPI server code
│   └── main.py      # Main application
├── frontend/        # Static HTML/JS/CSS files
│   └── index.html   # Dashboard UI
├── skill/           # Nanobot skill package for agent integration
├── dev-docs/        # Development documentation
└── README.md
```

## Quick Start
1. Install dependencies: `pip install -r backend/requirements.txt`
2. (Optional) Copy `.env.example` to `.env` and configure:
   - `DASHKIT_API_KEY`: Your API key (auto-generated if empty)
   - `DASHKIT_PASSWORD`: Dashboard password (optional)
   - `DASHKIT_PORT`: Server port (default: 8000)
3. Run server: `python backend/main.py`
4. Access dashboard at `http://localhost:8000`
5. Use API to add components to your dashboard

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/components` | List all dashboard components |
| POST | `/api/components` | Create a new component |
| PUT | `/api/components/{id}` | Update a component |
| DELETE | `/api/components/{id}` | Delete a component |
| GET | `/api/export` | Export all components as JSON |
| GET | `/api/templates` | Get predefined component templates |
| POST | `/api/auth/login` | Authenticate dashboard password |
| POST | `/api/auth/logout` | Logout from dashboard |
| GET | `/api/auth/status` | Check authentication status |

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DASHKIT_API_KEY` | API key for agent authentication | Auto-generated UUID |
| `DASHKIT_PASSWORD` | Dashboard password (optional) | Empty (disabled) |
| `DASHKIT_PORT` | Server port | 8000 |
| `DASHKIT_DB_PATH` | SQLite database path | dashkit.db |

## Component Types
| Type | Description | Example Data |
|------|-------------|--------------|
| `progress` | Progress bar with percentage | `{"value": 80, "status": "In Progress"}` |
| `task_list` | Checklist of tasks | `{"tasks": [{"name": "Task 1", "completed": true}]}` |
| `text` | Free-form text card | `{"content": "Your text", "source": "optional"}` |
| `chart` | Data visualization | `{"chartType": "line", "data": {...}}` |
| `table` | Tabular data | `{"headers": ["Col1"], "rows": [["val"]]}` |
| `timer` | Count-up timer | `{"value": 1234, "label": "Days"}` |
| `markdown` | Markdown renderer | `{"content": "# Hello\n**bold**"}` |
| `iframe` | Embedded content | `{"url": "https://example.com"}` |
| `calendar` | Calendar display | `{"month": "March 2026", "days": [...], "highlighted": [1, 15]}` |

## Span Control
Components can span 1, 2, or 3 columns:
```json
POST /api/components
{
  "type": "chart",
  "title": "Wide Chart",
  "span": 2,
  "data": {...}
}
```
