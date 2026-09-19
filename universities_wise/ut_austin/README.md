# The University of Texas at Austin (UT Austin) Faculty & Lab Scraper

This directory contains the standardized, production-grade faculty intelligence scraper and dataset for **The University of Texas at Austin** (Department of Aerospace Engineering and Engineering Mechanics [ASE/EM], Walker Department of Mechanical Engineering [ME], and Department of Mathematics).

---

## 1. Directory Structure

```text
universities_wise/ut_austin/
├── README.md                                   <- Detailed documentation and pipeline architecture guide
├── ut_austin_profs.py                          <- Standalone scraper, OpenAlex API extractor & exporter
├── ut_austin_cold_email_pillars.py             <- Dual flagship papers, tech stack, and tripartite findings
├── ut_austin_aerospace_mechanical_faculty.xlsx <- Formatted 3-sheet Excel dataset (strictly no CSV/JSON)
├── ut_austin_aerospace_mechanical_faculty.md   <- Standalone interactive Markdown faculty dossier
├── openalex_cache/                             <- Local JSON cache of author metadata and reconstructed abstracts
└── run.log                                     <- Real-time pipeline execution and verification log
```

---

## 2. What `ut_austin_profs.py` Does (End-to-End Pipeline)

`ut_austin_profs.py` is an **all-in-one, multi-stage automated scraper** that extracts, filters, verifies, cross-references, deep-scrapes, and formats the faculty dataset in a single run:

### Stage 1: Department Directory Harvesting via Direct REST & Algolia APIs
- **Aerospace Engineering & Engineering Mechanics (ASE/EM)**: Harvested via Cockrell School WordPress REST API (`https://ae.utexas.edu/wp-json/wp/v2/person?cockrell_person_type=3012`) -> **49 active faculty**.
- **Walker Department of Mechanical Engineering (ME)**: Harvested via Cockrell School WordPress REST API (`https://me.utexas.edu/wp-json/wp/v2/person?cockrell_person_type=34`) -> **82 active faculty**.
- **Department of Mathematics**: Harvested via Algolia InstantSearch API (`https://R1M3WN6NBD-dsn.algolia.net/1/indexes/directory_LIVE/query`, App ID: `R1M3WN6NBD`) -> **45 active faculty**.
- **Total active faculty harvested**: **176 active professors** across all three departments.

### Stage 2: Strict Active Faculty Verification (Emeritus / Retired Purge)
- `is_active_faculty()` examines all titles, ranks, and categories:
- **Completely excludes**: Emeritus professors, retired faculty, adjuncts, visiting scholars, lecturers, instructors, administrative coordinators, and postdocs.

### Stage 3: Rich Profile Attribute Extraction & Lab Scraping
- Extracts core academic and institutional profile data:
  - **Academic Rank & Department Affiliation**: Tenured/tenure-track appointments across Cockrell School and Natural Sciences.
  - **Office Location**: Campus buildings (ASE, ETC, PMA/RLM) and room numbers (96.6% coverage across all 176 professors).
  - **Research Interests & Biographies**: Extracted directly from official departmental databases and profiles.

### Stage 4: Zero Browser Dependency — OpenAlex API & Offline Abstract Reconstruction
- **No Headless Browsers Used for Publications**: All publication records and scientific abstracts are pulled programmatically via the **OpenAlex REST API** using inverted index reconstruction (`abstract_inverted_index`).
- Extracts and preserves:
  - Author metrics (`works_count`, `cited_by_count`, `h_index`).
  - Top Research Topics with publication counts.
  - Landmark historical papers (`top_cited_works`) with venues, publication years, citations, and clickable DOIs.
  - **Recent Papers (2023–2026)** (`recent_works`) with full reconstructed abstracts, venues, and direct DOIs.
- All extracted JSON data is saved locally to `openalex_cache/<slug>.json` for complete auditability and reproducibility.

### Stage 5: Cold Outreach Intelligence Synthesis (Pillars 1–4)
- **Pillar 1 — Research Hook**: Synthesized across the body of recent papers (`[Primary Method / Solver] + [Flow Regime / Physics] + [Target Engineering Outcome]`).
- **Pillar 2 — Dual Recent Flagship Papers (2023–2026)**: Two high-impact recent publications in core aero/fluids/CFD/comp math with verified direct publisher DOIs.
- **Pillar 3 — Tech Stack**: Computational solvers (DNS, LES, DG methods, AMReX, PeleC, DSMC) and experimental diagnostics (PLIF, KTV, CARS, LDV, ICP torch).
- **Pillar 4 — Tripartite Physical Findings**: Formulated individually for both flagship papers (`[gerund solver] in [geometry] demonstrating [root physical causality + hard metric]`).

### Stage 6: Multi-Sheet Excel Output (`.xlsx`)
- Produces exclusively an Excel workbook (`ut_austin_aerospace_mechanical_faculty.xlsx`) with 48 dynamic columns:
  1. **`Aero Focus`**: Exclusively Tier 1 Core Aero, Fluids, CFD, Propulsion, and Applied Math faculty (26 professors).
  2. **`Field Matched`**: All qualifying Tier 1 and Tier 2 faculty with matched keywords (101 professors).
  3. **`All Faculty`**: Complete active faculty cohort (176 professors).
- All profile URLs, Google Scholar searches, and paper DOIs use active `=HYPERLINK(...)` formulas.

### Stage 7: Standalone Interactive Markdown Dossier (`.md`)
- Outputs `ut_austin_aerospace_mechanical_faculty.md` containing:
  - Ranked jump index with research tier labels and matched keywords.
  - Four-tier classification breakdowns.
  - Comprehensive faculty dossiers featuring cold email hooks, dual flagship papers with direct DOIs, tripartite physical findings, full publisher abstracts, top-cited landmark papers, and recent publications.

---

## 3. GitHub Synchronization
- Automatically committed and pushed to GitHub under user `ksv-ai`:
  `https://github.com/ksv-ai/findprofs.git`
