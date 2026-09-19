# Georgia Institute of Technology (Georgia Tech) Faculty & Lab Scraper

This directory contains the standalone scraper and dataset for the **Georgia Institute of Technology** (Daniel Guggenheim School of Aerospace Engineering, George W. Woodruff School of Mechanical Engineering, and School of Mathematics).

---

## 1. Directory Structure

```text
universities_wise/georgia_tech_university/
├── README.md                                       <- Detailed documentation and pipeline architecture guide
├── georgia_tech_profs.py                           <- Standalone scraper, OpenAlex API extractor & exporter
├── georgia_tech_cold_email_pillars.py              <- Dual flagship papers, tech stack, and tripartite findings
├── georgia_tech_aerospace_mechanical_faculty.xlsx  <- Formatted 3-sheet Excel dataset (strictly no CSV/JSON)
├── georgia_tech_aerospace_mechanical_faculty.md    <- Standalone interactive Markdown faculty dossier
├── openalex_cache/                                 <- Local JSON cache of author metadata and abstracts
└── run.log                                         <- Real-time pipeline execution and verification log
```

---

## 2. What `georgia_tech_profs.py` Does (End-to-End Pipeline)

`georgia_tech_profs.py` is an **all-in-one, multi-stage automated scraper** that extracts, filters, verifies, cross-references, deep-scrapes, and formats the faculty dataset in a single run:

### Stage 1: Department Directory Harvesting
- Scrapes the official Drupal directory views across three schools:
  - **Aerospace Engineering (AE)**: `https://ae.gatech.edu/browser-directory?tid=1` (Academic Faculty)
  - **Mechanical Engineering (ME)**: `https://me.gatech.edu/faculty?field_staff_group_target_id=5` (All 6 paginated sections)
  - **School of Mathematics (Math)**: `https://math.gatech.edu/people?field_job_type_tid=11` (Full faculty roster)
- Harvests a total cohort of **266 active professors**.

### Stage 2: Strict Active Faculty Verification (Emeritus / Retired Purge)
- `is_active_faculty()` examines all titles, ranks, and categories:
- **Completely excludes**: Emeritus professors, retired faculty, adjuncts, visiting scholars, lecturers, instructors, administrative coordinators, and postdocs.

### Stage 3: Rich Profile Attribute Extraction & Deep Lab Scraping
- Fetches individual profile pages to extract:
  - **Education / Degrees**: Degree credentials, institutions, and graduation years.
  - **Office Location**: Campus building name and office room numbers.
  - **Lab & Personal Websites**: Lab homepages and research group URLs.
  - **Biographies & Research Focus**: Research interests, teaching interests, and bio summaries.
  - **Lab Scraping**: Actively hiring statements, target skills (C++, Python, OpenFOAM), equipment, sponsors, and code repositories.

### Stage 4: Zero Browser Dependency — OpenAlex API & Offline Abstract Reconstruction
- **No Headless Browsers Used for Publications**: All publication records and scientific abstracts are pulled programmatically via the **OpenAlex REST API** using inverted index reconstruction (`abstract_inverted_index`).
- Extracts and preserves:
  - Author metrics (`works_count`, `cited_by_count`).
  - Top 3 Research Topics with publication counts.
  - Landmark historical papers (`top_cited_works`) with venues, publication years, citations, and clickable DOIs.
  - **5 Recent Papers (2023–2026)** (`recent_works`) with full reconstructed abstracts, venues, and direct DOIs.
- All extracted JSON data is saved locally to `openalex_cache/<slug>.json` for complete auditability and reproducibility.

### Stage 5: Cold Outreach Intelligence Synthesis (Pillars 1–4)
- **Pillar 1 — Research Hook**: Synthesized across the body of 4–5 recent papers (`[Primary Method / Solver] + [Flow Regime / Physics] + [Target Engineering Outcome]`).
- **Pillar 2 — Dual Recent Flagship Papers (2020–2026)**: Two high-impact recent publications in core aero/fluids/CFD with verified direct publisher DOIs.
- **Pillar 3 — Tech Stack**: Computational solvers (LES, DNS, LBM, DG, OpenFOAM, RAPTOR) and experimental diagnostics (PIV, CARS, PLIF).
- **Pillar 4 — Tripartite Physical Findings**: Formulated individually for both flagship papers (`[gerund solver] in [geometry] demonstrating [root physical causality + hard metric]`).

### Stage 6: Multi-Sheet Excel Output (`.xlsx`)
- Produces exclusively an Excel workbook (`georgia_tech_aerospace_mechanical_faculty.xlsx`) with 48 dynamic columns:
  1. **`Aero Focus`**: Exclusively Tier 1 Core Aero, Fluids, CFD, Propulsion, and Applied Math faculty.
  2. **`Field Matched`**: All qualifying Tier 1 and Tier 2 faculty with matched keywords.
  3. **`All Faculty`**: Complete qualifying Tier 1 and Tier 2 cohort.
- All profile URLs, Google Scholar searches, and paper DOIs use active `=HYPERLINK(...)` formulas.

### Stage 7: Standalone Interactive Markdown Dossier (`.md`)
- Outputs `georgia_tech_aerospace_mechanical_faculty.md` containing:
  - Ranked jump index with visual status indicators (🔥 Hiring, 📩 Cold Email, 📄 Paper, 🔬 Lab).
  - Four-tier classification breakdowns.
  - Comprehensive faculty dossiers featuring cold email hooks, dual flagship papers with direct DOIs, tripartite physical findings, full publisher abstracts, and recent publications.

---

## 3. GitHub Synchronization
- Automatically committed and pushed to GitHub under user `ksv-ai`:
  `https://github.com/ksv-ai/findprofs.git`
