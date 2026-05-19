# Syngenta-Seeds-Project

# Seed Quality Control Data Validator

**Author:** Joshua Levie  
**Language:** Python 3  
**Libraries:** Pandas, NumPy

---

## Overview

This project simulates a real-world seed quality control data validation workflow. The script generates a mock dataset representative of seed QC testing records — including variety codes, vendor information, test types, and result values — then runs a series of validation checks to identify data quality issues, produces a cleaned dataset, and outputs a detailed markdown validation report.

The project was built to demonstrate practical data validation and quality control skills applicable to agricultural and laboratory data management environments.

---

## What It Does

**1. Generates a Mock Seed QC Dataset**
Creates 200 records simulating real seed testing data across five test types:
- Germination
- Moisture
- Purity
- Vigor
- Disease Screening

Each record includes a sample ID, variety code, vendor, test type, result value, status, sample date, technician, and lot number. Intentional data quality errors are injected to simulate real-world messy data.

**2. Runs Validation Checks**
The validation engine flags the following issue types:

| Issue Type | Description |
|------------|-------------|
| `NULL` | Missing values across any column |
| `DUPLICATE` | Exact duplicate rows |
| `OUT_OF_RANGE` | Result values outside accepted ranges per test type |
| `FORMAT_ERROR` | Malformed status values or non-standard date formats |
| `INVALID_VALUE` | Unrecognized variety codes not in the approved list |

**3. Cleans the Dataset**
Applies corrections and removals based on flagged issues:
- Removes duplicate rows
- Standardizes status values to `PASS`, `FAIL`, or `PENDING`
- Removes records with out-of-range result values
- Removes records with invalid variety codes
- Removes records with non-conforming date formats

**4. Outputs a Validation Report**
Generates a markdown report including:
- Summary metrics (records processed, issues found, retention rate)
- Issue breakdown by type and column
- Full issue detail log with row-level flagging
- Validation rules applied
- Preview of the cleaned dataset

---

## Accepted Value Ranges by Test Type

| Test Type | Min | Max | Unit |
|-----------|-----|-----|------|
| Germination | 60.0 | 100.0 | % |
| Moisture | 8.0 | 14.0 | % |
| Purity | 95.0 | 100.0 | % |
| Vigor | 50.0 | 100.0 | % |
| Disease Screening | 0.0 | 5.0 | % |

---

## Output Files

Running the script produces four output files:

| File | Description |
|------|-------------|
| `seed_qc_raw.csv` | Original mock dataset with injected errors |
| `seed_qc_cleaned.csv` | Cleaned dataset after validation |
| `seed_qc_issues.csv` | Row-level log of every flagged issue |
| `seed_qc_validation_report.md` | Full markdown validation report |

---

## How to Run

**1. Clone the repository**
```
git clone https://github.com/YOURUSERNAME/seed-qc-validator.git
cd seed-qc-validator
```

**2. Install dependencies**
```
pip install pandas numpy tabulate
```

**3. Run the script**
```
python3 seed_qc_validator.py
```

Output files will be saved to the same directory.

---

## Project Structure

```
seed-qc-validator/
│
├── seed_qc_validator.py         # Main validation script
├── seed_qc_raw.csv              # Generated raw dataset
├── seed_qc_cleaned.csv          # Cleaned output dataset
├── seed_qc_issues.csv           # Issue log
├── seed_qc_validation_report.md # Markdown validation report
└── README.md                    # Project documentation
```

---

## Skills Demonstrated

- Data cleaning and validation in Python using Pandas
- Rule-based quality control logic
- Automated report generation
- Handling real-world data issues: nulls, duplicates, formatting errors, out-of-range values
- Domain-relevant dataset design for agricultural QC workflows

---

## Relevance to Industry

This project mirrors the data validation responsibilities common in agricultural quality control environments, including:
- Validating third-party test results against accepted standards
- Ensuring data integrity before entry into quality management systems (e.g., SAP QM)
- Generating audit-ready documentation of data quality checks
- Supporting compliance with seed testing standards (AOSA, ISTA)

---

*Part of the Data Science Portfolio of Joshua Levie*  
*Contact: Joshua.levie95@gmail.com*
