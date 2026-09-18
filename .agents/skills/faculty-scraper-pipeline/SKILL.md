---
name: faculty-scraper-pipeline
description: Comprehensive operational guide and playbook for scraping, filtering, and structuring university faculty directories, research groups, and lab websites into standardized Excel workbooks.
---

# University Faculty & Lab Scraping Playbook (`skills.md`)

This skill defines the standardized protocol for extracting, filtering, ranking, and exporting university faculty data into clean, clickable `.xlsx` workbooks.

---

## 1. Core Operating Constraints & Rules

1. **NO Intermediate CSV or JSON Spreadsheets**:
   - The final primary output MUST strictly be a stylized Excel workbook (`.xlsx`) and interactive markdown reference (`.md`).
   - Clean up and purge any temporary `.csv` or tabular `.json` spreadsheet dumps.
   - Preserved API Intelligence: All raw API extractions from OpenAlex must be preserved in a dedicated `openalex_cache/` directory (named by professor slug) for complete reproducibility, auditability, and future reference.
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

## 2. Standardized 33-Column Dataset Schema (Cold Outreach Architecture)

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
| 12 | `Recent Papers (2024-2026)` | 3 recent papers with journal, year & clickable DOI |
| 13 | `Top Cited Papers` | 3 landmark papers with journal, year, cites & clickable DOI |
| 14 | `Courses Taught` | Filtered lecture courses taught |
| 15 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER |
| 16 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails |
| 17 | `OpenAlex Research Topics` | Top 3 research topics with publication counts from OpenAlex |
| 18 | `Google Scholar Tags` | Extracted Google Scholar / OpenAlex research interest tags |
| 19 | `Research Interests` | Specific research topic tags |
| 20 | `Expertise Areas` | High-level research domain taxonomy |
| 21 | `Research / Bio Summary` | Bio summary or research focus paragraph |
| 22 | `Education / Degrees` | Degrees, institutions, and graduation years |
| 23 | `Lab / Research Group Name` | Official research lab or group title |
| 24 | `Lab / Personal Website` | Hyperlinked personal or lab homepage |
| 25 | `Actively Hiring / Openings` | Recruitment announcements extracted from lab websites |
| 26 | `Target Skills / Prerequisites` | Required skills/languages (Python, C++, ROS2, PyTorch, etc.) |
| 27 | `Lab Facilities & Equipment` | Experimental setups, facilities & hardware |
| 28 | `Funding Sponsors` | Federal/industrial sponsors (NSF, NASA, ONR, DARPA, etc.) |
| 29 | `Software / Code Repo` | Open-source GitHub/Bitbucket/GitLab repositories |
| 30 | `Latest Project / Highlight` | Project banner, latest headline, or paper announcement |
| 31 | `Office Location` | Building and room number |
| 32 | `Is Field Match` | Boolean (`TRUE` / `FALSE`) |
| 33 | `Directory URL` | Source university directory URL (at the end of every row) |

---

## 3. Playbook: How to Transfer the Pipeline to Any New University

To scrape any new institution (e.g. Georgia Tech, Purdue, MIT, Michigan) and achieve identical high-fidelity output, follow this standardized 7-step replication protocol:

### Step 1: Project Setup & Workspace Isolation
1. Create a dedicated directory: `universities_wise/<university_slug>/` (e.g. `universities_wise/georgia_tech/`).
2. Follow the no-CSV/JSON rule: Only produce the final `.xlsx` workbook and `.md` reference directory. Delete any temporary dump files automatically.
3. Import the shared 33-column `COLUMNS_CONFIG` and keyword ontology (`TARGET_KEYWORDS`, `EXCLUDED_KEYWORDS`) directly from the project standard.

### Step 2: Directory Architecture Discovery & Harvesting (Stage 1)
1. Identify the target schools/departments (e.g. Aerospace Engineering + Mechanical Engineering).
2. Inspect the network requests and DOM structure:
   - **JSON REST API Endpoint** (e.g. ASU Drupal API): If the university powers its directory via an API, call it directly with pagination (`page_size=100`) to retrieve raw records with rich metadata.
   - **Server-Side Rendered HTML Cards** (e.g. Georgia Tech, Auburn): Parse cards using `BeautifulSoup` or `cloudscraper`, extracting faculty name, academic title, department, email, and profile URL.
   - **Client-Side SPA / Dynamic Loading**: If behind client-side rendering or bot-protection, use `cloudscraper` sessions with realistic headers.

