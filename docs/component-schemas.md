# Component Data Schemas

## 1. Progress Bar (progress)
```json
{
  "value": 80, // Current value
  "max": 100, // Maximum value
  "unit": "%" // Optional, unit label
}
```
Display: Progress bar with percentage indicator

## 2. Checklist (checklist)
```json
{
  "items": [
    {"text": "Complete industry news collection", "checked": true},
    {"text": "Generate analysis report", "checked": false},
    {"text": "Sync to knowledge base", "checked": false}
  ]
}
```
Display: Interactive checklist with toggleable items

## 3. Text Card (text)
```json
{
  "content": "Amazon UK Policy Updates:\n1. Auto parts certification requirements adjusted\n2. FBA inbound time restored to 3-5 days\n3. Advertising bid limit increased by 20%",
  "link": "https://sellercentral.amazon.co.uk/news" // Optional, external link
}
```
Display: Multi-line text card with optional link

## 4. Chart (chart)
```json
{
  "type": "line|bar|pie",
  "labels": ["Jan", "Feb", "Mar", "Apr"],
  "datasets": [
    {
      "label": "Sales",
      "data": [12000, 15000, 18000, 21000],
      "color": "#3b82f6"
    }
  ]
}
```
Display: Line/bar/pie chart visualization

## 5. Table (table)
```json
{
  "headers": ["SKU", "Stock", "Sales", "Estimated Stockout Date"],
  "rows": [
    ["UKGSD7000TLR", "120", "45", "2026-03-25"],
    ["UKGSD6500TLR", "85", "32", "2026-03-20"],
    ["UKGSD7500TLR", "210", "28", "2026-04-10"]
  ]
}
```
Display: Structured data table

## 6. Countdown Timer (timer)
```json
{
  "target": "2026-03-30T23:59:59",
  "label": "Restocking Deadline"
}
```
Display: Auto-updating countdown timer

## 7. Markdown (markdown)
```json
{
  "content": "# Weekly Priorities\n- Complete advertising architecture optimization\n- Submit Q2 restocking plan\n- Analyze competitor pricing strategy\n"
}
```
Display: Rendered Markdown content