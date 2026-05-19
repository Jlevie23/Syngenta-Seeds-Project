# Seed QC Data Validation Report

**Generated:** 2026-05-19 00:52:22  
**Script:** seed_qc_validator.py  
**Author:** Joshua Levie

---

## Summary
| Metric | Value |
|--------|-------|
| Total raw records | 210 |
| Total issues flagged | 63 |
| Records removed during cleaning | 30 |
| Records in cleaned dataset | 180 |
| Data retention rate | 85.7% |

---

## Issues by Type
| Issue Type | Count |
|------------|-------|
| NULL | 33 |
| OUT_OF_RANGE | 12 |
| DUPLICATE | 7 |
| INVALID_VALUE | 6 |
| FORMAT_ERROR | 5 |

---

## Issues by Column
| Column | Count |
|--------|-------|
| result_value | 20 |
| lot_number | 10 |
| vendor | 8 |
| status | 7 |
| ALL | 7 |
| variety | 6 |
| sample_date | 5 |

---

## Issue Detail Log
| Row | Column | Issue Type | Detail |
|-----|--------|------------|--------|
| 14 | vendor | NULL | Missing value in 'vendor' |
| 38 | vendor | NULL | Missing value in 'vendor' |
| 49 | vendor | NULL | Missing value in 'vendor' |
| 63 | vendor | NULL | Missing value in 'vendor' |
| 72 | vendor | NULL | Missing value in 'vendor' |
| 83 | vendor | NULL | Missing value in 'vendor' |
| 134 | vendor | NULL | Missing value in 'vendor' |
| 200 | vendor | NULL | Missing value in 'vendor' |
| 60 | result_value | NULL | Missing value in 'result_value' |
| 72 | result_value | NULL | Missing value in 'result_value' |
| 94 | result_value | NULL | Missing value in 'result_value' |
| 117 | result_value | NULL | Missing value in 'result_value' |
| 119 | result_value | NULL | Missing value in 'result_value' |
| 123 | result_value | NULL | Missing value in 'result_value' |
| 166 | result_value | NULL | Missing value in 'result_value' |
| 180 | result_value | NULL | Missing value in 'result_value' |
| 7 | status | NULL | Missing value in 'status' |
| 16 | status | NULL | Missing value in 'status' |
| 117 | status | NULL | Missing value in 'status' |
| 128 | status | NULL | Missing value in 'status' |
| 172 | status | NULL | Missing value in 'status' |
| 186 | status | NULL | Missing value in 'status' |
| 198 | status | NULL | Missing value in 'status' |
| 19 | lot_number | NULL | Missing value in 'lot_number' |
| 37 | lot_number | NULL | Missing value in 'lot_number' |
| 46 | lot_number | NULL | Missing value in 'lot_number' |
| 91 | lot_number | NULL | Missing value in 'lot_number' |
| 108 | lot_number | NULL | Missing value in 'lot_number' |
| 130 | lot_number | NULL | Missing value in 'lot_number' |
| 146 | lot_number | NULL | Missing value in 'lot_number' |
| 163 | lot_number | NULL | Missing value in 'lot_number' |
| 169 | lot_number | NULL | Missing value in 'lot_number' |
| 177 | lot_number | NULL | Missing value in 'lot_number' |
| 66 | ALL | DUPLICATE | Exact duplicate row |
| 124 | ALL | DUPLICATE | Exact duplicate row |
| 130 | ALL | DUPLICATE | Exact duplicate row |
| 177 | ALL | DUPLICATE | Exact duplicate row |
| 179 | ALL | DUPLICATE | Exact duplicate row |
| 201 | ALL | DUPLICATE | Exact duplicate row |
| 209 | ALL | DUPLICATE | Exact duplicate row |
| 16 | result_value | OUT_OF_RANGE | Value -4.31 outside expected range [50.0, 100.0] for Vigor |
| 29 | result_value | OUT_OF_RANGE | Value 113.47 outside expected range [8.0, 14.0] for Moisture |
| 34 | result_value | OUT_OF_RANGE | Value -1.68 outside expected range [60.0, 100.0] for Germination |
| 47 | result_value | OUT_OF_RANGE | Value -1.45 outside expected range [0.0, 5.0] for Disease Screening |
| 93 | result_value | OUT_OF_RANGE | Value 107.65 outside expected range [60.0, 100.0] for Germination |
| 120 | result_value | OUT_OF_RANGE | Value -0.56 outside expected range [50.0, 100.0] for Vigor |
| 140 | result_value | OUT_OF_RANGE | Value 112.07 outside expected range [95.0, 100.0] for Purity |
| 161 | result_value | OUT_OF_RANGE | Value 117.59 outside expected range [8.0, 14.0] for Moisture |
| 167 | result_value | OUT_OF_RANGE | Value -4.68 outside expected range [0.0, 5.0] for Disease Screening |
| 185 | result_value | OUT_OF_RANGE | Value -3.37 outside expected range [0.0, 5.0] for Disease Screening |
| 189 | result_value | OUT_OF_RANGE | Value 106.4 outside expected range [0.0, 5.0] for Disease Screening |
| 196 | result_value | OUT_OF_RANGE | Value 102.8 outside expected range [95.0, 100.0] for Purity |
| 64 | variety | INVALID_VALUE | Unrecognized variety code: 'syn101' |
| 89 | variety | INVALID_VALUE | Unrecognized variety code: 'N/A' |
| 110 | variety | INVALID_VALUE | Unrecognized variety code: 'UNKNOWN' |
| 173 | variety | INVALID_VALUE | Unrecognized variety code: 'SYN-000' |
| 198 | variety | INVALID_VALUE | Unrecognized variety code: '???' |
| 207 | variety | INVALID_VALUE | Unrecognized variety code: 'SYN-999' |
| 20 | sample_date | FORMAT_ERROR | Date not in YYYY-MM-DD format: 'N/A' |
| 54 | sample_date | FORMAT_ERROR | Date not in YYYY-MM-DD format: 'March 2024' |
| 82 | sample_date | FORMAT_ERROR | Date not in YYYY-MM-DD format: '15/03/2024' |
| 136 | sample_date | FORMAT_ERROR | Date not in YYYY-MM-DD format: '15/03/2024' |
| 150 | sample_date | FORMAT_ERROR | Date not in YYYY-MM-DD format: 'N/A' |

