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
2. **Strict Tier-Filtered Scraping (Tier 1 & Tier 2 Focus Only + Computational Math)**:
   - Scrape and enrich **only** Tier 1 (Core Aero / Fluids / CFD / Turbulence / Hypersonics / Propulsion / Combustion / Aerothermodynamics) and Tier 2 (Thermal Sciences / Heat Transfer / Energy Systems) faculty.
   - Do **NOT** scrape or retain faculty outside Tiers 1 and 2 (e.g., pure robotics, pure manufacturing, pure civil, biomedical, or structural mechanics not coupled to aero/fluids/thermal).
   - **Cross-Departmental Computational Mathematics**: Actively include faculty in Mathematics, Applied Mathematics, or Scientific Computing whose research focuses on computational fluid dynamics (CFD), high-order PDE solvers, turbulence modeling, finite element/spectral methods, or numerical flow physics.
3. **5 Recent Papers & Dual Recent Flagship Papers (Aero/CFD/Fluids Focused)**:
   - Extract **~5 recent papers** (2024–2026 / latest available) rather than only 3.
   - Select **2 Flagship Papers** strictly from among recent, high-impact publications (2020–2026) that are closely tied to core aero / fluids / CFD physics.
   - Both flagship papers must have valid, clickable direct DOIs and abstracts.
4. **Recent-Paper-Driven Research Hook & Tech Stack**:
   - **Research Hook Formulation**: Must be synthesized across the body of **4–5 recent papers** (capturing current active grants and modern directions) using the exact formulation:
     $$\text{Research Hook} = \mathbf{[Primary\ Method\ /\ Numerical\ Scheme]} + \mathbf{[Flow\ Regime\ /\ Physics]} + \mathbf{[Target\ Engineering\ Outcome]}$$
   - **Tech Stack**: Extracted from the collective toolsets, solvers, codes, and diagnostics used across the **4–5 recent papers** (e.g., specific solvers like OpenFOAM, Nek5000, SU2, in-house high-order DG, PIV, CARS), ensuring you speak to what the lab is actively running today.
5. **Preserved API Intelligence**:
   - All raw API extractions from OpenAlex for Tier 1 core aero and computational math faculty are preserved in `openalex_cache/<slug>.json` for complete reproducibility, auditability, and downstream cold email generation.
6. **Strict Active Faculty Verification (Zero Emeritus / Retired Faculty)**:
   - Always inspect ALL candidate title fields, appointment lists, affiliations, and subaffiliations.
   - Reject any profile containing: `emeritus`, `retired`, `adjunct`, `visiting`, `lecturer`, `instructor`, `postdoc`, `courtesy`, or `staff`.
7. **Keyword Matching & Ranking (`fields.txt`)**:
   - Extract research keywords from `fields.txt` across Turbulence, CFD, Fluids, Thermal/Heat Transfer, Propulsion, Combustion, Scramjets, Hypersonics, and Computational Mathematics.
   - Excel sheets must be sorted with high-priority fluids/CFD faculty prominently positioned (`Matched Count` or `Research Tier`).
8. **Active Clickable Excel Hyperlinks**:
   - Every URL and email must use `=HYPERLINK("...", "...")` formulas and OpenPyXL `Hyperlink` styles so they work seamlessly in Microsoft Excel, Google Sheets, and LibreOffice.
9. **Authentic, Real Data Only**:
   - Never fabricate data. If a faculty member does not have a lab website or office number, leave the cell empty.
10. **Automatic GitHub Synchronization**:
   - After code or dataset modifications, commit and push to GitHub repository under user `ksv-ai`.

---

## 2. Standardized Dataset Schema (Cold Outreach Architecture)

Every university extraction pipeline outputs an Excel workbook with clean sheets:
1. **`Aero Focus`**: Only professors working strictly in Tier 1 Core Aero, Fluids, CFD, Turbulence, Hypersonics, Propulsion, Combustion, and Computational Math.
2. **`Field Matched`**: All qualifying Tier 1 and Tier 2 professors with `Matched Count > 0`, sorted descending.
3. **`All Faculty`**: All qualifying Tier 1 and Tier 2 verified active faculty, sorted descending by matched count.

### Column Specification:

