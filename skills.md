---
name: faculty-scraper-pipeline
description: Comprehensive operational guide and playbook for scraping, filtering, and structuring university faculty directories, research groups, and lab websites into standardized Excel workbooks.
---

# University Faculty & Lab Scraping Playbook (`skills.md`)

This skill defines the standardized protocol for extracting, filtering, ranking, and exporting university faculty data into clean, clickable `.xlsx` workbooks.

---

## 1. Core Operating Constraints & Rules

1. **NO Intermediate CSV or JSON Files**:
   - The final output MUST strictly be a stylized Excel workbook (`.xlsx`).
   - Clean up and purge any temporary `.csv` or `.json` files upon completion.
2. **Strict Active Faculty Verification (Zero Emeritus / Retired Faculty)**:
   - Always inspect ALL candidate title fields, appointment lists, affiliations, and subaffiliations.
   - Reject any profile containing: `emeritus`, `retired`, `adjunct`, `visiting`, `lecturer`, `instructor`, `postdoc`, `courtesy`, or `staff`.
3. **Keyword Matching & Ranking (`fields.txt`)**:
   - Extract research keywords from `fields.txt` across Turbulence, CFD, Fluids, Thermal/Heat Transfer, Robotics, Control, Autonomy, Materials, Structures, and Aerospace.
   - Both sheets in Excel must be sorted in descending order of **maximum matched keywords first** (`Matched Count`).
4. **Active Clickable Excel Hyperlinks**:
   - Every URL and email must use `=HYPERLINK("...", "...")` formulas and OpenPyXL `Hyperlink` styles so they work seamlessly in Microsoft Excel, Google Sheets, and LibreOffice.
5. **Authentic, Real Data Only**:
   - Never fabricate data. If a faculty member does not have a lab website or office number, leave the cell empty.
6. **Automatic GitHub Synchronization**:
   - After code or dataset modifications, commit and push to GitHub repository under user `ksv-ai`.

---

## 2. Standardized 28-Column Dataset Schema (Cold Outreach Architecture)

Every university extraction pipeline outputs an Excel workbook with two clean sheets:
1. **`Field Matched`**: Only professors with `Matched Count > 0`, sorted descending.
2. **`All Faculty`**: Complete cohort of verified active faculty, sorted descending by matched count.

### Column Specification:

| Col # | Column Header | Description |
| :---: | :--- | :--- |
| 1 | `Name` | Faculty full name |
| 2 | `University` | Institution name |
| 3 | `Profile URL` | Official university directory profile page (hyperlinked) |
| 4 | `Google Scholar URL` | Direct Scholar URL with `user=<id>` or targeted search |
| 5 | `Job Title` | Academic rank (Professor, Associate Professor, Assistant Professor) |
| 6 | `Department` | Department / School name |
| 7 | `Scholar ID` | Direct Google Scholar 12-character User ID |
| 8 | `Email` | Hyperlinked email address (`mailto:`) |
| 9 | `Matched Count` | Integer count of matching research fields (primary sorting key) |
| 10 | `Matched Fields` | Comma-separated list of matched field keywords |
| 11 | `Latest Paper / Publication` | Most recent research paper title (cold email hook) |
| 12 | `Courses Taught` | Filtered lecture courses taught |
| 13 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER |
| 14 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails |
| 15 | `Research Interests` | Specific research topic tags |
| 16 | `Expertise Areas` | High-level research domain taxonomy |
| 17 | `Research / Bio Summary` | Bio summary or research focus paragraph |
| 18 | `Education / Degrees` | Degrees, institutions, and graduation years |
| 19 | `Lab / Research Group Name` | Official research lab or group title |
| 20 | `Lab / Personal Website` | Hyperlinked personal or lab homepage |
| 21 | `Actively Hiring / Openings` | Recruitment announcements extracted from lab websites |
| 22 | `Target Skills / Prerequisites` | Required skills/languages (Python, C++, ROS2, PyTorch, etc.) |
| 23 | `Funding Sponsors` | Federal/industrial sponsors (NSF, NASA, ONR, DARPA, etc.) |
| 24 | `Software / Code Repo` | Open-source GitHub/Bitbucket/GitLab repositories |
| 25 | `Latest Project / Highlight` | Project banner, latest headline, or paper announcement |
| 26 | `Office Location` | Building and room number |
| 27 | `Is Field Match` | Boolean (`TRUE` / `FALSE`) |
| 28 | `Directory URL` | Source university directory URL (at the end of every row) |

---

## 3. How to Scrape New Universities

When adding a new university:
1. Create a directory under `universities_wise/<university_name>/`.
2. Inspect the target directory page using `tools_and_inspectors/` prototypes (check if it uses a JSON API endpoint or HTML cards).
3. Implement a scraper conforming to the 5-stage pipeline:
   - **Stage 1 (Harvest)**: Retrieve directory records.
   - **Stage 2 (Filter)**: Purge emeritus, retired, and adjunct personnel.
   - **Stage 3 (Enrich Profile)**: Extract education credentials, office locations, and Google Scholar IDs.
   - **Stage 4 (Deep-Scrape Lab)**: Visit lab homepages to extract hiring notices, required skills, funding sponsors, and code repositories.
   - **Stage 5 (Excel Export)**: Format into two sheets sorted by `Matched Count` descending with clickable `=HYPERLINK(...)` cells.
