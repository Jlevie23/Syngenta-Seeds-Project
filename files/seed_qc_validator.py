"""
Seed Quality Control Data Validation Script
Author: Joshua Levie
Description: Generates a mock seed QC dataset, identifies data quality issues
             (nulls, duplicates, out-of-range values, formatting errors),
             outputs a cleaned dataset and a markdown validation report.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ── Configuration ─────────────────────────────────────────────────────────────
RANDOM_SEED = 42
NUM_RECORDS = 200
OUTPUT_DIR = "/mnt/user-data/outputs"

# Valid reference values
VALID_VARIETIES = ["SYN-101", "SYN-202", "SYN-303", "SYN-404", "SYN-505"]
VALID_VENDORS = ["AgriTest Labs", "SeedCheck Inc", "CropVerify LLC", "BioSeed QA"]
VALID_TEST_TYPES = ["Germination", "Moisture", "Purity", "Vigor", "Disease Screening"]
VALID_STATUSES = ["PASS", "FAIL", "PENDING"]

# Acceptable ranges per test type
TEST_RANGES = {
    "Germination":        (60.0, 100.0),
    "Moisture":           (8.0,  14.0),
    "Purity":             (95.0, 100.0),
    "Vigor":              (50.0, 100.0),
    "Disease Screening":  (0.0,  5.0),
}

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)


# ── 1. Generate Mock Dataset ───────────────────────────────────────────────────
def generate_mock_data(n=NUM_RECORDS):
    base_date = datetime(2024, 1, 1)
    records = []

    for i in range(1, n + 1):
        test_type = random.choice(VALID_TEST_TYPES)
        lo, hi = TEST_RANGES[test_type]
        result = round(random.uniform(lo, hi), 2)
        status = "PASS" if result >= lo + (hi - lo) * 0.15 else "FAIL"
        sample_date = base_date + timedelta(days=random.randint(0, 364))

        records.append({
            "sample_id":    f"SMP-{i:04d}",
            "variety":      random.choice(VALID_VARIETIES),
            "vendor":       random.choice(VALID_VENDORS),
            "test_type":    test_type,
            "result_value": result,
            "result_unit":  "%" ,
            "status":       status,
            "sample_date":  sample_date.strftime("%Y-%m-%d"),
            "technician":   random.choice(["J. Smith", "A. Patel", "M. Torres", "R. Kim"]),
            "lot_number":   f"LOT-{random.randint(1000, 9999)}",
        })

    df = pd.DataFrame(records)

    # ── Inject intentional errors ──────────────────────────────────────────────
    idx = df.index.tolist()

    # Nulls
    for col in ["result_value", "vendor", "status", "lot_number"]:
        null_idx = random.sample(idx, 8)
        df.loc[null_idx, col] = np.nan

    # Duplicates (copy 10 rows)
    dupes = df.sample(10, random_state=1)
    df = pd.concat([df, dupes], ignore_index=True)

    # Out-of-range result values
    oor_idx = random.sample(df.index.tolist(), 12)
    df.loc[oor_idx, "result_value"] = [
        round(random.uniform(-5, -0.1), 2) if i % 2 == 0
        else round(random.uniform(101, 120), 2)
        for i in range(12)
    ]

    # Bad formatting in status
    fmt_idx = random.sample(df.index.tolist(), 10)
    df.loc[fmt_idx, "status"] = random.choices(
        ["pass", "fail", "Pass ", " FAIL", "pending", "PASSS"], k=10
    )

    # Invalid variety codes
    bad_variety_idx = random.sample(df.index.tolist(), 6)
    df.loc[bad_variety_idx, "variety"] = ["SYN-999", "UNKNOWN", "syn101", "N/A", "SYN-000", "???"]

    # Bad date formats
    bad_date_idx = random.sample(df.index.tolist(), 8)
    df.loc[bad_date_idx, "sample_date"] = random.choices(
        ["15/03/2024", "March 2024", "2024/99/01", "N/A", ""], k=8
    )

    return df.sample(frac=1, random_state=42).reset_index(drop=True)


# ── 2. Validation Engine ───────────────────────────────────────────────────────
def validate(df):
    issues = []

    def flag(row_idx, col, issue_type, detail):
        issues.append({
            "row":        row_idx,
            "column":     col,
            "issue_type": issue_type,
            "detail":     detail,
        })

    # --- Nulls ---
    for col in df.columns:
        null_rows = df[df[col].isnull()].index.tolist()
        for r in null_rows:
            flag(r, col, "NULL", f"Missing value in '{col}'")

    # --- Duplicates ---
    dup_mask = df.duplicated(keep="first")
    for r in df[dup_mask].index.tolist():
        flag(r, "ALL", "DUPLICATE", "Exact duplicate row")

    # --- Out-of-range result values ---
    for _, row in df.iterrows():
        tt = row.get("test_type")
        rv = row.get("result_value")
        if pd.notnull(tt) and pd.notnull(rv) and tt in TEST_RANGES:
            lo, hi = TEST_RANGES[tt]
            if not (lo <= float(rv) <= hi):
                flag(row.name, "result_value",
                     "OUT_OF_RANGE",
                     f"Value {rv} outside expected range [{lo}, {hi}] for {tt}")

    # --- Status formatting ---
    for r, val in df["status"].items():
        if pd.notnull(val) and str(val).strip().upper() not in VALID_STATUSES:
            flag(r, "status", "FORMAT_ERROR",
                 f"Invalid status value: '{val}'")

    # --- Invalid variety codes ---
    for r, val in df["variety"].items():
        if pd.notnull(val) and val not in VALID_VARIETIES:
            flag(r, "variety", "INVALID_VALUE",
                 f"Unrecognized variety code: '{val}'")

    # --- Date format validation ---
    for r, val in df["sample_date"].items():
        if pd.notnull(val) and val != "":
            try:
                datetime.strptime(str(val), "%Y-%m-%d")
            except ValueError:
                flag(r, "sample_date", "FORMAT_ERROR",
                     f"Date not in YYYY-MM-DD format: '{val}'")

    return pd.DataFrame(issues)


# ── 3. Clean Dataset ───────────────────────────────────────────────────────────
def clean(df, issues_df):
    cleaned = df.copy()

    # Remove duplicates
    cleaned = cleaned.drop_duplicates(keep="first")

    # Standardize status
    cleaned["status"] = cleaned["status"].apply(
        lambda x: x.strip().upper() if pd.notnull(x) else x
    )
    cleaned.loc[~cleaned["status"].isin(VALID_STATUSES + [np.nan]), "status"] = np.nan

    # Remove rows with out-of-range result values
    oor_rows = issues_df[issues_df["issue_type"] == "OUT_OF_RANGE"]["row"].unique()
    cleaned = cleaned.drop(index=[r for r in oor_rows if r in cleaned.index], errors="ignore")

    # Remove rows with invalid variety codes
    bad_variety_rows = issues_df[issues_df["issue_type"] == "INVALID_VALUE"]["row"].unique()
    cleaned = cleaned.drop(index=[r for r in bad_variety_rows if r in cleaned.index], errors="ignore")

    # Remove rows with bad date formats
    bad_date_rows = issues_df[
        (issues_df["issue_type"] == "FORMAT_ERROR") & (issues_df["column"] == "sample_date")
    ]["row"].unique()
    cleaned = cleaned.drop(index=[r for r in bad_date_rows if r in cleaned.index], errors="ignore")

    cleaned = cleaned.reset_index(drop=True)
    return cleaned


# ── 4. Markdown Report ─────────────────────────────────────────────────────────
def generate_report(raw_df, cleaned_df, issues_df, report_path):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(raw_df)
    total_issues = len(issues_df)
    removed = total - len(cleaned_df)

    type_counts = issues_df["issue_type"].value_counts()
    col_counts  = issues_df["column"].value_counts()

    lines = [
        "# Seed QC Data Validation Report",
        f"\n**Generated:** {now}  ",
        f"**Script:** seed_qc_validator.py  ",
        f"**Author:** Joshua Levie\n",
        "---\n",

        "## Summary",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total raw records | {total} |",
        f"| Total issues flagged | {total_issues} |",
        f"| Records removed during cleaning | {removed} |",
        f"| Records in cleaned dataset | {len(cleaned_df)} |",
        f"| Data retention rate | {len(cleaned_df)/total*100:.1f}% |\n",

        "---\n",
        "## Issues by Type",
        "| Issue Type | Count |",
        "|------------|-------|",
    ]
    for issue_type, count in type_counts.items():
        lines.append(f"| {issue_type} | {count} |")

    lines += [
        "\n---\n",
        "## Issues by Column",
        "| Column | Count |",
        "|--------|-------|",
    ]
    for col, count in col_counts.items():
        lines.append(f"| {col} | {count} |")

    lines += [
        "\n---\n",
        "## Issue Detail Log",
        "| Row | Column | Issue Type | Detail |",
        "|-----|--------|------------|--------|",
    ]
    for _, row in issues_df.iterrows():
        lines.append(f"| {row['row']} | {row['column']} | {row['issue_type']} | {row['detail']} |")

    lines += [
        "\n---\n",
        "## Validation Rules Applied",
        "- **NULL check:** Flagged missing values across all columns",
        "- **Duplicate check:** Identified and removed exact duplicate rows",
        "- **Out-of-range check:** Validated `result_value` against accepted ranges per test type:",
    ]
    for tt, (lo, hi) in TEST_RANGES.items():
        lines.append(f"  - {tt}: [{lo}, {hi}]")

    lines += [
        "- **Status formatting:** Standardized to PASS / FAIL / PENDING; invalid values set to null",
        "- **Variety code validation:** Flagged unrecognized variety codes against approved list",
        "- **Date format validation:** Enforced YYYY-MM-DD format; non-conforming rows removed\n",
        "---\n",
        "## Cleaned Dataset Preview (first 10 rows)\n",
        cleaned_df.head(10).to_markdown(index=False),
        "\n---\n",
        "*End of Report*",
    ]

    with open(report_path, "w") as f:
        f.write("\n".join(lines))


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating mock seed QC dataset...")
    raw_df = generate_mock_data()

    print("Running validation checks...")
    issues_df = validate(raw_df)

    print("Cleaning dataset...")
    cleaned_df = clean(raw_df, issues_df)

    # Save outputs
    raw_path     = os.path.join(OUTPUT_DIR, "seed_qc_raw.csv")
    cleaned_path = os.path.join(OUTPUT_DIR, "seed_qc_cleaned.csv")
    issues_path  = os.path.join(OUTPUT_DIR, "seed_qc_issues.csv")
    report_path  = os.path.join(OUTPUT_DIR, "seed_qc_validation_report.md")

    raw_df.to_csv(raw_path, index=False)
    cleaned_df.to_csv(cleaned_path, index=False)
    issues_df.to_csv(issues_path, index=False)
    generate_report(raw_df, cleaned_df, issues_df, report_path)

    print(f"\n✅ Complete!")
    print(f"   Raw dataset:        {raw_path}")
    print(f"   Cleaned dataset:    {cleaned_path}")
    print(f"   Issues log:         {issues_path}")
    print(f"   Validation report:  {report_path}")
    print(f"\n   Records: {len(raw_df)} raw → {len(cleaned_df)} clean")
    print(f"   Issues flagged: {len(issues_df)}")
