# Arizona State University (ASU) Faculty & Lab Scraper

This directory contains the standalone scraper and dataset for **Arizona State University** (School for Engineering of Matter, Transport and Energy — Aerospace & Mechanical Engineering).

---

## 1. Directory Structure

```text
universities_wise/arizona_state_university/
├── README.md                              <- Detailed documentation and pipeline architecture guide
├── asu_profs.py                           <- Standalone scraper, OpenAlex API extractor & exporter
├── asu_aerospace_mechanical_faculty.xlsx  <- Formatted 3-sheet Excel dataset (strictly no CSV/JSON)
├── asu_aerospace_mechanical_faculty.md    <- Standalone interactive Markdown faculty dossier
├── openalex_cache/                        <- Local JSON cache of author metadata and abstracts
├── tools_and_inspectors/                  <- Audit, inspection, and verification scripts
└── run.log                                <- Real-time pipeline execution and verification log
```

---

## 2. What `asu_profs.py` Does (End-to-End Pipeline)

`asu_profs.py` is an **all-in-one, multi-stage automated scraper** that extracts, filters, verifies, cross-references, deep-scrapes, and styles the faculty dataset in a single run:

### Stage 1: API Discovery & Filtering
- Queries ASU's internal Search REST API:
  `https://search.asu.edu/api/v1/webdir-profiles/faculty-staff/filtered?dept_ids=1662&employee_types=Faculty,Faculty%20w/Admin%20Appointment`
- Applies `profiles_to_exclude` parameter to restrict the cohort specifically to **Aerospace & Mechanical Engineering** faculty within SEMTE.

### Stage 2: Strict Active Faculty Verification (Emeritus / Retired Purge)
- Unlike basic directory scrapers, `is_active_faculty()` examines **all** raw title and appointment channels:
  - `primary_title`
  - `working_title`
  - `titles`
  - `home_rank_description`
  - `subaffiliations`
  - `affiliations`
  - `departments` & `primary_department`
- **Completely excludes**: Emeritus professors (`Regents Professor Emeritus`, `Emeritus Faculty`), retired faculty, adjuncts, visiting scholars, lecturers, instructors, administrative coordinators, and postdocs.

### Stage 3: Rich Profile Attribute Extraction & Lab Scraping
- **Education / Degrees**: Parses HTML lists into clean degree credentials (e.g., `Ph.D. Aeronautics and Astronautics, Stanford University 2006 | M.S. Stanford University 2002`).
- **Office Location**: Extracts campus, building, and room numbers from profile microdata (e.g., `ENGRC 327 (Tempe, AZ 85287-6106)`).
- **Lab & Personal Websites**: Scrapes lab URLs hosted on ASU engineering subdomains, Google Sites, or GitHub Pages.
- **Biographies & Research Focus**: Scrapes research interest tags, expertise areas, and short bios.
- **Deep Lab Scraping**: Visits faculty lab homepages to extract actively hiring statements, prerequisites (Python, C++, ROS2, PyTorch, OpenFOAM), facilities, sponsors, and code repositories.

### Stage 4: Zero Browser Dependency — OpenAlex API & Offline Abstract Reconstruction
- **No Headless Browsers Used for Publications**: All publication records, citations, and scientific abstracts are pulled programmatically via the **OpenAlex REST API** using inverted index reconstruction (`abstract_inverted_index`).
- Extracts and preserves:
  - Author metrics (`works_count`, `cited_by_count`).
  - Top 3 Research Topics with publication counts.
  - Landmark historical papers (`top_cited_works`) with venues, publication years, citations, and clickable DOIs.
  - **5 Recent Papers (2023–2026)** (`recent_works`) with full reconstructed abstracts, venues, and direct DOIs.
- All extracted JSON data is saved locally to `openalex_cache/<slug>.json` for complete auditability and reproducibility.

### Stage 5: Cold Outreach Intelligence Synthesis (Pillars 1–4)
- **Pillar 1 — Research Hook**: Synthesized across the body of 4–5 recent papers (`[Primary Method / Solver] + [Flow Regime / Physics] + [Target Engineering Outcome]`).
- **Pillar 2 — Dual Recent Flagship Papers (2020–2026)**: Two high-impact recent publications in core aero/fluids/CFD with verified direct publisher DOIs.
- **Pillar 3 — Tech Stack**: Computational solvers (LES, DNS, LBM, DG, OpenFOAM) and experimental diagnostics (PIV, CARS, PLIF).
- **Pillar 4 — Tripartite Physical Findings**: Formulated individually for both flagship papers (`[gerund solver] in [geometry] demonstrating [root physical causality + hard metric]`).

### Stage 6: Multi-Sheet Excel Output (`.xlsx`)
- Produces **only** `.xlsx` (strictly no intermediate `.csv` or `.json` files).
- Contains 3 dedicated sheets structured with 48 dynamic columns:
  1. **`Aero Focus`**: Solely Tier 1 Core Aero / Fluids / CFD / Propulsion and Applied Math faculty.
  2. **`Field Matched`**: All qualifying Tier 1 and Tier 2 faculty matching project keywords, sorted descending.
  3. **`All Faculty`**: Complete qualifying Tier 1 and Tier 2 verified active faculty cohort.
