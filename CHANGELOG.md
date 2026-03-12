# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-03-12

### Added
- Environment variable support via `.env` file
  - `DASHKIT_API_KEY`: API authentication key
  - `DASHKIT_PASSWORD`: Dashboard password protection
  - `DASHKIT_PORT`: Server port configuration
  - `DASHKIT_DB_PATH`: Database file path
- Dashboard password protection
  - Session-based authentication (24-hour validity)
  - Login/logout endpoints
  - Frontend password modal
- JSON export/backup API endpoint (`GET /api/export`)
- GZip compression middleware for better performance

### Changed
- Updated dependencies in `backend/requirements.txt`
- Fixed frontend CSS compatibility (removed Tailwind @apply)

### Security
- Added try-except for python-dotenv to prevent import errors

---

## [0.1.0] - 2026-03-11

### Added
- Initial MVP release
- Block-based dashboard components
- API endpoints for CRUD operations
- Built-in component types: progress, task_list, text, chart, table
- Token-based API authentication
- SQLite database storage
