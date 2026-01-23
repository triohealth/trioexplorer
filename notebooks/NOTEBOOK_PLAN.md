# Plan: Revamp Getting Started Notebook

## Structure

### 1. Configuration
- API URL setup
- Configurable search variables: `SEARCH_TERM = "side effects"`, `COHORT_IDS = None`
- API key setup with clear instructions (remove entitlements mention)
- **Validation cell** - tests the key and shows ✓/✗ before proceeding

### 2. Step 1: Discover Available Cohorts
- Keep as-is (already good)

### 3. Step 2: Broad Search (was "Search a Cohort")
- Use `SEARCH_TERM` with high `k` (e.g., k=200)
- Show total results count
- Introduce the concept: "Now let's narrow this down with filters"

### 4. Step 3: Filtering by Quality Score
- Highlight this as the key filtering strategy
- Show how `min_quality_score` and `min_chunk_quality_score` reduce noise
- Compare counts: before vs after
- **Bar chart**: funnel showing result reduction

### 5. Step 4: Filtering by Date
- Add date filters to further narrow
- **Timeline visualization**: results mapped to note dates

### 6. Step 5: Entity and Assertion Filtering
- Keep entity/assertion tables
- Show how entity filters narrow to clinically relevant results
- Update funnel chart with this step

### 7. Step 6: Advanced Filters (renamed from Turbopuffer)
- Remove "Turbopuffer" terminology
- Show raw filter syntax for power users

### 8. Step 7: Filter Field Discovery
- Keep but describe namespace as "index partitioning scheme in our search system"
- Useful for discovering what fields are filterable

### 9. Step 8: Reviewing Results by Encounter
- Group final results by `encounter_id`
- Show encounter summary table (encounter_id, note_count, date range)
- **Display actual note text** for a few encounters

### 10. Summary
- Update endpoint table
- Remove note-types endpoint
- Emphasize the broad→narrow workflow

## Key Changes

### Remove
- Entitlements details (`read:global`, `read:<cohort-id>`)
- "Turbopuffer" terminology
- Note types section

### Add
- API key validation cell
- Configurable search variables at top
- Funnel chart (bar chart showing result reduction at each filter step)
- Timeline chart (results mapped to note dates)
- Encounter grouping with actual note display

### Rename
- "Turbopuffer Filters" → "Advanced Filters"
- "namespace" → describe as "index partitioning scheme in our search system"
- Renumber steps to flow logically

## Workflow Theme

The notebook demonstrates a **broad-to-narrow** search workflow:

```
Broad search (k=200)     ████████████████████ 500 results
+ quality ≥0.7           ████████████         200 results
+ date filter            ██████               100 results
+ entity filter          ███                   30 results
→ Review by encounter    [actual notes]
```
