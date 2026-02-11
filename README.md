# Monday.com Business Intelligence Agent

## Overview

This project is an AI-powered **Business Intelligence Agent** built on top of **monday.com**.  
It enables founders and executives to ask **high-level business questions** and receive **clean, contextual, and decision-ready insights** across messy operational and sales data.

The agent dynamically connects to monday.com boards, cleans real-world data issues, and generates insights with clear data-quality caveats.

---

## Problem Statement

Business leaders often need quick answers like:

> *“How’s our energy pipeline looking this quarter?”*

Answering this manually requires:
- Exporting data from multiple monday.com boards
- Cleaning inconsistent formats
- Handling missing or incomplete records
- Writing custom analysis for every question

This project automates that entire process.

---

## Key Features

### 1. Monday.com Integration (Read-Only)
- Uses monday.com **GraphQL API (v2)**
- Dynamically fetches board data using board IDs
- No CSV files are accessed directly after import

### 2. Data Resilience & Cleaning
- Handles missing values (`"", NA, null, unknown`)
- Normalizes inconsistent sector names (e.g., `energy`, `ENERGY` → `Energy`)
- Safely parses dates and numbers
- Tracks data quality issues instead of hiding them

### 3. Business Intelligence Logic
- Pipeline value calculations
- Sector-wise breakdowns
- Quarter-based analysis
- Early-stage vs late-stage deal insights

### 4. Founder-Friendly Insights
Instead of raw numbers, the agent provides **context**:

> “The pipeline is strong this quarter with ₹0.42 Cr across 2 deals, but 50% of deals are missing close dates, so projections may be conservative.”

### 5. Conversational Interface
- Simple chat-based UI built with **Streamlit**
- Supports clarification questions (e.g., current vs next quarter)
- Maintains conversation context

### 6. Leadership Updates (Optional Feature)
- Generates ready-made summaries for leadership or investors
- Includes pipeline, risks, and data quality notes

---

## Architecture Overview:
monday-bi-agent/
│
├── backend/
│ ├── monday_client.py # monday.com API integration
│ ├── data_cleaner.py # Data cleaning & normalization logic
│ ├── bi_engine.py # Business intelligence & insights
│ ├── app.py # Streamlit conversational app
│ ├── test_cleaner.py # Step 3 validation tests
│ └── test_bi_engine.py # BI logic tests
│
├── README.md
├── decision-log.md
└── requirements.txt

---

## Tech Stack

- **Python**
- **monday.com GraphQL API**
- **Streamlit** (UI)
- **Requests** (API calls)
- **python-dateutil** (date parsing)

---