---

## Validation Rules Applied
- **NULL check:** Flagged missing values across all columns
- **Duplicate check:** Identified and removed exact duplicate rows
- **Out-of-range check:** Validated `result_value` against accepted ranges per test type:
  - Germination: [60.0, 100.0]
  - Moisture: [8.0, 14.0]
  - Purity: [95.0, 100.0]
  - Vigor: [50.0, 100.0]
  - Disease Screening: [0.0, 5.0]
- **Status formatting:** Standardized to PASS / FAIL / PENDING; invalid values set to null
- **Variety code validation:** Flagged unrecognized variety codes against approved list
- **Date format validation:** Enforced YYYY-MM-DD format; non-conforming rows removed

---

## Cleaned Dataset Preview (first 10 rows)

| sample_id   | variety   | vendor         | test_type   |   result_value | result_unit   | status   | sample_date   | technician   | lot_number   |
|:------------|:----------|:---------------|:------------|---------------:|:--------------|:---------|:--------------|:-------------|:-------------|
| SMP-0031    | SYN-303   | BioSeed QA     | Vigor       |          57.01 | %             | FAIL     | 2024-04-03    | A. Patel     | LOT-2235     |
| SMP-0173    | SYN-404   | CropVerify LLC | Vigor       |          86.48 | %             | PASS     | 2024-06-09    | M. Torres    | LOT-7132     |
| SMP-0085    | SYN-505   | BioSeed QA     | Germination |          83.15 | %             | PASS     | 2024-06-08    | R. Kim       | LOT-4249     |
| SMP-0200    | SYN-101   | AgriTest Labs  | Germination |          62.28 | %             | FAIL     | 2024-05-26    | R. Kim       | LOT-8581     |
| SMP-0061    | SYN-202   | CropVerify LLC | Moisture    |          10.52 | %             | PASS     | 2024-07-13    | R. Kim       | LOT-9977     |
| SMP-0156    | SYN-505   | BioSeed QA     | Moisture    |          10.33 | %             | PASS     | 2024-07-08    | A. Patel     | LOT-7797     |
| SMP-0046    | SYN-101   | BioSeed QA     | Vigor       |          62.56 | %             | PASS     | 2024-01-27    | M. Torres    | LOT-1722     |
| SMP-0183    | SYN-505   | AgriTest Labs  | Purity      |          98.61 | %             | nan      | 2024-10-17    | J. Smith     | LOT-3549     |
| SMP-0010    | SYN-101   | SeedCheck Inc  | Moisture    |          12.02 | %             | PASS     | 2024-12-25    | A. Patel     | LOT-3677     |
| SMP-0197    | SYN-404   | BioSeed QA     | Germination |          67.09 | %             | PASS     |               | R. Kim       | LOT-6295     |

---

*End of Report*