### Step 3: Strict Active Faculty Verification (Stage 2)
1. Inspect all candidate titles, appointments, affiliations, and rank descriptions.
2. Filter out all non-target personnel:
   - Reject: `emeritus`, `retired`, `emerita`, `adjunct`, `visiting`, `lecturer`, `instructor`, `postdoc`, `courtesy`, `administrative`, `coordinator`, `advisor`, `manager`, `staff`.
3. Retain strictly active tenured & tenure-track faculty:
   - Keep: `Assistant Professor`, `Associate Professor`, `Professor`, `Chaired Professor`, `Regents Professor`.

### Step 4: Primary Profile Scraping & Cold Email Hooks (Stage 3)
Visit each faculty member's official university profile page (`https://search...` or `https://.../people/...`) to extract:
1. **Office Location**: Building, room number, and campus.
2. **Education & Degrees**: Degree credentials, universities, and graduation years.
3. **Courses Taught**: Filter out research credits/dissertations; capture 2–3 active lecture courses.
4. **Recent Awards & Accolades**: Fellowships, NSF CAREER awards, society honors.
5. **Cold Email Instructions**: Look for explicit PI guidance on how to reach out (`send CV`, `subject line`, `prospective student`, `statement of interest`).
6. **Direct Google Scholar User ID**: Search for 12-character ID strings matching `user=([a-zA-Z0-9_-]{12})`.

### Step 5: Deep Lab Website Crawling & Intelligence (Stage 4)
If a faculty member has a personal or lab website (`sites.google.com`, lab subdomains, or external URLs):
1. Visit the lab homepage and discover internal subpages (`/publications`, `/openings`, `/join`, `/research`, `/facilities`, `/equipment`).
2. Extract rich outreach intelligence:
   - **Actively Hiring / Openings**: Live statements seeking PhD, MS, or undergraduate students.
   - **Target Skills / Prerequisites**: Programming languages (`Python`, `C++`), frameworks (`PyTorch`, `ROS/ROS2`), or foundational math (`Linear Algebra`, `CFD`).
   - **Lab Facilities & Experimental Equipment**: Hardware, testbeds, and setups (Wind Tunnel, Towing Tank, PIV, AFM, GPU cluster, 3D printing).
   - **Funding Sponsors**: Federal/industrial sponsors (*NSF, NASA, ONR, DARPA, AFOSR, DOE*).
   - **Code Repositories**: Open-source GitHub, GitLab, or Bitbucket project links.

### Step 6: Academic Intel via OpenAlex API (Stage 5)
Leverage the OpenAlex API using the active API key to extract publication intelligence without bot blocks:
1. **OpenAlex Research Topics**: Query the author's primary topics and format with publication counts:
   - Example: `Fluid Dynamics and Heat Transfer (66) | Fluid Dynamics and Turbulent Flows (27) | Particle Dynamics in Fluid Flows (27)`
2. **Top 3 Cited Papers (Landmark Research)**:
   - Retrieve top 3 works sorted by `cited_by_count:desc`.
   - Format with paper title, journal/venue name, publication year, citation count, and direct clickable DOI link (`[🔗 DOI Link](https://doi.org/...)`).
3. **Top 3 Recent Papers (2024–2026)**:
   - Retrieve works filtered by `publication_year:2024-2026` sorted by year descending.
   - Format with paper title, journal/venue name, year, and direct clickable DOI link.
4. **Disambiguation Rule**: Cross-reference the author's institutions with the university name and filter topics against aerospace/mechanical keywords to prevent mismatching namesakes.

### Step 7: Dual Output Generation & Git Synchronization (Stage 6 & 7)
1. **Excel Workbook (`<slug>_aerospace_mechanical_faculty.xlsx`)**:
   - Sheet 1: `Field Matched` (sorted descending by `Matched Count`).
   - Sheet 2: `All Faculty` (complete cohort, sorted descending by `Matched Count`).
   - Write all 33 dynamic columns using `=HYPERLINK(...)` formulas and OpenPyXL `Hyperlink` styles.
2. **Markdown Directory (`<slug>_aerospace_mechanical_faculty.md`)**:
   - Interactive Quick Directory Index with clickable anchor bookmarks (`[Professor Name](#anchor)`).
   - Visual indicator badges: 🔥 **Hiring**, 📩 **Cold Email**, 📄 **Paper**, 🔬 **Lab**.
   - Structured numbered lists for papers with embedded `[🔗 DOI Link]` buttons.
   - Return-to-top buttons on every profile (`[⬆️ Back to Top]`).
3. **Commit & Push to GitHub**:
   - Synchronize all code, spreadsheets, and markdown documentation to GitHub repository under user `ksv-ai`.

