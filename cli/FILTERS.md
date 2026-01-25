# Trioexplorer Filters Guide

This guide covers entity and assertion filters for refining clinical note searches.

## Overview

The API supports two types of filters:

1. **Entity Filters** (`--entity-filters`) — Filter by extracted medical entities (medications, diagnoses, symptoms, etc.)
2. **Metadata Filters** (`--filters`) — Filter by note metadata (note_type, date, etc.)

## Available Entity Filter Fields

| Category | Fields |
|----------|--------|
| **Entities** | `medications`, `diagnoses`, `symptoms`, `procedures`, `lab_tests`, `allergies`, `vitals`, `anatomy`, `devices`, `organisms`, `substances`, `observations`, `social` |
| **Assertions** | `present`, `negated`, `historical`, `hypothetical`, `family` |
| **Combined** | `medications_present`, `diagnoses_negated`, `symptoms_historical`, etc. |

## Discovering Available Filter Values

Before filtering, check what values are indexed for your cohort:

```bash
# List all filter fields
trioexplorer list filters --namespace "v2-cohort-YOUR_COHORT_ID-arctic"

# List values for a specific field
trioexplorer list filters --namespace "v2-cohort-YOUR_COHORT_ID-arctic" --field medications --limit 100

# Search for specific values (pipe to grep)
trioexplorer list filters --namespace "v2-cohort-YOUR_COHORT_ID-arctic" --field medications -o csv | grep -i "metformin"
```

## Medications Filters

### Filter by medication mentions

```bash
# Notes mentioning metformin (any assertion)
trioexplorer search "diabetes management" \
  --entity-filters '{"medications": ["metformin"]}'

# Notes where metformin is currently prescribed (present assertion)
trioexplorer search "diabetes management" \
  --entity-filters '{"medications_present": ["metformin"]}'

# Notes where a medication was stopped/discontinued (historical)
trioexplorer search "side effects" \
  --entity-filters '{"medications_historical": ["metformin"]}'

# Multiple medications (OR logic within field)
trioexplorer search "blood sugar control" \
  --entity-filters '{"medications_present": ["metformin", "glipizide", "insulin"]}'
```

### Common medication filter patterns

```bash
# Biologics for asthma
trioexplorer search "asthma exacerbation" \
  --entity-filters '{"medications_present": ["Dupixent", "Nucala", "Fasenra", "Tezspire"]}'

# Pain management
trioexplorer search "chronic pain" \
  --entity-filters '{"medications_present": ["oxycodone", "hydrocodone", "tramadol"]}'

# Cardiac medications
trioexplorer search "heart failure" \
  --entity-filters '{"medications_present": ["lisinopril", "metoprolol", "furosemide"]}'
```

## Lab Tests Filters

### Filter by lab mentions

```bash
# Notes mentioning A1C results
trioexplorer search "diabetes control" \
  --entity-filters '{"lab_tests": ["A1C", "hemoglobin A1c"]}'

# Notes with present lab values
trioexplorer search "kidney function" \
  --entity-filters '{"lab_tests_present": ["creatinine", "BUN", "GFR"]}'

# Notes discussing abnormal labs
trioexplorer search "abnormal results" \
  --entity-filters '{"lab_tests_present": ["elevated", "low", "abnormal"]}'
```

### Common lab filter patterns

```bash
# Metabolic panel
trioexplorer search "metabolic disorder" \
  --entity-filters '{"lab_tests": ["glucose", "sodium", "potassium", "chloride", "CO2"]}'

# Liver function
trioexplorer search "liver disease" \
  --entity-filters '{"lab_tests": ["AST", "ALT", "bilirubin", "albumin"]}'

# Lipid panel
trioexplorer search "cholesterol management" \
  --entity-filters '{"lab_tests": ["LDL", "HDL", "triglycerides", "total cholesterol"]}'

# CBC
trioexplorer search "anemia" \
  --entity-filters '{"lab_tests": ["hemoglobin", "hematocrit", "WBC", "platelets"]}'
```

## Vitals Filters

### Filter by vital sign mentions

```bash
# Notes mentioning blood pressure
trioexplorer search "hypertension" \
  --entity-filters '{"vitals": ["blood pressure", "BP", "systolic", "diastolic"]}'

# Notes with present vital measurements
trioexplorer search "patient assessment" \
  --entity-filters '{"vitals_present": ["heart rate", "pulse", "temperature"]}'

# Notes mentioning abnormal vitals
trioexplorer search "critical care" \
  --entity-filters '{"vitals_present": ["tachycardia", "hypotension", "fever"]}'
```

### Common vitals filter patterns

```bash
# Respiratory vitals
trioexplorer search "respiratory distress" \
  --entity-filters '{"vitals": ["oxygen saturation", "SpO2", "respiratory rate"]}'

# Cardiovascular vitals
trioexplorer search "cardiac monitoring" \
  --entity-filters '{"vitals": ["blood pressure", "heart rate", "pulse"]}'

# General assessment
trioexplorer search "routine exam" \
  --entity-filters '{"vitals_present": ["weight", "height", "BMI", "temperature"]}'
```

## Combining Filters

### Multiple entity types (AND logic between fields)

