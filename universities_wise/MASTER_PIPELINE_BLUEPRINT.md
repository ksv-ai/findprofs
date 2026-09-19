# Autonomous University Faculty & Lab Intelligence Pipeline
## Standardized Master Operational Guide & Blueprint

> **Reference Implementation**: `universities_wise/arizona_state_university/`  
> **Repository Target**: `ksv-ai/findprofs`  
> **Document Version**: 2.0 (Dual Recent Flagship Architecture, 2023–2026 Focus)

---

## 1. Executive Summary & Core Engineering Philosophy

This blueprint documents the exact architectural design, data pipelines, heuristics, schemas, and scraping protocols used to construct the authoritative faculty and laboratory intelligence database for Arizona State University (SEMTE — Aerospace & Mechanical Engineering).

Any automated AI coding agent, research assistant, or software engineer can read this document to replicate this exact pipeline for any other institution (e.g., Purdue, Georgia Tech, University of Michigan, UIUC, Texas A&M, Stanford, MIT).

### Non-Negotiable Operational Rules:
1. **100% Authentic, Real Data Only (Zero Fabrication)**:
   - Every author ID, paper title, DOI, citation count, course code, lab URL, and office location must originate from verified university directories, official lab sites, or authoritative bibliographic APIs (OpenAlex, Crossref, Semantic Scholar, Springer, Elsevier).
   - If an office number, lab link, or phone is unavailable, leave the field empty (`""`). Never fabricate or guess.
2. **Strict Tier Scoping (Tier 1 & Tier 2 + Computational Math Only)**:
   - **Tier 1 (Core Aero / Fluids / CFD / Propulsion / Combustion / Computational Math)**: Direct numerical simulation, large eddy simulation, turbulence modeling, hypersonics, compressible flow, shock waves, aerothermodynamics, vortex dynamics, and numerical analysis of flow PDEs.
   - **Tier 2 (Thermal Sciences & Energy)**: Heat transfer, phase change, micro-reactors, thermal management, thermoelectrics, energy storage.
   - **Strict Drop List (Filtered Out Early)**: Pure robotics, drone navigation, autonomous driving, solid mechanics/composites without fluid coupling, biomedical devices, manufacturing, and civil engineering.
3. **No Intermediate CSV or JSON Spreadsheets**:
   - The primary user deliverables must strictly be a stylized, multi-sheet Excel workbook (`.xlsx`) and an interactive, linked Markdown guide (`.md`).
4. **Active Hyperlink Formulas**:
   - Every URL and email address in Excel must be rendered using dynamic `=HYPERLINK("...", "...")` formulas with Calibri 11pt blue underline formatting (`#0563C1`).

---

## 2. Workspace File & Directory Layout

Each university pipeline is self-contained inside `universities_wise/<university_slug>/`:

```
universities_wise/
├── arizona_state_university/
│   ├── asu_profs.py                               # Complete executable pipeline script
│   ├── run.log                                    # Consolidated execution & audit log
│   ├── asu_aerospace_mechanical_faculty.xlsx      # Stylized 48-column multi-sheet Excel workbook
│   ├── asu_aerospace_mechanical_faculty.md        # Interactive Markdown dossier
│   └── openalex_cache/                            # Authoritative OpenAlex JSON cache
│       ├── alberto_scotti.json
│       ├── gokul_pathikonda.json
│       ├── jeonglae_kim.json
│       ├── kangping_chen.json
│       ├── kiran_ramesh.json
│       ├── leixin_ma.json
│       ├── marcus_herrmann.json
│       ├── mohamed_houssem_kasbaoui.json
│       ├── ronald_calhoun.json
│       ├── ryan_milcarek.json
│       └── yulia_peet.json
└── MASTER_PIPELINE_BLUEPRINT.md                   # This master documentation file
```

---

## 3. Detailed Step-by-Step Implementation Workflow