| Col # | Column Header | Description |
| :---: | :--- | :--- |
| 1 | `Name` | Faculty full name |
| 2 | `University` | Institution name |
| 3 | `Profile URL` | Official university directory profile page (hyperlinked) |
| 4 | `Google Scholar URL` | Direct Scholar URL with `user=<id>` or targeted search |
| 5 | `Job Title` | Academic rank (Professor, Associate Professor, Assistant Professor) |
| 6 | `Department` | Department / School name (including Aerospace, MechE, and Computational Math) |
| 7 | `Scholar ID` | Direct Google Scholar 12-character User ID |
| 8 | `Email` | Hyperlinked email address (`mailto:`) |
| 9 | `Research Tier` | Authoritative tier (Tier 1: Core Aero / Fluids / Comp Math, Tier 2: Thermal / Energy) |
| 10 | `Research Category` | Formatted tier badge and domain description |
| 11 | `Matched Count` | Integer count of matching research fields (primary sorting key) |
| 12 | `Matched Fields` | Comma-separated list of matched field keywords |
| 13 | `Flagship Paper Hook` | **Pillar 2**: Landmark recent paper titles (2 recent flagship papers, 2020–2026) with journal & year |
| 14 | `Flagship Paper DOI` | **Pillar 2 DOI**: Direct, clickable DOI hyperlinks for the 2 recent flagship papers |
| 15 | `Tech Stack` | **Pillar 3**: Exact numerical solvers, codes, or experimental rigs synthesized across the 4–5 recent papers |
| 16 | `Physical Finding` | **Pillar 4**: Tripartite structure (`[gerund solver] to investigate [geometry] demonstrating [causality + hard number]`) |
| 17 | `Research Hook` | **Pillar 1**: Synthesized from the PI's primary method, flow regime, and target engineering outcome across 4–5 recent papers |
| 18 | `Latest Paper / Publication` | Most recent research paper title (cold email hook) |
| 19 | `Recent Papers (2024-2026)` | ~5 recent papers with journal, year & clickable DOIs |
| 20 | `Top Cited Papers` | Landmark papers with journal, year, cites & clickable DOIs |
| 21 | `Courses Taught` | Filtered lecture courses taught |
| 22 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER |
| 23 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails |
| 24 | `OpenAlex Research Topics` | Top 3 research topics with publication counts from OpenAlex |
| 25 | `Google Scholar Tags` | Extracted Google Scholar / OpenAlex research interest tags |
| 26 | `Research Interests` | Specific research topic tags |
| 27 | `Expertise Areas` | High-level research domain taxonomy |
| 28 | `Research / Bio Summary` | Bio summary or research focus paragraph |
| 29 | `Education / Degrees` | Degrees, institutions, and graduation years |
| 30 | `Lab / Research Group Name` | Official research lab or group title |
| 31 | `Lab / Personal Website` | Hyperlinked personal or lab homepage |
| 32 | `Actively Hiring / Openings` | Recruitment announcements extracted from lab websites |
| 33 | `Target Skills / Prerequisites` | Required skills/languages (Python, C++, OpenFOAM, etc.) |
| 34 | `Lab Facilities & Equipment` | Experimental setups, facilities & hardware |
| 35 | `Funding Sponsors` | Federal/industrial sponsors (NSF, NASA, ONR, AFOSR, etc.) |
| 36 | `Software / Code Repo` | Open-source GitHub/Bitbucket/GitLab repositories |
| 37 | `Latest Project / Highlight` | Project banner, latest headline, or paper announcement |
| 38 | `Office Location` | Building and room number |
| 39 | `Is Field Match` | Boolean (`TRUE` / `FALSE`) |
| 40 | `Directory URL` | Source university directory URL (at the end of every row) |

---

## 3. Core Aero / Fluids Focus Filtering Protocol

To prevent scraping noisy, irrelevant profiles (robotics, materials science, manufacturing, biomedical) into the OpenAlex cache and cold email queue, enforce the **Core Aero Filter**:

