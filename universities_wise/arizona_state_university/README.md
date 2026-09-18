# Arizona State University (ASU) Faculty & Lab Scraper

This directory contains the standalone scraper and dataset for **Arizona State University** (School for Engineering of Matter, Transport and Energy — Aerospace & Mechanical Engineering).

---

## 1. Directory Structure

```text
universities_wise/arizona_state_university/
├── README.md                              <- Detailed documentation and architecture guide
├── asu_profs.py                           <- Comprehensive standalone scraper, Excel & Markdown exporter
├── asu_aerospace_mechanical_faculty.xlsx  <- Formatted Excel dataset (strictly no CSV/JSON)
└── asu_aerospace_mechanical_faculty.md    <- Interactive Markdown faculty directory with direct links
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

### Stage 3: Rich Profile Attribute Extraction
- **Education / Degrees**: Parses HTML lists into clean degree credentials (e.g., `Ph.D. Aeronautics and Astronautics, Stanford University 2006 | M.S. Stanford University 2002`).
- **Office Location**: Extracts campus, building, and room numbers from profile microdata (e.g., `ENGRC 327 (Tempe, AZ 85287-6106)`).
- **Lab & Personal Websites**: Scrapes lab URLs hosted on ASU engineering subdomains, Google Sites, or GitHub Pages.
- **Biographies & Research Focus**: Scrapes research interest tags, expertise areas, and short bios.

### Stage 4: Deep Lab Website Intelligence Scraping
For each faculty member with an active lab URL, the scraper visits their lab homepage and extracts:
- **`Actively Hiring / Openings`**: Live graduate student (PhD/MS), postdoc, or undergraduate recruitment announcements.
- **`Target Skills / Prerequisites`**: Specific programming languages, tools, and foundations required by the PI (e.g. *Python, ROS, ROS2, PyTorch, C++, Linear Algebra, CFD*).
- **`Funding Sponsors`**: Federal and industrial grant agencies funding the lab (*NSF, NASA, DARPA, ONR, AFOSR, DOE*).
- **`Software / Code Repo`**: Links to open-source GitHub, Bitbucket, or GitLab repositories.
- **`Latest Project / Highlight`**: Active project headlines and banners.

### Stage 5: Google Scholar User ID Resolution
- Scrapes direct 12-character Google Scholar User IDs from ASU profile pages and maps verified IDs.
- For professors with public Scholar IDs, constructs exact profile URLs (`https://scholar.google.com/citations?hl=en&user=<ID>`).
- For others, builds an exact-author search query targeting ASU.

### Stage 6: Keyword Matching & Ranking
- Matches against the project's comprehensive keyword ontology (`fields.txt`) spanning **Turbulence, CFD, Fluid Dynamics, Heat Transfer, Robotics, Control, Autonomy, Materials, Structures, and Aerospace Systems**.
- Computes **`Matched Count`** and lists all unique **`Matched Fields`**.
- Sorts both sheets in descending order of **maximum matched keywords first**.

### Stage 7: Formatted Excel Output (`.xlsx`)
- Produces **only** `.xlsx` (deletes any intermediate `.csv` or `.json` files as requested).
- Contains two sheets:
  1. **`Field Matched (Max Keywords)`**: Only faculty matching at least 1 keyword, sorted with the highest keyword count first.
  2. **`All Faculty (Max Keywords)`**: All active aerospace & mechanical engineering faculty, sorted with highest keyword count first.
- Inserts active Excel `=HYPERLINK(...)` formulas for `Profile URL`, `Google Scholar URL`, `Email` (`mailto:`), `Lab / Personal Website`, and `Directory URL` at the end of each row.
- Formats headers in navy (`#1F497D`), white bold text, cell borders, and auto-adjusted column widths.

---

## 3. Columns in the Dataset (29 Total — Cold Email Outreach Architecture)

