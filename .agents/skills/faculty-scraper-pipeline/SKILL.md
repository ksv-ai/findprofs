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
2. **Selective OpenAlex Extraction (Core Aero / CFD / Fluid Mechanics Focus Only)**:
   - OpenAlex enrichment and local `openalex_cache/` JSON file extraction MUST strictly target professors whose research focus is in **Core Aero / Fluids / CFD / Turbulence / Hypersonics / Aerodynamics / Multiphase / Propulsion / Combustion**.
   - Non-aero faculty (pure robotics, materials science, manufacturing, biomedical, electronic packaging, civil/environmental) must NOT have OpenAlex cache files created. This keeps the cache and downstream cold email intelligence 100% focused on relevant faculty without noisy, irrelevant data.
   - In Excel, support a dedicated **`Aero Focus`** sheet (or tier-based prioritization) containing solely these core aerospace/fluids faculty.
3. **Preserved API Intelligence**:
   - All raw API extractions from OpenAlex for core aero faculty are preserved in `openalex_cache/<slug>.json` for complete reproducibility, auditability, and downstream cold email generation.
4. **Strict Active Faculty Verification (Zero Emeritus / Retired Faculty)**:
   - Always inspect ALL candidate title fields, appointment lists, affiliations, and subaffiliations.
   - Reject any profile containing: `emeritus`, `retired`, `adjunct`, `visiting`, `lecturer`, `instructor`, `postdoc`, `courtesy`, or `staff`.
5. **Keyword Matching & Ranking (`fields.txt`)**:
   - Extract research keywords from `fields.txt` across Turbulence, CFD, Fluids, Thermal/Heat Transfer, Robotics, Control, Autonomy, Materials, Structures, and Aerospace.
   - Excel sheets must be sorted with high-priority fluids/CFD faculty prominently positioned (`Matched Count` or `Research Tier`).
6. **Active Clickable Excel Hyperlinks**:
   - Every URL and email must use `=HYPERLINK("...", "...")` formulas and OpenPyXL `Hyperlink` styles so they work seamlessly in Microsoft Excel, Google Sheets, and LibreOffice.
7. **Authentic, Real Data Only**:
   - Never fabricate data. If a faculty member does not have a lab website or office number, leave the cell empty.
8. **Automatic GitHub Synchronization**:
   - After code or dataset modifications, commit and push to GitHub repository under user `ksv-ai`.

---

## 2. Standardized Dataset Schema (Cold Outreach Architecture)

Every university extraction pipeline outputs an Excel workbook with clean sheets:
1. **`Aero Focus`**: Only professors working strictly in Core Aero, Fluids, CFD, Turbulence, Hypersonics, and Propulsion.
2. **`Field Matched`**: All professors with `Matched Count > 0`, sorted descending.
3. **`All Faculty`**: Complete cohort of verified active faculty, sorted descending by matched count.

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
| 9 | `Research Tier` | Authoritative tier (Tier 1: Core Aero, Tier 2: Thermal, Tier 3: Structures, Tier 4: Robotics) |
| 10 | `Research Category` | Formatted tier badge and domain description |
| 11 | `Matched Count` | Integer count of matching research fields (primary sorting key) |
| 12 | `Matched Fields` | Comma-separated list of matched field keywords |
| 13 | `Flagship Paper Hook` | **Pillar 2**: Landmark paper title with journal, year & DOI |
| 14 | `Tech Stack` | **Pillar 3**: Exact numerical solvers, codes, or experimental rigs used |
| 15 | `Physical Finding` | **Pillar 4**: Tripartite structure (`[gerund solver] to investigate [geometry] demonstrating [causality + hard number]`) |
| 16 | `Research Hook` | **Pillar 1**: Broad curiosity-driven opening sentence connecting PI's research agenda |
| 17 | `Latest Paper / Publication` | Most recent research paper title (cold email hook) |
| 18 | `Recent Papers (2024-2026)` | 3 recent papers with journal, year & clickable DOI |
| 19 | `Top Cited Papers` | 3 landmark papers with journal, year, cites & clickable DOI |
| 20 | `Courses Taught` | Filtered lecture courses taught |
| 21 | `Recent Awards / Honors` | Major accolades, fellowships & NSF CAREER |
| 22 | `Cold Email / Application Instructions` | Explicit instructions given by PI for applicant emails |
| 23 | `OpenAlex Research Topics` | Top 3 research topics with publication counts from OpenAlex |
| 24 | `Google Scholar Tags` | Extracted Google Scholar / OpenAlex research interest tags |
| 25 | `Research Interests` | Specific research topic tags |
| 26 | `Expertise Areas` | High-level research domain taxonomy |
| 27 | `Research / Bio Summary` | Bio summary or research focus paragraph |
| 28 | `Education / Degrees` | Degrees, institutions, and graduation years |
| 29 | `Lab / Research Group Name` | Official research lab or group title |
| 30 | `Lab / Personal Website` | Hyperlinked personal or lab homepage |
| 31 | `Actively Hiring / Openings` | Recruitment announcements extracted from lab websites |
| 32 | `Target Skills / Prerequisites` | Required skills/languages (Python, C++, ROS2, PyTorch, etc.) |
| 33 | `Lab Facilities & Equipment` | Experimental setups, facilities & hardware |
| 34 | `Funding Sponsors` | Federal/industrial sponsors (NSF, NASA, ONR, DARPA, etc.) |
| 35 | `Software / Code Repo` | Open-source GitHub/Bitbucket/GitLab repositories |
| 36 | `Latest Project / Highlight` | Project banner, latest headline, or paper announcement |
| 37 | `Office Location` | Building and room number |
| 38 | `Is Field Match` | Boolean (`TRUE` / `FALSE`) |
| 39 | `Directory URL` | Source university directory URL (at the end of every row) |

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