### 3.1 Qualifying Research Areas
A professor qualifies for OpenAlex JSON cache extraction and the `Aero Focus` tab if their profile matches at least one (or two) core aerospace/fluid dynamics paradigms:
- **CFD & Turbulence**: Direct Numerical Simulation (DNS), Large Eddy Simulation (LES), RANS, turbulent shear flows, boundary layer transition, vortex dynamics.
- **Aerodynamics & Gas Dynamics**: High-speed aerodynamics, hypersonics, supersonics, shock waves, shock–boundary-layer interaction (SBLI), compressible/incompressible flow, airfoils/wings.
- **Multiphase & Complex Flows**: Multiphase flow, droplet/bubble dynamics, particle dynamics in fluid flows, granular flows.
- **Propulsion & Reacting Flows**: Combustion, flame dynamics, jet noise/acoustics, rotating detonation engines, scramjets, nozzles.
- **Experimental Fluids**: Particle Image Velocimetry (PIV, SPIV, Tomo-PIV), hot-wire anemometry, Schlieren, wind tunnel/water tunnel facilities.

### 3.2 Automated Filter Logic
```python
import re

CORE_AERO_TERMS = [
    r'\bcomputational fluid dynamics\b', r'\bcfd\b', r'\bfluid dynamics\b',
    r'\bfluid mechanics\b', r'\bturbulence\b', r'\bturbulent\b',
    r'\baerodynamics\b', r'\baerodynamic\b', r'\bmultiphase flow\b', r'\bmultiphase\b',
    r'\bcombustion\b', r'\bpropulsion\b', r'\bhypersonic\b', r'\bsupersonic\b',
    r'\btransonic\b', r'\bdirect numerical simulation\b', r'\bdns\b',
    r'\blarge eddy simulation\b', r'\bboundary layer\b', r'\bvortex\b', r'\bvortices\b',
    r'\bflow control\b', r'\bshear flow\b', r'\bcompressible flow\b', r'\bshock waves\b',
    r'\bwind and air flow\b', r'\bwind energy\b', r'\baeroelasticity\b',
    r'\bparticle dynamics in fluid\b', r'\biomimetic flight\b'
]
COMPILED_AERO = [re.compile(p, re.IGNORECASE) for p in CORE_AERO_TERMS]

def is_core_aero_prof(prof_dict: dict) -> bool:
    """Returns True ONLY if professor's profile text contains verified aero/fluids keywords."""
    text = " | ".join([
        str(prof_dict.get("Matched Fields", "")),
        str(prof_dict.get("Research Interests", "")),
        str(prof_dict.get("Research / Bio Summary", "")),
        str(prof_dict.get("Lab / Research Group Name", "")),
    ])
    hits = [p.pattern.replace(r'\b', '') for p in COMPILED_AERO if p.search(text)]
    return len(hits) >= 1  # Strictly gate OpenAlex extraction
### 3.3 Authoritative OpenAlex JSON Cache Schema (`openalex_cache/<slug>.json`)
Every cached JSON file must adhere to this complete, standardized schema matching the ASU reference standard and capturing full academic impact metrics:
```json
{
  "name": "Marcus Herrmann",
  "uni": "Arizona State University",
  "author_id": "A5009928604",
  "author_display_name": "Marcus Herrmann",
  "works_count": 168,
  "cited_by_count": 2685,
  "2yr_mean_citedness": 1.6,
  "h_index": 24,
  "i10_index": 42,
  "affiliations": [
    "University of Stuttgart",
    "Infineon Technologies (Germany)",
    "University of Freiburg"
  ],
  "top_topics": [
    {
      "topic": "Fluid Dynamics and Heat Transfer",
      "count": 66
    },
    {
      "topic": "Fluid Dynamics and Turbulent Flows",
      "count": 27
    }
  ],
  "top_cited_works": [
    {
      "title": "Modeling Primary Atomization",
      "publication_year": 2008,
      "publication_date": "2008-01-01",
      "doi": "https://doi.org/10.1146/annurev.fluid.40.111406.102200",
      "venue": "Annual Review of Fluid Mechanics",
      "type": "review",
      "cited_by_count": 440,
      "is_oa": false,
      "oa_url": "",
      "concepts": ["Direct numerical simulation", "Multiphase flow", "Breakup"],
      "abstract": "Full reconstructed abstract from OpenAlex inverted index...",
      "authors": ["Mikhael Gorokhovski", "Marcus Herrmann"]
    }
  ],
  "recent_works": [
    {
      "title": "Recent publication title 2024-2026...",
      "publication_year": 2025,
      "publication_date": "2025-01-20",
      "doi": "https://doi.org/10.1016/j.jcp.2025.113765",
      "venue": "Journal of Computational Physics",
      "type": "article",
      "cited_by_count": 2,
      "is_oa": false,
      "oa_url": "",
      "concepts": ["Immersed boundary method", "Turbulence"],
      "abstract": "Full reconstructed abstract...",
      "authors": ["Himanshu Dave", "Marcus Herrmann"]
    }
  ]
}
```
## 3. Scope & Filtering Protocol (Tier 1, Tier 2 & Computational Math Only)

To prevent scraping noisy or non-relevant faculty profiles:
- **Eligible Tiers**: Only harvest, enrich, and export faculty classified as:
  - **Tier 1**: Core Aerospace, Fluid Dynamics, CFD, Turbulence, Hypersonics, Aerodynamics, Multiphase, Combustion, Propulsion, Scramjets, and **Computational Mathematics / Numerical Analysis of PDEs / Scientific Computing for Fluids**.
  - **Tier 2**: Thermal Sciences, Heat Transfer, Multiphase Heat Exchange, and Energy Systems.
- **Ineligible Faculty**: Reject and do not harvest professors in pure robotics, autonomous driving, solid mechanics/structures without aero/fluid coupling, biomedical, manufacturing, or materials science.

### 3.1 Qualifying Research Areas & Computational Mathematics
- **CFD & Turbulence**: DNS, LES, RANS, turbulent shear flows, boundary layer transition, vortex dynamics.
- **Aerodynamics & Gas Dynamics**: High-speed aerodynamics, hypersonics, supersonics, shock waves, shock–boundary-layer interaction (SBLI), compressible flow, scramjets, aerothermodynamics.
- **Propulsion & Combustion**: Detonation, rotating detonation engines (RDE), turbulent reacting flows, flame instability, rocket propulsion, plasma-assisted combustion.
- **Computational Mathematics & Scientific Computing**: High-order finite difference/volume, Discontinuous Galerkin (DG), spectral element methods (Nek5000), structure-preserving integrators, kinetic solvers (LBM/Boltzmann), adaptive mesh refinement (AMR) for fluid flow PDEs.
- **Multiphase & Complex Flows**: Droplet atomization, cavitation, bubble dynamics, particle-laden turbulent flows.

### 3.2 Tier Classification Hierarchy
- **Tier 1 (Core Aero / Fluids / CFD / Propulsion / Computational Math)**: Direct aerospace engineering, fluid dynamics, aero-propulsion, aerothermodynamics, hypersonics, or scientific computing/computational mathematics explicitly applied to flow equations.
- **Tier 2 (Thermal Sciences & Energy)**: Heat transfer, thermal management, phase change, electronic cooling, combustion/energy systems without deep aero focus.

---

## 4. Cold Outreach Intelligence Synthesis Architecture

### 4.1 Pillar 1: Research Hook (Synthesized from 4–5 Recent Papers)
- **Purpose**: Opens the email immediately after the salutation. Demonstrates active understanding of the professor's current research trajectory and modern publications.
- **Rule**: 1–2 sentences, curiosity-driven, forward-looking, no proper nouns (no professor name, no paper titles, no university name).
- **Formula**:
  $$\text{Research Hook} = \mathbf{[Primary\ Method\ /\ Numerical\ Scheme]} + \mathbf{[Flow\ Regime\ /\ Physics]} + \mathbf{[Target\ Engineering\ Outcome]}$$
- **Template Frame**:
  `"[Field-level phenomenon / open challenge] — [what makes it fundamentally hard or intractable] — [what this group's approach addresses across recent work]."`

### 4.2 Pillar 2: Dual Recent Flagship Papers (2020–2026, Core Aero/CFD/Fluids Focused)
Select **2 Flagship Papers** strictly from among recent, high-impact publications (2020–2026) that are closely tied to core aero / fluids / CFD physics.
Each flagship paper must pass 4 strict filters:
1. **Recency Window**: Published between 2020 and 2026.
2. **Subject Filter**: Fluid dynamics / CFD / aero keyword score $\ge 2$ in title + concepts.
3. **Article Type Filter**: Must be primary original research (exclude `review`, `survey`, `overview`, `book-chapter`, `editorial`, `erratum`).
4. **DOI Verification**: Direct clickable link (`https://doi.org/...`) verified via OpenAlex / Crossref.

