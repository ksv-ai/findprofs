# University of Colorado Boulder Faculty & Lab Scraper

This directory contains the standalone pipeline, OpenAlex publication harvester, and research intelligence dataset for the **University of Colorado Boulder** (Ann and H.J. Smead Department of Aerospace Engineering Sciences, Paul M. Rady Department of Mechanical Engineering, and Department of Applied Mathematics).

---

## 1. Directory Structure

```text
universities_wise/university_of_colorado_boulder/
├── README.md                                         <- Detailed documentation and pipeline architecture guide
├── cu_boulder_profs.py                               <- Standalone scraper, OpenAlex API extractor & Excel exporter
├── cu_boulder_cold_email_pillars.py                <- Dual flagship papers, direct DOIs, tech stack, and tripartite findings
├── cu_boulder_aerospace_mechanical_faculty.xlsx    <- Formatted 3-sheet Excel dataset (generated upon execution)
├── cu_boulder_aerospace_mechanical_faculty.md      <- Standalone interactive Markdown faculty dossier (generated upon execution)
├── openalex_cache/                                   <- Local JSON cache of author metadata, top papers, and reconstructed abstracts
└── run.log                                           <- Real-time pipeline execution and verification log
```

---

## 2. What `cu_boulder_profs.py` Does (End-to-End Pipeline)

`cu_boulder_profs.py` is an **all-in-one, multi-stage automated scraper and intelligence synthesis pipeline** that extracts, filters, cross-references, deep-scrapes, and formats the faculty dataset:

### Stage 1: Department Directory Harvesting via Native Drupal JSON:API
- Directly interfaces with the official CU Boulder Drupal JSON:API endpoints:
  - **Aerospace Engineering Sciences (Aero)**: `https://www.colorado.edu/aerospace/jsonapi/node/ucb_person`
  - **Paul M. Rady Mechanical Engineering (ME)**: `https://www.colorado.edu/mechanical/jsonapi/node/ucb_person`
  - **Department of Applied Mathematics (AMath)**: `https://www.colorado.edu/amath/jsonapi/node/ucb_person`
- Automatically traverses pagination (`page[offset]` and `page[limit]=50`) to collect active faculty nodes.

### Stage 2: Strict Active Faculty Verification (Emeritus / Staff Purge)
- `is_active_faculty()` examines academic titles, appointments, and job ranks:
- **Completely excludes**: Emeritus professors, retired faculty, adjuncts, lecturers, instructors, administrative staff, coordinators, postdocs, and students.
- Retains only active regular tenured, tenure-track, and endowed research professors.

### Stage 3: Rich Profile Attribute Extraction & Deep Lab Scraping
- Resolves official profile URLs (`https://www.colorado.edu/<dept><path.alias>`) and extracts:
  - **Education / Degrees**: Degrees, institutions, and disciplines.
  - **Office Location**: Building codes and room numbers (e.g., `AERO 452`, `ECME 120`).
  - **Lab & Personal Websites**: Direct URLs to laboratory domains.
  - **Research & Bio Summaries**: Research interests and biographical statements.
  - **Deep Lab Scraping**: Actively hiring statements, target technical skills (C++, Python, OpenFOAM, PyTorch), experimental equipment/facilities, and code repositories.

### Stage 4: Zero Browser Dependency — OpenAlex API & Abstract Reconstruction
- **No Headless Browsers Used for Publications**: All publication records and scientific abstracts are pulled programmatically via the **OpenAlex REST API** using inverted index reconstruction (`abstract_inverted_index`).
- Extracts and preserves:
  - Author metrics (`works_count`, `cited_by_count`).
  - Top 3 Research Topics with publication counts.
  - Landmark historical papers (`top_cited_works`) with venues, publication years, citations, and clickable DOIs.
  - **Recent Papers (2023–2026)** (`recent_works`) with full reconstructed abstracts, venues, and direct DOIs.
- All extracted JSON data is saved locally to `openalex_cache/<slug>.json` for complete auditability and reproducibility.

### Stage 5: Cold Outreach Intelligence Synthesis (Pillars 1–4)
- Formulates personalized cold outreach pillars for Tier 1 Core Aero / CFD / Fluids / Comp Math faculty:
  - **Pillar 1 — Research Hook**: Synthesized across recent papers (`[Primary Method / Solver] + [Flow Regime / Physics] + [Target Engineering Outcome]`).
  - **Pillar 2 — Dual Recent Flagship Papers (2020–2026)**: Two high-impact recent publications in core aero/fluids/CFD with verified direct publisher DOIs.
  - **Pillar 3 — Tech Stack**: Computational solvers (DSMC, PHASTA, FEM, IGA, LES, DNS, OpenFOAM) and experimental diagnostics (PIV, Molecular beam, AFM, Laser spectroscopy).
  - **Pillar 4 — Tripartite Physical Findings**: Formulated individually for both flagship papers (`[gerund solver] in [geometry] demonstrating [root physical causality + hard metric]`).

### Stage 6: Multi-Sheet Excel Output (`.xlsx`)
- Produces an Excel workbook (`cu_boulder_aerospace_mechanical_faculty.xlsx`) with 48 dynamic columns:
  1. **`Aero Focus`**: Exclusively Tier 1 Core Aero, Fluids, CFD, Propulsion, and Applied Math faculty.
  2. **`Field Matched`**: All keyword-matched faculty.
  3. **`All Faculty`**: Complete qualifying active cohort.
- Features **dual hyperlink registration**: uses both Excel `=HYPERLINK(url, text)` formulas and OpenPyXL `cell.hyperlink = url` styling with Calibri 11pt blue underline (`#0563C1`) for universal spreadsheet compatibility.

### Stage 7: Standalone Interactive Markdown Dossier (`.md`)
- Outputs `cu_boulder_aerospace_mechanical_faculty.md` containing:
  - Ranked jump index with visual status indicators (🔥 Hiring, 📩 Cold Email, 📄 Paper, 🔬 Lab).
  - Four-tier classification breakdowns.
  - Comprehensive faculty dossiers featuring cold email hooks, dual flagship papers with direct DOIs, tripartite physical findings, full publisher abstracts, and recent publications.

---

## 3. How to Run

Execute the main script directly from the terminal or command prompt:

```bash
cd d:\Others\findprofs\universities_wise\university_of_colorado_boulder
python cu_boulder_profs.py
```

The script will automatically execute all scraping stages, cross-reference OpenAlex intelligence, populate the cold outreach pillars, and generate both the formatted Excel workbook (`cu_boulder_aerospace_mechanical_faculty.xlsx`) and Markdown dossier (`cu_boulder_aerospace_mechanical_faculty.md`).

---

## 4. GitHub Synchronization

All code and assets are committed and tracked under GitHub repository:
`https://github.com/ksv-ai/findprofs.git`
