# Agent DashKit
A lightweight, agent-friendly dashboard framework that lets AI agents build and customize their own dashboards like building blocks.

## Features
- 🧱 **Block-based components**: Agents can add/remove/update components via simple API calls
- 🔌 **Zero-config frontend**: Auto-generates beautiful dashboard UI without manual coding
- 🔐 **Secure API**: Token-based authentication, no exposed server access
- 📊 **Built-in component types**: Progress bars, task lists, text cards, charts, data tables, and more
- 🤖 **Agent-native**: Designed to be controlled entirely by AI agents, no human intervention needed

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: HTML + Tailwind CSS + Alpine.js (no build step required)
- Data storage: SQLite (lightweight, no external dependencies)
- Deployment: Standalone server, can be exposed via Cloudflare Tunnel/NGINX

## Project Structure
```
agent-dashkit/
├── backend/          # FastAPI server code
├── frontend/         # Static HTML/JS/CSS files
├── skill/            # Nanobot skill package for agent integration
├── docs/             # Documentation and API specs
└── README.md
```

## Quick Start
1. Install dependencies: `pip install -r backend/requirements.txt`
2. Run server: `python backend/main.py`
3. Access dashboard at `http://localhost:8000`
4. Use the skill API to add components to your dashboard