---

## 4. Cold Outreach Intelligence: Flagship Paper, Tech Stack & Tripartite Finding

To elevate cold emails from generic inquiries into high-impact academic outreach that achieves a 25–35% response rate, adhere to the **4 Pillars of Cold Outreach**:

### 4.1 Pillar 1: Research Hook
- **Purpose**: Opens the email immediately after the salutation. Demonstrates understanding of the professor's overarching research agenda, tension, or open question.
- **Rule**: 1–2 sentences, curiosity-driven, no proper nouns (no professor name, no paper titles, no university name).
- **Template Frame**:
  `"[Field-level phenomenon / open challenge] — [what makes it fundamentally hard or intractable] — [what this group's approach addresses]."`

### 4.2 Pillar 2: Flagship Paper Selection & Filtering
The flagship paper is the single most relevant primary research paper used as the anchor hook. It must pass 4 strict filters:
1. **Subject Filter**: Fluid dynamics / CFD / aerodynamics keyword score $\ge 2$ in title + concepts.
2. **Article Type Filter**: Must be primary original research (exclude `review`, `survey`, `overview`, `book-chapter`, `editorial`, `erratum`).
3. **DOI Verification**: DOI must resolve with HTTP 200 via the Crossref API (`https://api.crossref.org/works/<doi>`).
4. **Detail Filter**: Abstract must contain both a named method/solver (for Tech Stack) and a quantitative metric (for Tripartite Finding).

**Paper Scoring Formula**:
$$\text{Score} = \text{Citations} + (50 \times \text{Fluid Keyword Hits}) + 100 \times \mathbb{I}(\text{Has Quant Result}) - 500 \times \mathbb{I}(\text{Is Review}) + \text{Recency Bonus}$$

### 4.3 Pillar 3: Tech Stack Extraction
- **Definition**: A concise, comma-separated list of the primary computational solvers or experimental tools actually used in the flagship paper.
- **Categories**:
  - *Open-Source CFD*: `OpenFOAM (LES)`, `Nek5000 (spectral-element DNS)`, `SU2 (adjoint optimization)`.
  - *Commercial CFD*: `ANSYS Fluent (k-ω SST)`, `STAR-CCM+`, `CONVERGE`, `OVERFLOW`.
  - *In-House Codes*: `In-house pseudo-spectral DNS solver`, `Immersed-boundary solver`.
  - *Experimental*: `Stereo PIV`, `Tomo-PIV`, `Hot-wire anemometry`, `Schlieren imaging`.
- **Rules**: Max 2–3 tools, under 60 characters, official naming format.

### 4.4 Pillar 4: Tripartite Physical Finding
The Tripartite Finding connects directly after the phrase:
> *"…specifically your investigation into…"*

It consists of three mandatory, interconnected components:
1. **Part 1 `[ENGINE]` — Active Methodology / Solver**:
   - Opens with an active gerund (`performing`, `conducting`, `coupling`, `deploying`).
   - Example: `performing wall-resolved large-eddy simulations (WRLES)` or `deploying stereo PIV in a Mach 2.5 blowdown tunnel`.
2. **Part 2 `[ARENA]` — Specific Flow Physics & Geometry**:
   - Combines geometry + flow condition / dimensionless regime.
   - Example: `transonic shock–boundary-layer interaction (SBLI) over a 24° compression ramp at Re_theta = 4500`.
3. **Part 3 `[PAYOFF]` — Root Physical Mechanism & Hard Quantitative Benchmark**:
   - Reveals causality (why the flow behaves as it does) and contains **at least one hard quantitative benchmark** (%, dB, St, Cf, Re_tau, Ma).
   - Example: `demonstrating that low-frequency shock oscillation is driven by upstream boundary layer breathing, resulting in a 28% peak wall-pressure fluctuation reduction`.

**Full Sentence Assembly Example**:
> *"I was particularly drawn to your work in [Journal], specifically your investigation into **performing wall-resolved large-eddy simulations** to investigate **transonic shock–boundary-layer interaction over a 24° compression ramp**, demonstrating that **shock-unsteadiness is coupled to upstream coherent structures, resulting in a 28% peak wall-pressure fluctuation reduction**."*

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
