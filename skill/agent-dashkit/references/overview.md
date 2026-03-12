# Agent DashKit Skill Overview

## What is this?
This skill allows nanobot agents to interact with the Agent DashKit dashboard, enabling visual display of task progress, data statistics, and real-time information.

## Key Features
- Create 7 different component types (progress, checklist, text, chart, table, timer, markdown)
- Update existing components dynamically
- Manage dashboard layout and positioning
- Export backup of all dashboard data
- Simple API interface for agent use

## Component Types
1. **Progress** - Progress bars for task completion tracking
2. **Checklist** - Interactive to-do lists with toggleable items
3. **Text** - Multi-line text cards with optional external links
4. **Chart** - Data visualizations (line, bar, pie charts)
5. **Table** - Structured data tables for metrics and reports
6. **Timer** - Countdown timers for deadlines and events
7. **Markdown** - Rendered Markdown content for formatted text

## Usage Flow
1. Set environment variables for API key and base URL
2. Use `dashkit_add_component()` to create new components
3. Use `dashkit_update_component()` to refresh data as tasks progress
4. Use `dashkit_get_components()` to list existing components for reuse
5. Clean up old components with `dashkit_delete_component()` when no longer needed

## Best Practices
- Reuse components instead of creating new ones for the same purpose
- Position important components at lower position numbers (appear higher on the dashboard)
- Keep text content concise, use links for longer content
- Limit to 3 components of the same type to avoid clutter
- Send notifications to users when critical components are updated