### 4.3 Pillar 3: Tech Stack Extraction (Synthesized Across 4–5 Recent Papers)
- **Definition**: A concise, comma-separated list of the computational solvers, numerical algorithms, or experimental tools actually deployed across the **4–5 recent papers**.
- **Categories**:
  - *CFD Solvers & Frameworks*: `OpenFOAM (LES)`, `Nek5000 (spectral-element DNS)`, `SU2`, `In-house high-order DG solver`.
  - *Turbulence & Multiphase Methods*: `Refined Level Set Grid (RLSG)`, `Volume of Fluid (VOF)`, `Direct Numerical Simulation (DNS)`, `Wall-modeled LES (WMLES)`.
  - *Experimental Diagnostics*: `Stereo PIV`, `Dual-pump CARS`, `High-speed Schlieren`, `Shock tube facilities`.
- **Rules**: Max 3–4 tools, official naming format.

### 4.4 Pillar 4: Tripartite Physical Finding
Formulated from the recent flagship papers:
$$\text{Regime} \longrightarrow \text{Physical Mechanism} \longrightarrow \text{Engineering Consequence}$$
1. **Part 1 `[ENGINE]` — Active Methodology / Solver**: Opens with an active gerund (`performing`, `conducting`, `coupling`, `deploying`).
2. **Part 2 `[ARENA]` — Specific Flow Physics & Geometry**: Flow condition + geometry.
3. **Part 3 `[PAYOFF]` — Root Physical Mechanism & Hard Quantitative Benchmark**: Causality + quantitative metric (%, dB, St, Cf, Re_tau, Ma).