```
[University Faculty Directory / API]
           │
           ▼
[Step 1: Active Faculty Discovery & Verification]
           │
           ▼
[Step 2: Early Tier 1/2 Scoping Heuristic] ─── (Drop Tier 3/4 profiles immediately)
           │
           ▼
[Step 3: Primary Profile & Deep Lab Website Extraction]
           │
           ▼
[Step 4: OpenAlex API Intelligence & JSON Cache (5 Recent Works 2023–2026)]
           │
           ▼
[Step 5: Four Cold Outreach Pillars Synthesis (Dual Flagship Full Treatment)]
           │
           ├── Pillar 1: Research Hook (Synthesized across 4–5 recent papers)
           ├── Pillar 2: Dual Recent Flagship Papers (2020–2026, Core Aero/CFD)
           │             ├── Flagship 1 Title, DOI, Abstract, Tripartite Finding
           │             └── Flagship 2 Title, DOI, Abstract, Tripartite Finding
           ├── Pillar 3: Tech Stack (Synthesized across 4–5 recent papers)
           └── Pillar 4: Dedicated Tripartite Physical Findings (Both papers)
           │
           ▼
[Step 6: Multi-Sheet Excel Generation (48 Columns, Dynamic Hyperlinks)]
           │
           ▼
[Step 7: Interactive Markdown Guide Generation (Clickable DOI & Abstract Cards)]
           │
           ▼
[Step 8: Execution Telemetry to run.log & GitHub Push to ksv-ai/findprofs]
```

---

## 4. Phase 1: Directory Harvesting & Early Tier Dropping

### 1. Intercepting the Directory Endpoint
Instead of parsing complex, dynamically loaded HTML tables, inspect network traffic to locate the university’s internal JSON REST endpoint.
- **ASU Endpoint**: `https://search.asu.edu/api/v1/webdir-profiles/departments/SEMTE/faculty`
- **Output**: 55 raw faculty candidate objects.

### 2. Active Faculty Filter (Rejecting Non-Tenure Staff)
Every candidate's appointment titles and affiliations are evaluated against an exclusion blocklist:
```python
EXCLUDED_KEYWORDS = [
    "emeritus", "retired", "adjunct", "visiting", "lecturer", "staff",
    "postdoc", "courtesy", "administrative", "coordinator", "advisor",
    "manager", "instructor", "emerita"
]
```
Any profile containing these titles is immediately discarded.

### 3. Early Dropping Heuristic
To avoid unnecessary network requests, filter the roster **immediately after harvesting**:
- **Tier 1 Regex Ontology**:
  ```python
  TIER_1_AERO_TERMS = [
      r'\bfluid dynamics\b', r'\bcfd\b', r'\bcomputational fluid dynamics\b',
      r'\bfluid mechanics\b', r'\bturbulence\b', r'\bturbulent\b',
      r'\bdirect numerical simulation\b', r'\bdns\b', r'\blarge eddy simulation\b', r'\bles\b',
      r'\baerodynamics\b', r'\baerodynamic\b', r'\bhypersonic\b', r'\bsupersonic\b',
      r'\bcompressible flow\b', r'\bshock waves\b', r'\bairfoil\b', r'\bpropulsion\b',
      r'\bcombustion\b', r'\bmultiphase flow\b', r'\bparticle dynamics in fluid\b',
      r'\bboundary layer\b', r'\bvortex\b', r'\bflow control\b', r'\bwind energy\b'
  ]
  ```
- **Tier 2 (Thermal)**: `heat transfer`, `thermal management`, `thermodynamics`, `energy systems`.
- **Dropped Cohort**: Pure robotics (Tier 4) and pure materials/manufacturing (Tier 3) are dropped right away.
- **ASU Result**: 30 profiles dropped; **18 retained** (11 Tier 1 + 7 Tier 2).

---

## 5. Phase 2: Deep Profile & Lab Website Extraction

For each retained professor, execute deep web scraping using `cloudscraper`:

1. **Official Directory Profile (`https://search.asu.edu/profile/<slug>`)**:
   - Extract building & room number (`Office Location`).
   - Extract degrees, institutions, and graduation years (`Education / Degrees`).
   - Extract catalog courses taught (`Courses Taught`).
   - Extract full research bio statement (`Research / Bio Summary`).
   - Discover personal, lab, or Google Sites links.
2. **Deep Lab Website Scraping (`scrape_deep_lab_site`)**:
   - Discover internal subpages (`/join`, `/openings`, `/research`, `/publications`, `/facilities`).
   - **Actively Hiring / Openings**: Regex match funding announcements (e.g. graduate assistantships, fellowships).
   - **Cold Email Instructions**: Extract explicit PI instructions for applicants.
   - **Target Skills**: Identify required tools (e.g., Python, C++, OpenFOAM, PIV).
   - **Funding Sponsors**: Match agencies (`NSF`, `NASA`, `ONR`, `AFOSR`, `DOE`, `DARPA`).
   - **Code Repositories**: Extract GitHub, GitLab, and Bitbucket URLs.

---

## 6. Phase 3: OpenAlex API Integration & Standardized Cache

For each Tier 1 Core Aero professor, query OpenAlex (`https://api.openalex.org/authors`):

