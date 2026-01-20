# TODO: Revamp Getting Started Notebook

## Completed Tasks

- [x] 1. Update Configuration section
  - Removed entitlements mention from prerequisites
  - Added configurable search variables (SEARCH_TERM, COHORT_IDS)
  - Added API key validation cell with ✓/✗ feedback

- [x] 2. Keep Step 1: Discover Available Cohorts (already good)
  - Updated to remove Turbopuffer reference in namespace description

- [x] 3. Remove Note Types section (Step 2 in current notebook)

- [x] 4. Create Step 2: Broad Search
  - Uses SEARCH_TERM with high k (200)
  - Shows total results count
  - Introduces "narrow down with filters" concept

- [x] 5. Create Step 3: Filtering by Quality Score
  - Highlights as key filtering strategy
  - Shows min_quality_score and min_chunk_quality_score
  - Compares counts before vs after
  - Added funnel bar chart (in Step 5)

- [x] 6. Create Step 4: Filtering by Date
  - Added date filters to narrow results
  - Added timeline visualization of results by note date

- [x] 7. Update Step 5: Entity and Assertion Filtering
  - Kept entity/assertion tables
  - Shows how filters narrow to clinically relevant results
  - Added funnel chart after this step

- [x] 8. Update Step 6: Advanced Filters
  - Renamed from "Turbopuffer Filters"
  - Removed all "Turbopuffer" terminology
  - Kept raw filter syntax for power users

- [x] 9. Update Step 7: Filter Field Discovery
  - Described namespace as "index partitioning scheme"
  - Removed Turbopuffer references

- [x] 10. Create Step 8: Reviewing Results by Encounter
  - Groups results by encounter_id
  - Shows encounter summary table
  - Displays actual note text for sample encounters

- [x] 11. Update Summary section
  - Updated endpoint table (removed note-types)
  - Emphasized broad→narrow workflow
  - Removed any remaining Turbopuffer/entitlements mentions

- [x] 12. Remove deprecated sections
  - Removed "Comparing Search Types" section
  - Removed "Visualizing Search Results" section (omission/ranking charts)
  - These are replaced by the new funnel/timeline visualizations

- [x] 13. Final review and cleanup
  - Verified all steps are numbered correctly
  - Ensured notebook flows logically
  - All cells execute in order