```bash
# Notes with both a medication AND a diagnosis
trioexplorer search "treatment response" \
  --entity-filters '{"medications_present": ["metformin"], "diagnoses_present": ["diabetes"]}'

# Notes with medication AND abnormal lab
trioexplorer search "drug monitoring" \
  --entity-filters '{"medications_present": ["warfarin"], "lab_tests": ["INR", "PT"]}'
```

### With cohort filtering

```bash
# Search within specific cohort with entity filter
trioexplorer search "efficacy assessment" \
  --cohort-ids YOUR_COHORT_ID \
  --entity-filters '{"medications_present": ["Dupixent"]}' \
  -d patient \
  -k 20
```

## Metadata Filters

For filtering by note metadata rather than extracted entities.

### Patient and Encounter Filtering

```bash
# Filter to a specific patient
trioexplorer search "medication history" \
  --patient-id "001EFCDE-62D9-42A0-B184-3E3C732EBDA5"

# Filter to a specific encounter
trioexplorer search "vital signs" \
  --encounter-id "ABC12345-6789-0DEF-GHIJ-KLMNOPQRSTUV"

# Combine patient with other filters
trioexplorer search "diabetes management" \
  --patient-id "001EFCDE-62D9-42A0-B184-3E3C732EBDA5" \
  --date-from 2025-01-01 \
  --note-types "Progress Note,Discharge Summary"
```

### Note Type Filtering

```bash
# Single note type
trioexplorer search "discharge planning" \
  --note-types "Discharge Summary"

# Multiple note types (comma-separated, OR logic)
trioexplorer search "patient assessment" \
  --note-types "Progress Note,H&P,Consultation"
```

### Date Range Filtering

```bash
# Notes from a specific date onwards
trioexplorer search "follow up" \
  --date-from 2025-01-01

# Notes before a specific date
trioexplorer search "historical treatment" \
  --date-to 2024-12-31

# Notes within a date range
trioexplorer search "treatment response" \
  --date-from 2025-01-01 \
  --date-to 2025-01-31
```

### Raw Filter Format (Advanced)

For complex filter logic, use the `--filters` flag with JSON format:

```bash
# Filter by note type (raw format)
trioexplorer search "discharge planning" \
  --filters '["note_type", "Eq", "DISCHARGE SUMMARY"]'

# OR logic for patients
trioexplorer search "comparison" \
  --filters '["Or", [["patient_id", "Eq", "PATIENT-1-UUID"], ["patient_id", "Eq", "PATIENT-2-UUID"]]]'

# Exclude specific note types
trioexplorer search "clinical notes" \
  --filters '["Not", ["note_type", "Eq", "Telephone Encounter"]]'
```

### Filter Format Reference

The API uses an array-based filter format:

| Field | Operators | Example |
|-------|-----------|---------|
| `patient_id` | `Eq` | `["patient_id", "Eq", "UUID"]` |
| `encounter_id` | `Eq` | `["encounter_id", "Eq", "UUID"]` |
| `note_type` | `Eq`, `NotEq`, `In`, `NotIn` | `["note_type", "In", ["Progress Note", "H&P"]]` |
| `note_date` | `Eq`, `Lt`, `Lte`, `Gt`, `Gte` | `["note_date", "Gte", "2025-01-01"]` |
| `cohort_ids` | `Contains`, `ContainsAny` | `["cohort_ids", "Contains", 123]` |

Logical operators: `And`, `Or`, `Not`

```json
// Combine multiple conditions
["And", [
  ["patient_id", "Eq", "UUID"],
  ["note_date", "Gte", "2025-01-01"],
  ["note_type", "In", ["Progress Note", "Discharge Summary"]]
]]
```

## Assertion Types Explained

| Assertion | Description | Example |
|-----------|-------------|---------|
| `present` | Currently active/true | "Patient is taking metformin" |
| `negated` | Explicitly denied | "Patient denies taking aspirin" |
| `historical` | Past occurrence | "Previously on insulin" |
| `hypothetical` | Conditional/possible | "May need to start statin" |
| `family` | Family history | "Mother has diabetes" |

## Tips

1. **Case sensitivity**: Filter values are generally case-insensitive, but check indexed values to be sure
2. **Partial matching**: Filters use exact matching; include variations (e.g., "metformin", "Metformin", "METFORMIN")
3. **Empty results**: If no results, the entity may not be indexed; try including it in the search query instead
4. **Performance**: Entity filters are applied post-retrieval; use cohort filters for large-scale filtering

## Troubleshooting

### No results with entity filter?

1. Check if the entity is indexed:
   ```bash
   trioexplorer list filters --namespace "v2-cohort-COHORT_ID-arctic" --field medications -o csv | grep -i "your_medication"
   ```

2. If not indexed, include in search query instead:
   ```bash
   trioexplorer search "your_medication lack of efficacy" --cohort-ids COHORT_ID
   ```

### Finding the namespace for your cohort

The namespace format is: `v2-cohort-{COHORT_ID}-arctic`

Or check the metadata in JSON output:
```bash
trioexplorer search "test" --cohort-ids YOUR_COHORT_ID -k 1 -o json | grep namespace
```
