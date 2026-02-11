# backend/data_cleaner.py
# STEP 3: Data Cleaning Logic for monday.com BI Agent
# Uses column IDs (robust & production-safe)

from dateutil import parser

# -------------------------------
# 1. Generic missing value handler
# -------------------------------
def clean_value(value):
    if value is None:
        return "Missing"

    value = str(value).strip()

    if value == "" or value.lower() in ["na", "n/a", "null", "-", "unknown"]:
        return "Missing"

    return value


# -------------------------------
# 2. Normalize sector names
# -------------------------------
def normalize_sector(sector):
    sector = clean_value(sector)

    if sector == "Missing":
        return "Missing"

    sector = sector.lower().replace(" ", "")

    mapping = {
        "energy": "Energy",
        "renewables": "Renewables",
        "powerline": "Powerline",
        "mining": "Mining",
        "tender": "Tender"
    }

    return mapping.get(sector, sector.capitalize())


# -------------------------------
# 3. Safe date parsing
# -------------------------------
def parse_date(date_str):
    date_str = clean_value(date_str)

    if date_str == "Missing":
        return None

    try:
        return parser.parse(date_str)
    except:
        return None


# -------------------------------
# 4. Safe number parsing
# -------------------------------
def parse_number(value):
    value = clean_value(value)

    if value == "Missing":
        return 0

    try:
        return float(value.replace(",", ""))
    except:
        return 0


# -------------------------------
# 5. Clean Deals Board data
#    (USING MONDAY COLUMN IDs)
# -------------------------------
def clean_deals(raw_items):
    cleaned_deals = []
    missing_close_date_count = 0

    # 🔑 UPDATE THESE IF YOUR COLUMN IDs DIFFER
    SECTOR_COL = "sector"
    DEAL_VALUE_COL = "deal_value"
    CLOSE_DATE_COL = "expected_close_date"
    STAGE_COL = "status"

    for item in raw_items:
        deal = {
            "deal_name": item.get("name"),
            "sector": "Missing",
            "deal_value": 0,
            "expected_close_date": None,
            "stage": "Missing"
        }

        for col in item.get("column_values", []):
            col_id = col.get("id")
            value = col.get("text")

            if col_id == SECTOR_COL:
                deal["sector"] = normalize_sector(value)

            elif col_id == DEAL_VALUE_COL:
                deal["deal_value"] = parse_number(value)

            elif col_id == CLOSE_DATE_COL:
                deal["expected_close_date"] = parse_date(value)
                if deal["expected_close_date"] is None:
                    missing_close_date_count += 1

            elif col_id == STAGE_COL:
                deal["stage"] = clean_value(value)

        cleaned_deals.append(deal)

    return cleaned_deals, missing_close_date_count


# -------------------------------
# 6. Data quality summary
# -------------------------------
def generate_data_quality_summary(total_deals, missing_close_dates):
    warnings = []

    if total_deals == 0:
        return warnings

    percentage = round((missing_close_dates / total_deals) * 100, 1)

    if percentage > 0:
        warnings.append(
            f"{percentage}% of deals are missing expected close dates. "
            "Revenue projections may be conservative."
        )

    return warnings


# -------------------------------
# 7. Step 3 pipeline runner
# -------------------------------
def run_step_3(raw_items):
    cleaned_data, missing_count = clean_deals(raw_items)

    warnings = generate_data_quality_summary(
        total_deals=len(cleaned_data),
        missing_close_dates=missing_count
    )

    return {
        "cleaned_data": cleaned_data,
        "data_quality_notes": warnings
    }