- Inserts active Excel `=HYPERLINK(...)` formulas for `Profile URL`, `Google Scholar URL`, `Email` (`mailto:`), `Lab / Personal Website`, paper DOIs, and `Directory URL`.

### Stage 7: Standalone Interactive Markdown Dossier (`.md`)
- Generates `asu_aerospace_mechanical_faculty.md` containing:
  - Quick-jump directory index ranked by Research Tier and matched keywords.
  - Visual status indicators (🔥 Hiring, 📩 Cold Email, 📄 Paper, 🔬 Lab).
  - Dedicated faculty dossiers with verified flagship DOIs, tripartite physical findings, and full unabridged abstracts.

---

## 3. Columns in the Dataset (48 Total — Cold Email Outreach Architecture)

| Col # | Column Header | Description |
| :---: | :--- | :--- |
| 1 | `Name` | Faculty Full Name |
| 2 | `University` | Institution name |
| 3 | `Profile URL` | ASU official profile link (hyperlinked) |
| 4 | `Google Scholar URL` | Direct Scholar link (hyperlinked) |
| 5 | `Job Title` | Official academic rank |
| 6 | `Department` | Department name (Aerospace & Mechanical Engineering) |
| 7 | `Scholar ID` | Direct Google Scholar user ID |
| 8 | `Email` | Direct email address (hyperlinked) |
| 9 | `Research Tier` | Authoritative tier (Tier 1: Core Aero / Fluids / Comp Math, Tier 2: Thermal / Energy) |
| 10 | `Research Category` | Formatted tier badge and domain description |
| 11 | `Matched Count` | Total field keywords matched (Primary sort key) |
| 12 | `Matched Fields` | List of matched research fields |
| 13 | `Research Hook` | **Pillar 1**: Synthesized from method, flow regime, and target outcome |
| 14 | `Tech Stack` | **Pillar 3**: Exact solvers, codes, and diagnostics across recent papers |
| 15 | `Flagship 1 Title` | **Pillar 2 (Paper 1)**: Landmark recent paper 1 title (2020–2026) |
| 16 | `Flagship 1 DOI` | **Pillar 2 DOI (Paper 1)**: Direct clickable DOI link for flagship paper 1 |
| 17 | `Flagship 1 Tripartite Finding` | **Pillar 4 (Paper 1 Finding)**: Tripartite structure (`[gerund solver] ... demonstrating [number]`) |
| 18 | `Flagship 1 Abstract` | Complete publisher-verified abstract for flagship paper 1 |
| 19 | `Flagship 2 Title` | **Pillar 2 (Paper 2)**: Landmark recent paper 2 title (2020–2026) |
| 20 | `Flagship 2 DOI` | **Pillar 2 DOI (Paper 2)**: Direct clickable DOI link for flagship paper 2 |
| 21 | `Flagship 2 Tripartite Finding` | **Pillar 4 (Paper 2 Finding)**: Tripartite structure for flagship paper 2 |
| 22 | `Flagship 2 Abstract` | Complete publisher-verified abstract for flagship paper 2 |
| 23 | `Flagship Paper Hook` | Composite dual paper hook title string |
| 24 | `Flagship Paper DOI` | Composite clickable DOIs |
| 25 | `Physical Finding` | Primary tripartite finding |
| 26 | `Latest Paper / Publication` | Most recent research paper title (cold email hook) |
| 27 | `Recent Papers (2023-2026)` | 5 recent papers with journal, year & clickable DOI |
| 28 | `Top Cited Papers` | Landmark papers with journal, year, cites & clickable DOI |
| 29 | `Courses Taught` | Filtered lecture courses taught |
| 30 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER |
| 31 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails |
| 32 | `OpenAlex Research Topics` | Top 3 topics with publication counts from OpenAlex |
| 33 | `Google Scholar Tags` | Official research interest tags |
| 34 | `Research Interests` | Scraped research interests |
| 35 | `Expertise Areas` | Scraped expertise categories |
| 36 | `Research / Bio Summary` | Bio summary |
| 37 | `Education / Degrees` | Degrees and alma maters |
| 38 | `Lab / Research Group Name` | Official research lab name |
| 39 | `Lab / Personal Website` | Lab homepage URL (hyperlinked) |
| 40 | `Actively Hiring / Openings` | Live hiring notice from lab |
| 41 | `Target Skills / Prerequisites` | Required technical skills (Python, ROS2, CFD, etc.) |
| 42 | `Lab Facilities & Equipment` | Experimental setups, facilities & hardware |
| 43 | `Funding Sponsors` | Active research sponsors (NSF, NASA, ONR, etc.) |
| 44 | `Software / Code Repo` | Lab GitHub or Bitbucket repository URL |
| 45 | `Latest Project / Highlight` | Headline research project or banner |
| 46 | `Office Location` | Building & room number |
| 47 | `Is Field Match` | Boolean filter flag |
| 48 | `Directory URL` | Source SEMTE directory URL |

---

## 4. Requirements & Execution

Run using Python 3.9+:

```bash
pip install cloudscraper beautifulsoup4 openpyxl requests
python asu_profs.py
```

---

## 5. Automatic GitHub Synchronization
- All changes are synchronized and pushed to GitHub under user `ksv-ai`:
  `https://github.com/ksv-ai/findprofs.git`