---

## 5. Playbook: Transferring the Pipeline to Any New University

Follow this standardized 7-step replication protocol for any new institution (e.g. Purdue, Georgia Tech, Michigan, UIUC, Texas A&M):

### Step 1: Project Setup & Workspace Isolation
1. Create directory: `universities_wise/<university_slug>/`.
2. Clean up any temporary `.csv` or tabular `.json` spreadsheets.
3. Import `COLUMNS_CONFIG` and `TARGET_KEYWORDS`.

### Step 2: Directory Architecture Discovery & Harvesting
1. Identify Aerospace Engineering & Mechanical Engineering faculty rosters.
2. Intercept JSON REST API or scrape server-side HTML directory cards.

### Step 3: Strict Active Faculty Verification
1. Reject: `emeritus`, `retired`, `adjunct`, `visiting`, `lecturer`, `instructor`, `postdoc`, `staff`.
2. Keep: `Assistant Professor`, `Associate Professor`, `Professor`, `Chaired Professor`, `Regents Professor`.

### Step 4: Primary Profile & Lab Website Intelligence
1. Profile Scraping: Office location, degrees, courses taught, awards, Google Scholar ID.
2. Lab Scraping: Active hiring statements, prerequisites (Python, C++, ROS, PyTorch), experimental facilities, funding sponsors, GitHub code repos.

### Step 5: Selective OpenAlex API Extraction (Aero Core Only)
1. Evaluate faculty against `is_core_aero_prof()`.
2. **Extract OpenAlex JSON only for qualifying aero faculty**; save compact structured JSON to `openalex_cache/<slug>.json`.
3. For core aero faculty, extract:
   - Top Research Topics (with publication counts).
   - Top 3 Cited Papers (with journal, year, cites, DOI).
   - Top 3 Recent Papers 2024–2026 (with journal, year, DOI).
   - Flagship paper, Tech Stack, and abstract for Tripartite Finding generation.

### Step 6: Multi-Sheet Excel & Markdown Generation
1. Build Excel workbook (`<slug>_aerospace_mechanical_faculty.xlsx`):
   - Sheet 1: `Aero Focus` (solely Core Aero/Fluids/CFD professors, ready for cold outreach).
   - Sheet 2: `Field Matched` (all active professors with matched keywords).
   - Sheet 3: `All Faculty` (complete cohort audit log).
2. Build Markdown directory (`<slug>_aerospace_mechanical_faculty.md`):
   - Quick jump index, visual indicator badges (🔥 Hiring, 📩 Cold Email, 📄 Paper, 🔬 Lab).
   - Clickable DOI links for landmark and recent publications.

### Step 7: Automatic GitHub Synchronization
- Commit all updated code, workbooks, markdown files, and curated cache to GitHub repository under user `ksv-ai`.