| Col # | Column Name | Description | Example Real Data |
| :---: | :--- | :--- | :--- |
| 1 | `Name` | Faculty Full Name | `Liping Wang` |
| 2 | `University` | Institution name | `Arizona State University` |
| 3 | `Profile URL` | ASU official profile link | `https://search.asu.edu/profile/lwang78` |
| 4 | `Google Scholar URL` | Direct Scholar link (hyperlinked) | `https://scholar.google.com/citations?hl=en&user=...` |
| 5 | `Job Title` | Official academic rank | `Associate Professor` |
| 6 | `Department` | Department name | `Aerospace & Mechanical Engineering` |
| 7 | `Scholar ID` | Direct Google Scholar user ID | `xT-lX9sAAAAJ` |
| 8 | `Email` | Direct email address (hyperlinked) | `liping.wang@asu.edu` |
| 9 | `Matched Count` | Total field keywords matched (Primary sort) | `7` |
| 10 | `Matched Fields` | List of matched research fields | `aerospace, guidance, heat transfer, materials...` |
| 11 | `Latest Paper / Publication` | Most recent research paper title (cold email hook) | `Simultaneous velocity and density measurements...` |
| 12 | `Courses Taught` | Filtered lecture courses taught | `MAE 241: Intro to Thermodynamics \| MAE 501...` |
| 13 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER | `2017 AFOSR Young Investigator (YIP) Award` |
| 14 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails | `Email me your CV along with a 1-2 page document...` |
| 15 | `Research Interests` | Scraped research interests | `Nanoscale radiative transfer, metamaterials` |
| 16 | `Expertise Areas` | Scraped expertise categories | `Energy, Heat Transfer, Nanotechnology` |
| 17 | `Research / Bio Summary` | Bio summary | `Associate Professor of Mechanical Engineering...` |
| 18 | `Education / Degrees` | Degrees and alma maters | `Ph.D. Mechanical Engineering, Georgia Tech 2011` |
| 19 | `Lab / Research Group Name` | Official research lab name | `Nanoscale Thermal Radiation Lab` |
| 20 | `Lab / Personal Website` | Lab homepage URL (hyperlinked) | `http://faculty.engineering.asu.edu/lpwang` |
| 21 | `Actively Hiring / Openings` | Live hiring notice from lab | `Multiple UG/MS research positions available...` |
| 22 | `Target Skills / Prerequisites` | Required technical skills | `Python, PyTorch, ROS2, Linear Algebra, CFD` |
| 23 | `Lab Facilities & Equipment` | Experimental setups, facilities & hardware | `Towing Tank, GPU Cluster, 3D Printer, AFM` |
| 24 | `Funding Sponsors` | Active research sponsors | `NASA, NSF` |
| 25 | `Software / Code Repo` | Lab GitHub or Bitbucket URL | `https://bitbucket.org/krgasu/leap/` |
| 26 | `Latest Project / Highlight` | Headline research project | `News & Awards: NSF CAREER Award` |
| 27 | `Office Location` | Building & room number | `ENGRC 327 (Tempe, AZ 85287-6106)` |
| 28 | `Is Field Match` | Boolean filter flag | `TRUE` |
| 29 | `Directory URL` | Source SEMTE directory URL | `https://faculty.engineering.asu.edu/directory/...` |

The Excel workbook contains two sheets:
1. **`Field Matched`**: Filtered cohort with `Matched Count > 0`, sorted descending by matched count.
2. **`All Faculty`**: Full active faculty cohort, sorted descending by matched count.

---

## 4. Requirements & Installation

Run using Python 3.9+:

```bash
pip install cloudscraper beautifulsoup4 openpyxl
```

### Dependency Details:
* **`cloudscraper`**: Bypasses Cloudflare bot challenges and TLS fingerprinting on university servers.
* **`beautifulsoup4`**: Parses HTML microdata, profiles, and lab websites.
* **`openpyxl`**: Generates stylized Excel workbooks, hyperlinks, borders, fills, and auto-sized columns.

---

## 5. How to Run

Navigate to this directory and run:

```bash
python asu_profs.py
```

The script will:
1. Purge any old `.csv` or `.json` files.
2. Query the ASU directory API.
3. Filter out emeritus/retired personnel.
4. Deep-scrape lab websites and individual profile pages.
5. Create and save `asu_aerospace_mechanical_faculty.xlsx`.
6. Output a complete terminal summary.