1. **Author Resolution**:
   Match candidate names while verifying institution affiliation (`Arizona State University`) and concept overlap to avoid wrong namesakes.
2. **Authoritative JSON Schema (`openalex_cache/<slug>.json`)**:
   - `author_id`, `author_display_name`, `works_count`, `cited_by_count`.
   - `top_topics`: List of top 5 topics with paper counts.
   - `top_cited_works`: Top 3 landmark historical papers with cites, journal venues, DOIs, and abstracts.
   - `recent_works`: **5 recent papers from 2023–2026** with reconstructed abstracts, DOIs, and venues.
3. **Abstract Reconstitution**:
   Reconstruct linear abstract text from OpenAlex's `abstract_inverted_index`.
4. **Recent Works Query Window (2023–2026)**:
   ```
   https://api.openalex.org/works?filter=author.id:{auth_id},publication_year:2023-2026&sort=publication_date:desc&per_page=5
   ```

---

## 7. Phase 4: The Four Cold Outreach Pillars (Dual Flagship Architecture)

### Pillar 1: Research Hook (Synthesized Across 4–5 Recent Papers)
- **Rule**: 1–2 sentences opening the email after the salutation. Demonstrates active understanding of the professor's current trajectory (2023–2026).
- **Formula**:
  $$\text{Research Hook} = \mathbf{[Primary\ Method\ /\ Numerical\ Scheme]} + \mathbf{[Flow\ Regime\ /\ Physics]} + \mathbf{[Target\ Engineering\ Outcome]}$$

### Pillar 2: Dual Recent Flagship Papers (2020–2026)
- **Selection**: 2 landmark original research papers published between 2020 and 2026 closely tied to core aero/fluids/CFD.
- **Requirements**: Direct clickable DOIs (`https://doi.org/...`) and complete unabridged scientific abstracts.

### Pillar 3: Tech Stack (Synthesized Across 4–5 Recent Papers)
- **Definition**: Exact numerical solvers, codes, algorithms, and experimental rigs actively deployed across the 2023–2026 papers (e.g., `OpenFOAM`, `Nek5000`, `VF-IBM`, `Stereo PIV`).

### Pillar 4: Dedicated Tripartite Physical Findings for Both Flagship Papers
Formulated individually for **both Flagship 1 and Flagship 2**:
$$\text{Regime} \longrightarrow \text{Physical Mechanism} \longrightarrow \text{Engineering Consequence}$$
1. **Part 1 `[ENGINE]`**: Active methodology / solver (opens with gerund: `performing`, `coupling`, `deploying`).
2. **Part 2 `[ARENA]`**: Specific flow physics and geometry.
3. **Part 3 `[PAYOFF]`**: Root physical mechanism + **hard quantitative benchmark** (`35%`, `3.5 dB`, `15.8 kHz`, `Re_T^0.42`).

---

## 8. Phase 5: Standardized 48-Column Dataset Specification

The Excel workbook is structured with an explicit **48-column schema**:

