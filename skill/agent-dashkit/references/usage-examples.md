# Usage Examples

## Example 1: Track Task Progress
```python
# Create progress bar for report generation
component_id = dashkit_add_component(
    type="progress",
    title="Q2 Sales Report Generation",
    data={"value": 0, "max": 100, "unit": "%"},
    position=1
)

# Update progress as work completes
dashkit_update_component(component_id, data={"value": 30})
dashkit_update_component(component_id, data={"value": 60})
dashkit_update_component(component_id, data={"value": 100})

# Optional: Delete when done
# dashkit_delete_component(component_id)
```

## Example 2: Task Checklist
```python
# Create daily task checklist
component_id = dashkit_add_component(
    type="checklist",
    title="Daily Operations Tasks",
    data={
        "items": [
            {"text": "Check inventory levels", "checked": False},
            {"text": "Review advertising performance", "checked": False},
            {"text": "Process customer feedback", "checked": False},
            {"text": "Update pricing strategy", "checked": False}
        ]
    },
    position=2
)

# Mark tasks as completed
dashkit_update_component(
    component_id,
    data={
        "items": [
            {"text": "Check inventory levels", "checked": True},
            {"text": "Review advertising performance", "checked": True},
            {"text": "Process customer feedback", "checked": False},
            {"text": "Update pricing strategy", "checked": False}
        ]
    }
)
```

## Example 3: Industry News Card
```python
# Create news update card
component_id = dashkit_add_component(
    type="text",
    title="Amazon UK Policy Update",
    data={
        "content": "1. Auto parts certification requirements updated\n2. FBA inbound processing time reduced to 3 days\n3. New advertising features released for auto category",
        "link": "https://sellercentral.amazon.co.uk/news"
    },
    position=3,
    span=2
)
```

## Example 4: Sales Performance Chart
```python
# Create sales trend chart
component_id = dashkit_add_component(
    type="chart",
    title="Weekly Sales Trend",
    data={
        "type": "line",
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "datasets": [
            {
                "label": "Total Sales (£)",
                "data": [1200, 1450, 1380, 1620, 1750, 2100, 1980],
                "color": "#10b981"
            }
        ]
    },
    position=4,
    span=3
)
```

## Example 5: Inventory Table
```python
# Create inventory status table
component_id = dashkit_add_component(
    type="table",
    title="Top SKU Inventory Status",
    data={
        "headers": ["SKU", "Stock", "Daily Sales", "Est. Stockout Date"],
        "rows": [
            ["UKGSD7000TLR", "120", "45", "2026-03-25"],
            ["UKGSD6500TLR", "85", "32", "2026-03-20"],
            ["UKGSD7500TLR", "210", "28", "2026-04-10"],
            ["UKGSD8000TLR", "45", "15", "2026-03-18"]
        ]
    },
    position=5,
    span=3
)
```

## Example 6: Deadline Countdown
```python
# Create restocking deadline timer
component_id = dashkit_add_component(
    type="timer",
    title="Q2 Restocking Deadline",
    data={
        "target": "2026-03-30T23:59:59",
        "label": "Time Remaining"
    },
    position=6
)
```
