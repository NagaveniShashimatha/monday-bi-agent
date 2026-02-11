# Decision Log – Monday.com Business Intelligence Agent

## Overview

This document captures the key assumptions, design decisions, and trade-offs made while building the **Monday.com Business Intelligence Agent**.  
The goal of the project was not only to deliver correct analytics, but to handle real-world messy data and communicate insights clearly to leadership.

---

## 1. Key Assumptions

### 1.1 Data Source Assumptions
- CSV files are used **only once** to import data into monday.com boards.
- The application **never reads CSV files directly** at runtime.
- All operational and sales data is fetched dynamically from monday.com using the GraphQL API.

### 1.2 Board Structure
- Two primary boards are assumed:
  - **Deals Board** – Sales pipeline data
  - **Work Orders Board** – Project execution data
- Column names may vary slightly, so the system relies on column titles rather than hardcoded positions.

### 1.3 Sector Normalization
- Sector values are inconsistent in real data (e.g., `energy`, `ENERGY`, `Energy`).
- The system normalizes these values to a standard format (e.g., `Energy`).

### 1.4 Time Period Definition
- Quarters are interpreted as **calendar quarters**:
  - Q1: Jan–Mar
  - Q2: Apr–Jun
  - Q3: Jul–Sep
  - Q4: Oct–Dec

---

## 2. Data Cleaning & Resilience Decisions

### 2.1 Missing Data Handling
Real-world data often contains missing or invalid values such as:
- Empty strings
- `NA`, `N/A`, `null`, `unknown`

Instead of silently removing these records:
- Missing values are explicitly labeled as **“Missing”**
- Numeric fields default to `0` where appropriate
- Missing dates are tracked and reported

### 2.2 Date Parsing Strategy
- Multiple date formats are expected (e.g., `Feb 26`, `2025-03-15`, empty values)
- Dates are parsed safely using tolerant parsing logic
- Invalid or missing dates are set to `None`

### 2.3 Data Quality Transparency
Rather than hiding data issues, the system tracks them and reports caveats such as:

> “50% of deals are missing expected close dates, so revenue projections may be conservative.”

This was a deliberate design choice to support better leadership decisions.

---

## 3. Business Intelligence Design Choices

### 3.1 Insights Over Raw Numbers
The agent avoids returning only numeric outputs.

Instead of:
> “Total pipeline value = ₹0.42 Cr”

The system responds with:
> “The pipeline is moderate this quarter with ₹0.42 Cr across 2 deals, but a large portion is still in early stages.”

### 3.2 Early-Stage Risk Detection
Deals in stages like:
- Proposal
- Qualification
- Initial discussions

are flagged as early-stage risk indicators that may impact near-term revenue.

### 3.3 Multi-Board Reasoning
The architecture supports querying across:
- Sales pipeline (Deals)
- Execution data (Work Orders)

This allows future extensions such as delivery risk vs revenue analysis.

---

## 4. Conversational Interface Decisions

### 4.1 Simple UI First
- Streamlit was chosen over React to allow rapid prototyping within time constraints.
- The interface supports:
  - Free-text questions
  - Follow-up clarification questions
  - Context retention via session state

### 4.2 Clarification Over Assumption
When a question is ambiguous, the agent asks for clarification:

> “Do you want the current quarter or next quarter?”

This avoids incorrect assumptions and improves trust.

---

## 5. Leadership Updates Interpretation

### 5.1 Interpretation
The optional requirement *“help prepare data for leadership updates”* was interpreted as:

> Providing concise, ready-made summaries that a founder could directly share with leadership or investors.

### 5.2 Implementation
The agent can generate:
- Pipeline summary
- Sector contribution
- Deal count
- Key risks
- Data quality notes

All in a single, structured output.

---

## 6. Trade-offs Made

### 6.1 Rule-Based Query Understanding
- Natural language understanding is implemented using simple keyword logic.
- This was chosen for clarity and reliability under time constraints.

**With more time:**  
A full LLM-based intent parser could be added.

### 6.2 No Caching
- All data is fetched live from monday.com.

**With more time:**  
API response caching could improve performance.

---

## 7. Security Considerations

- The monday.com API token is stored as an **environment variable**
- No credentials are hardcoded
- Tokens are excluded from version control using `.gitignore`

---

## 8. What I Would Do With More Time

- Revenue forecasting models
- Trend visualizations (charts)
- Alerting for pipeline risk
- Board-level permission handling
- Multi-quarter comparisons

---

## Final Notes

This project was designed to mirror real-world business intelligence challenges:
- Messy data
- Ambiguous questions
- Leadership-level decision needs

The focus was on **clarity, resilience, and trust**, not just technical correctness.
