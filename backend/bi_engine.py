# backend/bi_engine.py
# STEP 4: Business Intelligence Engine

from datetime import datetime
from collections import defaultdict

# -------------------------------
# Helper: Get current quarter
# -------------------------------
def get_current_quarter(date):
    if date is None:
        return None
    month = date.month
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4


# -------------------------------
# 1. Energy Pipeline (Quarter-wise)
# -------------------------------
def energy_pipeline_this_quarter(cleaned_deals, data_quality_notes):
    current_quarter = get_current_quarter(datetime.now())

    total_value = 0
    deal_count = 0

    for deal in cleaned_deals:
        if deal["sector"] == "Energy":
            deal_quarter = get_current_quarter(deal["expected_close_date"])

            if deal_quarter == current_quarter:
                total_value += deal["deal_value"]
                deal_count += 1

    response = (
        f"Energy pipeline this quarter is valued at ₹{round(total_value/1e7,2)} Cr "
        f"across {deal_count} active deals."
    )

    if data_quality_notes:
        response += "\n\n" + "\n".join(data_quality_notes)

    return response


# -------------------------------
# 2. Overall Pipeline Summary
# -------------------------------
def overall_pipeline_summary(cleaned_deals, data_quality_notes):
    total_value = sum(d["deal_value"] for d in cleaned_deals)
    total_deals = len(cleaned_deals)

    response = (
        f"Total pipeline value is ₹{round(total_value/1e7,2)} Cr "
        f"across {total_deals} deals."
    )

    if data_quality_notes:
        response += "\n\n" + "\n".join(data_quality_notes)

    return response


# -------------------------------
# 3. Sector-wise Breakdown
# -------------------------------
def sector_breakdown(cleaned_deals):
    sector_totals = defaultdict(float)

    for deal in cleaned_deals:
        sector_totals[deal["sector"]] += deal["deal_value"]

    summary_lines = []
    for sector, value in sector_totals.items():
        summary_lines.append(
            f"{sector}: ₹{round(value/1e7,2)} Cr"
        )

    return "Sector-wise pipeline:\n" + "\n".join(summary_lines)


# -------------------------------
# 4. Leadership Update Generator
# -------------------------------
def leadership_update(cleaned_deals, data_quality_notes):
    total_value = sum(d["deal_value"] for d in cleaned_deals)
    total_deals = len(cleaned_deals)

    energy_value = sum(
        d["deal_value"] for d in cleaned_deals if d["sector"] == "Energy"
    )

    response = (
        "📊 Leadership Update\n"
        "------------------\n"
        f"• Total Pipeline: ₹{round(total_value/1e7,2)} Cr\n"
        f"• Total Deals: {total_deals}\n"
        f"• Energy Sector Contribution: ₹{round(energy_value/1e7,2)} Cr\n"
    )

    if data_quality_notes:
        response += "\n Data Quality Notes:\n" + "\n".join(data_quality_notes)

    return response
# -------------------------------
# 5. Insight Generator (STEP 5)
# -------------------------------
def generate_pipeline_insight(cleaned_deals, data_quality_notes):
    total_value = sum(d["deal_value"] for d in cleaned_deals)
    total_deals = len(cleaned_deals)

    # Early stage detection
    early_stages = ["Proposal", "Qualification", "Initial"]
    early_stage_count = sum(
        1 for d in cleaned_deals if d["stage"] in early_stages
    )

    # Strength judgement
    if total_value >= 1e7:  # ₹1 Cr
        strength = "strong"
    else:
        strength = "moderate"

    # Headline
    response = (
        f"The pipeline appears {strength} this quarter with "
        f"₹{round(total_value/1e7,2)} Cr across {total_deals} deals.\n\n"
    )

    # Insight
    if total_deals > 0:
        early_ratio = early_stage_count / total_deals

        if early_ratio > 0.5:
            response += (
                "Most deals are currently in early stages, which suggests healthy interest "
                "but may delay near-term revenue conversion.\n"
            )
        else:
            response += (
                "A healthy portion of deals are in advanced stages, supporting near-term "
                "revenue confidence.\n"
            )

    # Risks / caveats
    if data_quality_notes:
        response += "\n⚠️ " + " ".join(data_quality_notes)

    return response