| Col # | Column Header | Description |
| :---: | :--- | :--- |
| 1 | `Name` | Faculty full name |
| 2 | `University` | Institution name |
| 3 | `Profile URL` | Official university directory profile page (hyperlinked) |
| 4 | `Google Scholar URL` | Direct Scholar URL with `user=<id>` or targeted search |
| 5 | `Job Title` | Academic rank (Professor, Associate Professor, Assistant Professor) |
| 6 | `Department` | Department / School name (Aerospace & Mechanical Engineering) |
| 7 | `Scholar ID` | Direct Google Scholar 12-character User ID |
| 8 | `Email` | Hyperlinked email address (`mailto:`) |
| 9 | `Research Tier` | Authoritative tier (Tier 1: Core Aero / Fluids / Comp Math, Tier 2: Thermal / Energy) |
| 10 | `Research Category` | Formatted tier badge and domain description |
| 11 | `Matched Count` | Integer count of matching research fields (primary sorting key) |
| 12 | `Matched Fields` | Comma-separated list of matched field keywords |
| 13 | `Research Hook` | **Pillar 1**: Synthesized from the PI's primary method, flow regime, and target engineering outcome |
| 14 | `Tech Stack` | **Pillar 3**: Exact numerical solvers, codes, or experimental rigs synthesized across recent papers |
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
| 27 | `Recent Papers (2023-2026)` | ~5 recent papers with journal, year & clickable DOIs |
| 28 | `Top Cited Papers` | Landmark papers with journal, year, cites & clickable DOIs |
| 29 | `Courses Taught` | Filtered lecture courses taught |
| 30 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER |
| 31 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails |
| 32 | `OpenAlex Research Topics` | Top 3 research topics with publication counts from OpenAlex |
| 33 | `Google Scholar Tags` | Extracted Google Scholar / OpenAlex research interest tags |
| 34 | `Research Interests` | Specific research topic tags |
| 35 | `Expertise Areas` | High-level research domain taxonomy |
| 36 | `Research / Bio Summary` | Bio summary or research focus paragraph |
| 37 | `Education / Degrees` | Degrees, institutions, and graduation years |
| 38 | `Lab / Research Group Name` | Official research lab or group title |
| 39 | `Lab / Personal Website` | Hyperlinked personal or lab homepage |
| 40 | `Actively Hiring / Openings` | Recruitment announcements extracted from lab websites |
| 41 | `Target Skills / Prerequisites` | Required skills/languages (Python, C++, OpenFOAM, etc.) |
| 42 | `Lab Facilities & Equipment` | Experimental setups, facilities & hardware |
| 43 | `Funding Sponsors` | Federal/industrial sponsors (NSF, NASA, ONR, AFOSR, etc.) |
| 44 | `Software / Code Repo` | Open-source GitHub/Bitbucket/GitLab repositories |
| 45 | `Latest Project / Highlight` | Project banner, latest headline, or paper announcement |
| 46 | `Office Location` | Building and room number |
| 47 | `Is Field Match` | Boolean (`TRUE` / `FALSE`) |
| 48 | `Directory URL` | Source university directory URL (at the end of every row) |

### Sheet Structure:
- **Sheet 1 (`Aero Focus`)**: Only Tier 1 Core Aero/Fluids/CFD professors (11 professors).
- **Sheet 2 (`Field Matched`)**: All qualifying Tier 1 and Tier 2 professors (18 professors, sorted descending by matched count).
- **Sheet 3 (`All Faculty`)**: Complete active qualifying cohort (18 professors).

---

## 9. Phase 6: Markdown Dossier Specification

The markdown document `<slug>_aerospace_mechanical_faculty.md` must render:
1. **Quick Jump Anchor Index**: Hyperlinked list of all faculty.
2. **Tier Summary Breakdown**: Tables summarizing Tier 1 and Tier 2 cohorts.
3. **Dedicated Professor Cards**:
   - Directory, Scholar, Lab, Email, and Repo quick badges.
   - **Pillar 1 Research Hook & Pillar 3 Tech Stack**.
   - **Dedicated Flagship Paper 1 Card**: Title, direct DOI, Tripartite Finding 1, and full Paper 1 Abstract blockquote.
   - **Dedicated Flagship Paper 2 Card**: Title, direct DOI, Tripartite Finding 2, and full Paper 2 Abstract blockquote.
   - 5 Recent Papers (2023–2026) with clickable `[🔗 DOI Link]` formulas.
   - 3 Top Cited Papers with citation metrics.
   - Lab Openings and application instructions.

---

## 10. Phase 7: Logging Telemetry & GitHub Push

1. **Logging**: All events, dropped profile names with reasons, and the final 48-column fill audit table must be logged directly to `run.log`.
2. **GitHub Synchronization**:
   ```powershell
   git add .
   git commit -m "feat(asu): implement dual flagship papers with dedicated tripartite findings, complete abstracts, and explicit Excel columns"
   git push origin master
   ```

---

## 11. How to Replicate for Any New University (e.g. Purdue)

When replicating this system for Purdue or any subsequent university:
1. **Create Directory**: `universities_wise/purdue_university/`.
2. **Roster Extraction**: Identify the faculty API or roster for the School of Aeronautics & Astronautics (AAE) and School of Mechanical Engineering (ME).
3. **Apply Early Dropping**: Drop pure robotics, manufacturing, civil, and materials faculty right after discovery.
4. **Fetch OpenAlex Cache**: Query OpenAlex for qualifying Tier 1 PIs, extracting top topics, 3 cited works, and **5 recent papers from 2023–2026**.
5. **Formulate 4 Pillars**: Draft recent-paper research hooks, select 2 Flagship Papers (2020–2026) with direct DOIs, identify modern tech stacks, and write dedicated tripartite findings for **both** papers.
6. **Generate Outputs**: Export the 48-column `.xlsx` workbook and `.md` reference guide.
7. **Verify & Push**: Confirm `run.log` shows 100% active discovery and push to GitHub `ksv-ai/findprofs`.
