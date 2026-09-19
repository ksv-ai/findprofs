# COLD_EMAIL_METHODOLOGY.md
## Complete Guide: Research Hook · Flagship Paper · Tech Stack · Tripartite Finding

> **Project root:** `D:\Others\forGradSc\newones\`
> **Primary data:** `cold_emails\US_R1_COLD_EMAIL_VAULT_V1.xlsx`
> **Preview output:** `COLD_EMAIL_PREVIEWS\US_R1_Tier1_Cold_Emails.md`
> **OpenAlex cache:** `scratch\rows_*_openalex.json`

---

## Table of Contents

1. [Overview of the Pipeline](#1-overview-of-the-pipeline)
2. [PILLAR 1 — Research Hook](#2-pillar-1--research-hook)
3. [PILLAR 2 — Flagship Paper Selection & Filtering](#3-pillar-2--flagship-paper-selection--filtering)
4. [PILLAR 3 — Tech Stack Extraction](#4-pillar-3--tech-stack-extraction)
5. [PILLAR 4 — Tripartite Physical Finding](#5-pillar-4--tripartite-physical-finding)
6. [Column Map — XLSX Structure](#6-column-map--xlsx-structure)
7. [OpenAlex Cache — Structure & Usage](#7-openalex-cache--structure--usage)
8. [DOI Verification via Crossref](#8-doi-verification-via-crossref)
9. [Complete Python Audit Script](#9-complete-python-audit-script)
10. [Preview Generation Script](#10-preview-generation-script)
11. [Git Commit Convention](#11-git-commit-convention)

---

## 1. Overview of the Pipeline

```
[XLSX Master Directory (Tier 1 & Tier 2 + Computational Math)]
        │
        ▼
[OpenAlex API]  ──cached──▶  [openalex_cache/<slug>.json]
        │
        ├─── PILLAR 1: Research Hook (Synthesized across 4–5 recent papers: Method + Regime + Outcome)
        ├─── PILLAR 2: Dual Recent Flagship Papers (2020–2026, Core Aero/Fluids/CFD scoring)
        │         └── Direct Clickable DOIs → Crossref/OpenAlex Verification
        ├─── PILLAR 3: Tech Stack (Synthesized across 4–5 recent papers)
        └─── PILLAR 4: Tripartite Physical Finding (from recent flagship papers)
        │
        ▼
[Apply all 4 pillars back to XLSX columns]
        │
        ▼
[generate markdown reference with abstracts & clickable DOIs]
        │
        ▼
[git commit & push → ksv-ai/findprofs]
```

**Four Quality Gates:**

| Gate | Pillar | Pass Criterion |
|------|--------|----------------|
| G1 | Research Hook | Synthesized from **4–5 recent papers**: `[Primary Method] + [Flow Regime/Physics] + [Target Engineering Outcome]`. Curiosity-driven, no proper nouns. |
| G2 | Flagship Papers | **2 Recent Flagship Papers (2020–2026)**: Crossref/OpenAlex verified DOI + fluid-dynamics subject + primary research (not review). |
| G3 | Tech Stack | Named solvers/tools/diagnostics synthesized across the **4–5 recent papers**. |
| G4 | Physical Finding | Valid Tripartite structure with at least one hard quantitative benchmark from recent flagship work. |

---

## 2. PILLAR 1 — Research Hook

### 2.1 What Is a Research Hook?

The Research Hook is the **opening sentence** of the cold email. It appears right after "Dear Prof. [Name]," and its job is to:

1. Show you have read and understood the professor's **recent research trajectory (across 4–5 recent papers, 2023–2026)**.
2. Create an immediate **intellectual connection** — it should feel like a fellow scientist wrote it, not a template bot.
3. Be formulated using the standard tripartite engineering synthesis:
   $$\text{Research Hook} = \mathbf{[Primary\ Method\ /\ Numerical\ Scheme]} + \mathbf{[Flow\ Regime\ /\ Physics]} + \mathbf{[Target\ Engineering\ Outcome]}$$
4. Be **curiosity-driven and forward-looking** — it mentions an open challenge, an unsolved question, or a compelling implication, not just a historical summary.

**The hook is NOT:**
- A citation of a single paper (that comes in the Flagship Paper sentence).
- A flattery phrase ("Your work is impressive…").
- A generic discipline label ("As a fluid dynamics researcher…").
- A sentence that could apply to any CFD professor.

### 2.2 The Structure Template

```
[Primary Method / Numerical Scheme] + [Flow Regime / Physics] + [Target Engineering Outcome]
```

Or framed as an active scientific inquiry:

```
"[Primary method/solver] for resolving [flow regime or multi-scale phenomenon]
in order to [target engineering outcome or physical discovery]."
```

**The hook must be specific enough to identify the professor's sub-area but broad enough that it covers their entire body of work, not just one paper.**

### 2.3 Step-by-Step Formulation (7 Steps)

#### STEP 1 — Read ALL the professor's works in the OpenAlex cache

Do not look at just the flagship paper. Go through the full `works` list and extract the **recurring themes**:

```python
# From the cache entry
works = cache_entry["works"]

# Collect all titles and concept tags
all_titles   = [w.get("title","") for w in works]
all_concepts = []
for w in works:
    for c in w.get("concepts", []):
        if c.get("score", 0) > 0.5:
            all_concepts.append(c["display_name"])

# Find the most frequent concepts (these = the professor's core agenda)
from collections import Counter
top_concepts = Counter(all_concepts).most_common(10)
print(top_concepts)
```

Typical output for a turbulence DNS researcher:
```
[('Turbulence', 12), ('Reynolds number', 10), ('Boundary layer', 9),
 ('Large eddy simulation', 7), ('DNS', 6), ('Wall-bounded flow', 5)]
```

→ This tells you their core arena is **wall-bounded turbulence at high Reynolds numbers using DNS/LES**.

---

#### STEP 2 — Identify the Professor's Core Scientific Question

From the recurring themes, distill the **one big question** the professor is trying to answer.

Ask yourself: *"If this professor gave a keynote, what would the title be?"*

Examples:
- Turbulence DNS researcher → *"How do near-wall coherent structures scale with Reynolds number?"*
- SBLI modeller → *"Why do RANS models fail at shock–boundary-layer interactions, and can hybrid methods fix it?"*
- Experimental rough-wall BL → *"Does outer-layer similarity hold over industrially relevant rough surfaces?"*
- Combustion LES → *"What controls thermoacoustic instability onset in lean-premixed gas turbines?"*

---

#### STEP 3 — Identify the Open Challenge or Unsolved Problem

A great hook names an **open challenge** in the field — something that is still debated, poorly predicted, or computationally intractable. This shows scientific depth.

Examples of open challenges by sub-field:

| Sub-field | Open Challenge |
|-----------|---------------|
| Wall-bounded turbulence | Reynolds-number extrapolation of near-wall scaling laws |
| SBLI / shock physics | RANS failure at separated SBLI and transition prediction |
| Hypersonic aerodynamics | Ablative surface coupling and surface roughness effects on transition |
| Combustion | Thermoacoustic instability prediction and NOx emission control |
| Bluff-body aerodynamics | Unsteady wake dynamics and aeroelastic coupling at high Re |
| Multiphase flows | Droplet/bubble dynamics in turbulent shear layers |
| Rotating machinery | Tip-vortex and clearance flow losses in turbomachinery |
| Wind energy | Turbulent wake interactions in large wind farms |

---

#### STEP 4 — Write a Draft Hook (No Proper Nouns Yet)

Combine Steps 2 and 3 into one or two sentences. **Key rules:**

- **No professor's name** in the hook — it becomes generic if you do.
- **No specific paper titles or DOIs** — those come later.
- **No university name** — unnecessary and impersonal.
- **No "I" until the second paragraph** — this first sentence is about their science, not you.
- Start with the phenomenon or challenge, not with "Your research focuses on…"

**Draft templates:**

```
Template A (Open Question):
"Understanding [phenomenon] at [extreme condition or scale] remains one of the
central challenges in [sub-field], where [specific difficulty] limits our ability
to [practical goal or theoretical extrapolation]."

Template B (Paradox / Tension):
"Despite decades of [approach], [specific sub-problem] continues to elude
predictive accuracy — a gap that becomes critical at [industrially or
physically relevant regime]."

Template C (Implication-Forward):
"The interplay between [mechanism A] and [mechanism B] in [flow configuration]
controls [important outcome], yet the governing scaling laws remain poorly
understood beyond [current limit]."
```

---

#### STEP 5 — Check Against the Professor's Work

Read the draft hook and ask:

1. Could this hook apply to **five other professors** in the same sub-field? → If yes, it is too generic. Add one more specific detail.
2. Does it reference work the professor has **actually done** (even if broadly)? → Verify against the top concepts.
3. Does it end in a way that **flows into** the flagship paper sentence? → The next sentence should feel like a natural continuation.

---

#### STEP 6 — Final Grammar & Tone Check

| Check | Requirement |
|-------|-------------|
| Length | 1–2 sentences, max 50 words |
| Tone | Scientific, collegial, not sycophantic |
| No proper nouns | No names, no paper titles, no university names |
| Ends with | An open implication or challenge — not a full stop of finality |
| Flows into | "I was particularly drawn to your work on [TITLE]…" |

---

#### STEP 7 — Examples of Great vs. Bad Hooks

**Sub-area: High-Re Wall-Bounded Turbulence**

✅ **GREAT:**
> "Understanding how large-scale motions modulate near-wall turbulence at high Reynolds numbers — and whether classical scaling laws remain valid beyond Reτ ∼ 10⁴ — is one of the most consequential open questions in wall-bounded flow research, with direct implications for drag prediction in aerospace and marine systems."

❌ **BAD:**
> "Your research on turbulence and fluid mechanics is very interesting and relevant to my background."
*(Generic, no specific challenge, no scientific depth)*

❌ **BAD:**
> "I read your 2022 paper in the Journal of Fluid Mechanics on DNS at Reτ = 5200."
*(That's the flagship paper sentence, not the hook)*

---

**Sub-area: Shock–Boundary-Layer Interaction**

✅ **GREAT:**
> "Predicting the onset and extent of separation in shock–boundary-layer interactions remains a critical unsolved problem in high-speed aerodynamics — one where RANS-based approaches systematically fail and where high-fidelity simulations at flight-relevant Reynolds numbers remain computationally prohibitive."

❌ **BAD:**
> "Shock–boundary-layer interaction is an important topic in CFD."
*(Zero scientific depth — any undergraduate could write this)*

---

**Sub-area: Combustion / Thermoacoustics**

✅ **GREAT:**
> "The coupling between turbulent flame dynamics and acoustic resonance in lean-premixed combustors governs both emission performance and thermoacoustic stability, yet the precise feedback mechanism that triggers limit-cycle oscillations at realistic fuel–air equivalence ratios is still not fully understood."

---

### 2.4 Common Hook Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Names the professor | "Your work on turbulence is…" | Start with the phenomenon |
| Names the paper | "Your 2022 JFM paper…" | That goes in sentence 2 |
| Too short / vague | "Turbulence is complex." | Add the specific challenge + regime |
| Too flattering | "Your groundbreaking research…" | Delete all adjectives; state facts |
| Cannot be connected | Hook about combustion, but flagship paper is turbomachinery | Align hook sub-topic to flagship paper |

---

## 3. PILLAR 2 — Dual Recent Flagship Paper Selection & Filtering

### 3.1 What Are the Flagship Papers?

The **2 Flagship Papers** are the two most impressive, relevant, and verifiable primary research articles by the professor that:

1. Are drawn strictly from **recent publications (2020–2026)** to reflect modern lab capabilities and active grants.
2. Are closely tied to **core fluid dynamics / CFD / turbulence / hypersonics / combustion / aero-acoustics**.
3. Have **live, verified DOIs** with direct clickable hyperlinks (`https://doi.org/...`).
4. Are **primary research articles** (not a review, not an editorial, not a book chapter).
5. Contain sufficient **methodological and physical detail** to extract the Tech Stack and Tripartite Findings.

### 3.2 The Five-Layer Filter

Apply filters in this order. Candidate papers must pass **all five** to qualify as flagship papers:

```
FILTER 1: Recency Filter        → Published between 2020 and 2026?
FILTER 2: Subject Filter        → Is it fluid dynamics / CFD / aero (score ≥ 2)?
FILTER 3: Article Type Filter   → Is it primary research (not a review/editorial)?
FILTER 4: DOI Filter            → Does the DOI resolve via OpenAlex/Crossref?
FILTER 5: Detail Filter         → Does the abstract contain method + quantitative result?
```

---

#### FILTER 1 — Subject Filter (Fluid-Dynamics Keywords)

Score each paper by counting how many of these keywords appear in the title + concept tags:

```python
FLUID_KEYWORDS = {
    # Phenomena
    "turbulence", "boundary layer", "shock", "vortex", "wake",
    "separation", "transition", "reattachment", "recirculation",
    "laminar", "compressible", "incompressible", "multiphase",
    "cavitation", "combustion", "detonation", "heat transfer",
    # Regimes
    "hypersonic", "supersonic", "transonic", "subsonic",
    "Mach", "Reynolds", "Strouhal", "Prandtl",
    # Methods — Numerical
    "DNS", "LES", "RANS", "DES", "DDES", "SDES", "ILES", "WRLES",
    "Navier-Stokes", "OpenFOAM", "ANSYS", "Fluent", "OVERFLOW",
    "SU2", "Nek5000", "STAR-CCM+", "CONVERGE", "COMSOL",
    # Methods — Experimental
    "PIV", "hot-wire", "Schlieren", "shadowgraph", "PSP",
    "particle image velocimetry", "laser Doppler",
    # Applications
    "aerodynamics", "aeroelasticity", "turbomachinery", "wind turbine",
    "helicopter", "airfoil", "wing", "nozzle", "combustor", "scramjet",
    "rocket", "re-entry", "bluff body", "cylinder", "pipe flow",
    "channel flow", "flat plate"
}

def fluid_score(work: dict) -> int:
    title    = (work.get("title") or "").lower()
    concepts = " ".join(c.get("display_name","") for c in work.get("concepts",[])).lower()
    combined = title + " " + concepts
    return sum(1 for kw in FLUID_KEYWORDS if kw.lower() in combined)
```

**Threshold:** A paper must score **≥ 2** to pass Filter 1.
Papers scoring 0–1 are almost certainly off-topic (materials science, chemistry, biology, etc.)

---

#### FILTER 2 — Article Type Filter (No Reviews)

Exclude papers whose title or type suggests a review, survey, or book chapter:

```python
REVIEW_SIGNALS = [
    "review of", "survey of", "overview of", "tutorial on",
    "state of the art", "handbook", "textbook", "invited paper",
    "perspective on", "progress in", "advances in"
]

def is_review(work: dict) -> bool:
    title = (work.get("title") or "").lower()
    return any(sig in title for sig in REVIEW_SIGNALS)
```

Also check the `type` field from OpenAlex:
```python
if work.get("type") in ["review", "book-chapter", "book", "editorial"]:
    return True  # skip this paper
```

---

#### FILTER 3 — DOI Verification via Crossref

Even if a DOI *looks* valid, it must be verified:

```python
import requests, time

def verify_doi(doi_raw: str) -> bool:
    clean = doi_raw.replace("https://doi.org/","").replace("http://doi.org/","").strip()
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{clean}",
            headers={"User-Agent": "UniAbroad/1.0"},
            timeout=15
        )
        time.sleep(0.4)
        return r.status_code == 200
    except:
        return False
```

**Why Crossref and not just the DOI URL?**

| Check | What it catches |
|-------|----------------|
| `doi.org/{doi}` redirect | Only tells you the redirect target exists |
| Browser resolution | May show "article not found" pages that still return HTTP 200 |
| **Crossref API** ✅ | Only returns 200 for *registered, metadata-complete* works |

A DOI that passes Crossref is **guaranteed to resolve correctly** for the professor reading the email.

---

#### FILTER 4 — Abstract Detail Filter

The abstract must contain **both** of the following:

1. **A named method or tool** (so you can write a Tech Stack).
2. **A quantitative result** (so you can write a Tripartite Finding).

```python
import re

QUANT_PATTERN = re.compile(r'\d+\.?\d*\s*(%|dB|St|Cf|TKE|Reτ|Ma|Hz|kHz|N-factor|°|×)')
METHOD_KEYWORDS = {"DNS", "LES", "RANS", "PIV", "OpenFOAM", "Fluent", "Nek5000",
                   "SU2", "OVERFLOW", "hot-wire", "Schlieren", "SPIV", "adjoint"}

def passes_detail_filter(abstract: str) -> bool:
    has_quant  = bool(QUANT_PATTERN.search(abstract))
    has_method = any(kw in abstract for kw in METHOD_KEYWORDS)
    return has_quant and has_method
```

---

### 3.3 Final Scoring & Selection

Combine all signals into a final score:

```python
def score_paper(work: dict, abstract: str) -> float:
    score = 0.0

    # Citation count (most important signal of impact)
    score += work.get("cited_by_count", 0) * 1.0

    # Fluid-dynamics keyword hits (relevance)
    score += fluid_score(work) * 50

    # Bonus for passing detail filter
    if passes_detail_filter(abstract):
        score += 100

    # Penalty for being a review
    if is_review(work):
        score -= 500

    # Recency bonus (papers from last 10 years)
    year = work.get("publication_year", 2000)
    if year >= 2015:
        score += 30
    if year >= 2020:
        score += 20

    return score
```

Select the paper with the **highest score** that also passes **all four filters**.

---

### 3.4 What Happens When No Paper Passes All Filters?

**Fallback strategy (in order):**

1. **Relax Filter 1 threshold** from ≥2 to ≥1 keyword hit.
2. **Accept a paper without a quantitative result** — use the method name alone to form a partial finding.
3. **Search OpenAlex directly** by professor name + fluid keyword:
   ```
   GET https://api.openalex.org/works?filter=author.display_name.search:"Jane Doe",concepts.id:C154945302&sort=cited_by_count:desc
   ```
   (`C154945302` = OpenAlex concept ID for "Fluid Mechanics")
4. **Mark the row for manual review** — flag it in the XLSX with `NEEDS_REVIEW` in column 27.

---

## 4. PILLAR 3 — Tech Stack Extraction (Across 4–5 Recent Papers)

### 4.1 What Is the Tech Stack?

The Tech Stack is a **concise, comma-separated list of the primary computational solvers, numerical frameworks, and experimental tools** actively deployed across the professor's **4–5 recent papers (2024–2026)**. It appears in the cold outreach profile as:

> **Tech Stack:** OpenFOAM (LES), Nek5000, high-order DG, Stereo PIV

It is **not** a generic list of high-level buzzwords. It represents the specific software, numerical methods, and diagnostics the lab actively uses today to generate data and publish findings.

### 4.2 Why Does It Matter?

- It proves you understand their current lab infrastructure and active grant workflows.
- It shows methodological compatibility — demonstrating you have skills in the exact tools they need.
- It grounds your application in software and hardware proficiencies that allow you to contribute immediately.

### 4.3 Step-by-Step Extraction (5 Steps)

#### STEP 1 — Read the Abstract for Named Solvers / Tools

Scan the abstract text for any of these categories:

**Category A — Open-Source CFD Solvers:**
```
OpenFOAM, SU2, Nek5000, Basilisk, Palabos, PyFR, FEniCS,
deal.II, DOLFIN, OpenLB, REEF3D
```

**Category B — Commercial / Proprietary Solvers:**
```
ANSYS Fluent, ANSYS CFX, STAR-CCM+, COMSOL, CONVERGE,
OVERFLOW, FUN3D, Cart3D, CFL3D, TAU (DLR), elsA (ONERA)
```

**Category C — In-House / Custom Codes:**
```
"in-house code", "custom solver", "spectral element method",
"Fourier–Chebyshev code", "pseudo-spectral solver"
```
→ In this case write: `In-house pseudo-spectral DNS code`

**Category D — Experimental Techniques:**
```
PIV, SPIV, Tomo-PIV, hot-wire anemometry, Schlieren imaging,
shadowgraphy, pressure-sensitive paint (PSP), oil-flow visualization,
laser Doppler velocimetry (LDV), infrared thermography
```

**Category E — Simulation Paradigm (if no specific code named):**
```
DNS (Direct Numerical Simulation)
LES (Large Eddy Simulation)
RANS (Reynolds-Averaged Navier-Stokes)
WRLES (Wall-Resolved LES)
ILES (Implicit LES)
DES / DDES / SDES (Detached Eddy Simulation variants)
Hybrid RANS/LES
```

---

#### STEP 2 — Check the Concept Tags in OpenAlex

The `concepts` field in OpenAlex often includes the method name even when the abstract is sparse:

```python
for concept in work.get("concepts", []):
    if concept["score"] > 0.6:
        print(concept["display_name"])
```

Example output:
```
Large eddy simulation      0.95
OpenFOAM                   0.88
Turbulence                 0.92
Boundary layer             0.81
```
→ Tech Stack: `OpenFOAM (LES)`

---

#### STEP 3 — Classify as Numerical or Experimental

| Abstract says... | Tech Stack format |
|-----------------|------------------|
| `"DNS of turbulent channel flow"` | `DNS (in-house spectral code)` or just `DNS` |
| `"Large-eddy simulations using OpenFOAM"` | `OpenFOAM (LES)` |
| `"ANSYS Fluent with k-ω SST turbulence model"` | `ANSYS Fluent (k-ω SST)` |
| `"PIV measurements in a wind tunnel"` | `Stereo PIV` |
| `"hybrid RANS/LES with dynamic Smagorinsky"` | `Hybrid RANS/LES (dynamic Smagorinsky)` |
| `"SU2 with adjoint-based optimization"` | `SU2 (adjoint optimization)` |
| `"Nek5000 spectral-element DNS"` | `Nek5000 (spectral-element DNS)` |

---

#### STEP 4 — If Multiple Tools Are Named, Rank and Select Top 2-3

If the paper uses multiple tools (e.g., DNS + experimental validation):

1. **Primary tool first** — the one used to generate the main results.
2. **Secondary tool second** — used for validation or comparison.
3. Maximum **3 items** in the Tech Stack to keep it concise.

Example:
> "Wall-resolved LES using Nek5000 was validated against hot-wire measurements."
→ Tech Stack: `Nek5000 (WRLES), Hot-wire anemometry`

---

#### STEP 5 — Final Format Rules

- Use the **official tool name**, not an abbreviation alone if the full name is known.
- Include the **method paradigm in parentheses** where helpful: `OpenFOAM (LES)`, not just `OpenFOAM`.
- Separate multiple tools with commas: `ANSYS Fluent (k-ω SST), Schlieren imaging`
- Keep total length under **60 characters**.

**✅ Good Tech Stacks:**
- `Nek5000 (spectral-element DNS)`
- `OpenFOAM (WRLES), PIV`
- `ANSYS Fluent (k-ω SST RANS)`
- `In-house pseudo-spectral DNS, Hot-wire anemometry`
- `SU2 (adjoint-based shape optimization)`

**❌ Bad Tech Stacks:**
- `CFD` — not specific enough
- `MATLAB` — post-processing tool, not a solver
- `Python, NumPy` — data analysis, not CFD
- `DNS, LES, RANS, PIV, OpenFOAM, ANSYS, SU2` — too many, pick the paper's primary tool

---

### 4.4 When the Abstract Does Not Name Any Tool

This happens most often with older papers or experimental-only work. Resolution:

1. **Check the title** — "Direct numerical simulation of…" → DNS
2. **Check the OpenAlex concepts** — they often tag the method even if the abstract is generic.
3. **Search the full paper PDF** title page / methods section via a DOI-based link.
4. **Fallback:** Use the paradigm alone: `DNS`, `Experimental (wind tunnel)`, or `LES`

---

## 5. PILLAR 4 — Tripartite Physical Finding

### 5.1 The Core Sentence Frame

The finding slots **grammatically after** the phrase:

> *"…specifically your investigation into…"*

Full cold-email sentence:

> *"I was particularly drawn to your work on [TITLE], specifically your investigation into **[PART 1]** to investigate **[PART 2]**, demonstrating that **[PART 3]**."*

---

### 5.2 Anatomy of the Three Parts

---

#### PART 1 — Active Methodology / Tool / Solver `[ENGINE]`

```
[gerund verb] [specific method / solver / experimental rig]
```

**Opens with an active gerund:**

| Method Type | Best Gerund |
|------------|-------------|
| Numerical simulation | `performing`, `executing`, `conducting` |
| Hybrid / coupled method | `coupling`, `combining` |
| Optimization / adjoint | `applying`, `deploying` |
| Experimental technique | `deploying`, `conducting` |
| Modal decomposition | `applying POD/DMD/SPOD to` |

**✅ Good:**
- `performing wall-resolved large-eddy simulations (WRLES)`
- `coupling Lattice-Boltzmann solvers with immersed-boundary methods`
- `deploying pressure-sensitive paint (PSP) in a Mach 2.5 blowdown tunnel`

**❌ Bad:**
- `the use of DNS` — no gerund
- `CFD study of…` — not a gerund
- `investigating turbulence` — too broad, no method

---

#### PART 2 — Specific Flow Physics / Configuration `[ARENA]`

```
[specific geometry / flow regime / shock / vortex structure]
```

- Specific enough that a domain expert can picture the exact test case.
- Combines **geometry + flow condition**:
  `turbulent channel flow at Reτ = 5200` or `M = 1.5 SBLI over a 14° wedge`

**✅ Good:**
- `transonic shock–boundary-layer interaction (SBLI) over a 25° compression ramp`
- `turbulent channel flow at Reτ = 5200 with spanwise wall oscillation`
- `roughness-induced transition over a hypersonic flat-plate geometry`

**❌ Bad:**
- `turbulent flows` — too vague
- `aerodynamics problems` — not a configuration

---

#### PART 3 — Root Mechanism / Scaling Law / Quantitative Discovery `[PAYOFF]`

```
[causal mechanism phrase] [exact metric / benchmark / number with units]
```

**Must contain at least one hard number:**
- `drag reduced by 23%`
- `St ≈ 0.27`
- `κ = 0.384 confirmed to within 1%`
- `k-ω SST over-predicts peak TKE by 31%`

**Must reveal causality (the *why*), not just observation (the *what*):**

| Weak (observation) | Strong (causality + number) |
|-------------------|-----------------------------|
| "results agree with experiment" | "pressure–strain redistribution dominates dissipation by 3.7× in the recirculation zone" |
| "the flow separates" | "separation onset shifts 40% upstream when Reτ exceeds 2000, driven by outer-layer streak growth" |
| "skin friction decreases" | "skin-friction drag reduced 17% via spanwise wall oscillation at optimal Wo = 14" |

---

### 5.3 Step-by-Step Extraction from an Abstract (7 Steps)

#### STEP 1 — Find the Method (→ PART 1)
Scan for: `DNS, LES, WRLES, RANS, DES, PIV, Schlieren, adjoint, POD, DMD, OpenFOAM, Nek5000, SU2…`
Wrap in gerund. (See Gerund table in §5.2 PART 1)

#### STEP 2 — Find the Geometry / Regime (→ PART 2)
Scan for: geometry names, `Re_τ = [N]`, `Ma = [N]`, `AoA = [°]`, flow configuration labels.
Combine: `[geometry] at [condition]`

#### STEP 3 — Find the Hard Number (→ PART 3 anchor)
Scan for: `%`, `dB`, `St`, `Cf`, `TKE`, `N-factor`, `factor of [N]`, any dimensionless group with a value.

#### STEP 4 — Find the Causal Mechanism (→ PART 3 wrapper)
Scan for: `"driven by"`, `"attributed to"`, `"dominated by"`, `"triggers"`, `"scales with"`, `"fails to capture"`, `"reveals that"`, `"demonstrates that"`.

#### STEP 5 — Assemble
```
PART 1: [gerund] [method from Step 1]
PART 2: [geometry + condition from Step 2]
PART 3: [mechanism from Step 4] [number from Step 3]
```

#### STEP 6 — Grammar Check
Read aloud after *"…specifically your investigation into…"*:
- Flows naturally? ✅
- Gerund at start? ✅
- Hard number in PART 3? ✅
- PART 3 is a discovery, not a method description? ✅
- Under 55 words total? ✅

#### STEP 7 — Period Check
- No double periods (`..`).
- Ends with `.` before the new line that has Tech Stack.
- Does not repeat the paper title verbatim.

---

### 5.4 Three Worked Examples with Real Abstracts

---

#### Example A — DNS Turbulent Channel Flow

**Abstract:**
> *"We perform direct numerical simulations of turbulent channel flow at friction Reynolds numbers up to Reτ = 5200. The results reveal that the von Kármán constant κ = 0.384 is confirmed to within 1% across the full Reynolds-number range, and that the log layer begins at y⁺ ≈ 200."*

| Step | Extracted |
|------|-----------|
| Method (PART 1) | `direct numerical simulations` → gerund: `performing` |
| Arena (PART 2) | `turbulent channel flow at Reτ = 5200` |
| Number (PART 3) | `κ = 0.384`, `1%` |
| Mechanism (PART 3) | `von Kármán constant confirmed`, `log layer begins at y⁺ ≈ 200` |

**Assembled Finding:**
> performing direct numerical simulations (DNS) to investigate turbulent channel flow at Reτ = 5200, demonstrating that the von Kármán constant κ = 0.384 holds to within 1% across the full Reynolds-number range and that the logarithmic layer begins at y⁺ ≈ 200.

---

#### Example B — Hybrid RANS/LES SBLI

**Abstract:**
> *"Hybrid RANS/LES with a dynamic Smagorinsky closure is applied to a shock–boundary-layer interaction at M = 2.3 over a 24° compression ramp. Skin-friction predictions show k-ω SST over-predicts peak Cf by 38%, traced to an overestimate of Reynolds shear stress in the interaction region."*

| Step | Extracted |
|------|-----------|
| Method (PART 1) | `hybrid RANS/LES with dynamic Smagorinsky closure` → gerund: `applying` |
| Arena (PART 2) | `shock–boundary-layer interaction at M = 2.3 over a 24° compression ramp` |
| Number (PART 3) | `38%` |
| Mechanism (PART 3) | `k-ω SST overestimates Reynolds shear stress → 38% Cf error` |

**Assembled Finding:**
> applying hybrid RANS/LES with a dynamic Smagorinsky closure to investigate shock–boundary-layer interaction at M = 2.3 over a 24° compression ramp, demonstrating that k-ω SST over-predicts peak skin friction by 38% due to an overestimate of Reynolds shear stress in the interaction zone.

---

#### Example C — Experimental Rough-Wall Boundary Layer

**Abstract:**
> *"Stereo PIV measurements characterize the turbulent boundary layer over a rough surface (ks+ = 50–200). The roughness function ΔU+ scales logarithmically with ks+ above ks+ = 70, with outer-layer similarity holding to within 3%."*

| Step | Extracted |
|------|-----------|
| Method (PART 1) | `stereo particle-image velocimetry (SPIV)` → gerund: `conducting` |
| Arena (PART 2) | `turbulent boundary layer over a rough surface (ks⁺ = 50–200)` |
| Number (PART 3) | `outer-layer similarity to within 3%`, `ΔU⁺` log scaling |
| Mechanism (PART 3) | `ΔU⁺ scales logarithmically above ks⁺ = 70` |

**Assembled Finding:**
> conducting stereo particle-image velocimetry (SPIV) measurements to characterize the turbulent boundary layer over a rough surface (ks⁺ = 50–200), demonstrating that the roughness function ΔU⁺ scales logarithmically with ks⁺ above ks⁺ = 70 and that outer-layer similarity holds to within 3% for all tested conditions.

---

### 5.5 Common Mistakes Table

| Mistake | Wrong | Correct |
|---------|-------|---------|
| No gerund opening | `"DNS of turbulent channel…"` | `"performing DNS of turbulent channel…"` |
| No hard number | `"showing turbulence is enhanced"` | `"showing a 23% increase in TKE production"` |
| Mechanism missing | `"Cf values match experiment"` | `"k-ω SST under-predicts Cf by 14% due to…"` |
| Too long (>55 words) | All results crammed in | Keep only the single most important finding |
| Double period | `"…by 14%.. Tech Stack:"` | `"…by 14%."` on its own line |
| Repeats title verbatim | Finding = title reworded | Rephrase to highlight the discovery |

---

## 6. Column Map — XLSX Structure

`US_R1_COLD_EMAIL_VAULT_V1.xlsx` — key columns (0-indexed):

| Col | Header | Pillar |
|-----|--------|--------|
| 0 | `Row_Number` | — |
| 1 | `First_Name` | — |
| 2 | `Last_Name` | — |
| 3 | `Email` | — |
| 4 | `University` | — |
| 5 | `Department` | — |
| 6 | `Research_Hook` | **PILLAR 1** |
| 7 | `Flagship_Paper_Title` | **PILLAR 2** |
| 8 | `Flagship_Paper_DOI` | **PILLAR 2** |
| 9 | `Flagship_Paper_Year` | **PILLAR 2** |
| 10 | `Flagship_Paper_Venue` | **PILLAR 2** |
| 11 | `Physical_Finding` | **PILLAR 4** |
| 12 | `Tech_Stack` | **PILLAR 3** |
| 27 | `Funding_Sponsors` | Cleared/blank |

---

## 7. OpenAlex Cache — Structure & Usage

### File Naming
```
scratch\rows_{start}_{end}_openalex.json
scratch\rows_{start}_{end}_openalex_auth.json
```

### JSON Structure
```json
[
  {
    "row": 101,
    "faculty_name": "Jane Doe",
    "university": "MIT",
    "works": [
      {
        "id": "https://openalex.org/W1234567890",
        "doi": "https://doi.org/10.1017/jfm.2022.123",
        "title": "Direct numerical simulation of turbulent channel flow",
        "publication_year": 2022,
        "primary_location": {
          "source": { "display_name": "Journal of Fluid Mechanics" }
        },
        "abstract_inverted_index": { "We": [0], "perform": [1], "DNS": [2] },
        "cited_by_count": 145,
        "concepts": [
          { "display_name": "Turbulence", "score": 0.98 },
          { "display_name": "Large eddy simulation", "score": 0.85 }
        ]
      }
    ]
  }
]
```

### Abstract Reconstruction
```python
def reconstruct_abstract(inv: dict) -> str:
    if not inv:
        return ""
    max_p = max(p for ps in inv.values() for p in ps)
    words = [""] * (max_p + 1)
    for w, ps in inv.items():
        for p in ps:
            words[p] = w
    return " ".join(words)
```

---

## 8. DOI Verification via Crossref

```python
import requests, time

def verify_doi(doi_raw: str) -> dict:
    clean = doi_raw.replace("https://doi.org/","").replace("http://doi.org/","").strip()
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{clean}",
            headers={"User-Agent": "UniAbroad/1.0"},
            timeout=15
        )
        time.sleep(0.4)
        if r.status_code == 200:
            m = r.json()["message"]
            return {
                "valid": True,
                "title": m.get("title",[""])[0],
                "year":  (m.get("published",{}).get("date-parts") or [[None]])[0][0],
                "venue": m.get("container-title",[""])[0] or m.get("event",{}).get("name",""),
                "doi":   clean
            }
        return {"valid": False, "status": r.status_code}
    except Exception as e:
        return {"valid": False, "error": str(e)}
```

---

## 9. Complete Python Audit Script

Save as `scratch\audit_and_apply.py`:

```python
"""
audit_and_apply.py  —  Full cold-email audit pipeline
Load XLSX → OpenAlex cache → Crossref verify → Re-synthesize → Apply
Usage:
    python scratch\audit_and_apply.py --start 101 --end 150
    python scratch\audit_and_apply.py --start 101 --end 150 --apply
"""

import argparse, json, time, requests, re, openpyxl
from pathlib import Path
from collections import Counter

BASE_DIR    = Path(r"D:\Others\forGradSc\newones")
XLSX_PATH   = BASE_DIR / "cold_emails" / "US_R1_COLD_EMAIL_VAULT_V1.xlsx"
SCRATCH_DIR = BASE_DIR / "scratch"

COL = {"first":1,"last":2,"doi":8,"title":7,"year":9,"venue":10,"finding":11,"tech":12}

FLUID_KW = {
    "turbulence","boundary layer","shock","LES","DNS","RANS","DES","vortex",
    "Navier-Stokes","Reynolds","aerodynamics","compressible","hypersonic",
    "supersonic","cavitation","combustion","OpenFOAM","ANSYS","Fluent",
    "SU2","Nek5000","OVERFLOW","STAR-CCM+","PIV","hot-wire","Schlieren"
}

REVIEW_SIGNALS = ["review of","survey of","overview of","state of the art",
                  "tutorial on","handbook","perspective on","advances in"]

def load_cache(start, end):
    all_rows = []
    for f in sorted(SCRATCH_DIR.glob("rows_*_openalex*.json")):
        parts = f.stem.split("_")
        try:
            fs, fe = int(parts[1]), int(parts[2])
        except:
            continue
        if fe < start or fs > end:
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        all_rows.extend(data)
        print(f"  [cache] {f.name}: {len(data)} entries")
    seen = {}
    for e in all_rows:
        r = e.get("row") or e.get("row_number")
        if r and r not in seen:
            seen[r] = e
    return seen

def reconstruct_abstract(inv):
    if not inv:
        return ""
    max_p = max(p for ps in inv.values() for p in ps)
    words = [""] * (max_p + 1)
    for w, ps in inv.items():
        for p in ps:
            words[p] = w
    return " ".join(words)

def fluid_score(work):
    txt = (work.get("title") or "").lower()
    txt += " ".join(c.get("display_name","") for c in work.get("concepts",[])).lower()
    return sum(1 for kw in FLUID_KW if kw.lower() in txt)

def is_review(work):
    title = (work.get("title") or "").lower()
    return any(s in title for s in REVIEW_SIGNALS) or work.get("type") in ["review","book-chapter"]

def select_flagship(works):
    candidates = []
    for w in works:
        if not w.get("doi") or is_review(w):
            continue
        score = w.get("cited_by_count", 0) + fluid_score(w) * 50
        year  = w.get("publication_year", 2000)
        if year >= 2015: score += 30
        if year >= 2020: score += 20
        candidates.append((score, w))
    return sorted(candidates, reverse=True)[0][1] if candidates else None

def verify_doi(doi_raw):
    clean = doi_raw.replace("https://doi.org/","").replace("http://doi.org/","").strip()
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{clean}",
            headers={"User-Agent":"UniAbroad/1.0"},
            timeout=15
        )
        time.sleep(0.4)
        if r.status_code == 200:
            m = r.json()["message"]
            return {
                "valid": True,
                "title": m.get("title",[""])[0],
                "year":  (m.get("published",{}).get("date-parts") or [[None]])[0][0],
                "venue": m.get("container-title",[""])[0] or m.get("event",{}).get("name",""),
                "doi":   clean
            }
        return {"valid": False, "status": r.status_code, "doi": clean}
    except Exception as e:
        return {"valid": False, "error": str(e), "doi": clean}

def run(start, end, dry_run=True):
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active
    cache = load_cache(start, end)
    print(f"Cache loaded: {len(cache)} entries\n")

    broken, corrections = [], {}

    for master_row in range(start, end + 1):
        xlsx_row = master_row + 1
        cells    = [ws.cell(row=xlsx_row, column=c+1).value for c in range(30)]
        name     = f"{cells[COL['first']]} {cells[COL['last']]}"
        doi_raw  = cells[COL['doi']] or ""

        print(f"Row {master_row:>3}: {name:<30} | {doi_raw[:45]}")
        res = verify_doi(doi_raw)

        if res["valid"]:
            print(f"         ✅ VALID")
        else:
            print(f"         ❌ BROKEN (HTTP {res.get('status','ERR')})")
            broken.append(master_row)
            entry = cache.get(master_row)
            if entry:
                best = select_flagship(entry.get("works", []))
                if best:
                    new_doi = (best.get("doi","")).replace("https://doi.org/","")
                    rc = verify_doi(new_doi)
                    if rc["valid"]:
                        abstract = reconstruct_abstract(best.get("abstract_inverted_index",{}))
                        print(f"         🔄 REPLACEMENT: {new_doi}")
                        print(f"         📄 Abstract[:200]: {abstract[:200]}")
                        corrections[master_row] = {
                            COL["doi"]:   f"https://doi.org/{new_doi}",
                            COL["title"]: best.get("title",""),
                            COL["year"]:  best.get("publication_year",""),
                            COL["venue"]: (best.get("primary_location") or {}).get("source",{}).get("display_name",""),
                        }
                    else:
                        print(f"         ⚠️  Replacement also broken: {new_doi}")
                else:
                    print(f"         ⚠️  No fluid-relevant paper in cache")
            else:
                print(f"         ⚠️  No cache entry for row {master_row}")
        print()

    if not dry_run and corrections:
        for mr, updates in corrections.items():
            for ci, val in updates.items():
                ws.cell(row=mr+1, column=ci+1).value = val
        wb.save(XLSX_PATH)
        print(f"✅ Saved {len(corrections)} corrections")
    else:
        print(f"[DRY RUN] {len(corrections)} corrections pending — use --apply to write")

    print(f"\nSUMMARY | Rows: {end-start+1} | Broken: {len(broken)} | Fixed: {len(corrections)}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end",   type=int, required=True)
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()
    run(a.start, a.end, dry_run=not a.apply)
```

---

## 10. Preview Generation Script

Save as `scratch\generate_us_r1_previews.py`:

```python
"""
generate_us_r1_previews.py
Reads XLSX → outputs formatted Markdown cold-email previews.
Usage:
    python scratch\generate_us_r1_previews.py
    python scratch\generate_us_r1_previews.py --start 101 --end 150
"""

import openpyxl
from pathlib import Path

BASE_DIR    = Path(r"D:\Others\forGradSc\newones")
XLSX_PATH   = BASE_DIR / "cold_emails" / "US_R1_COLD_EMAIL_VAULT_V1.xlsx"
OUTPUT_PATH = BASE_DIR / "COLD_EMAIL_PREVIEWS" / "US_R1_Tier1_Cold_Emails.md"

COL = {"first":1,"last":2,"univ":4,"doi":8,"year":9,"venue":10,
       "hook":6,"title":7,"finding":11,"tech":12}

def clean(s):
    s = (s or "").strip().replace("..", ".")
    return s if s.endswith(".") else s + "."

def build_body(cells):
    return (
        f"Dear Prof. {cells[COL['first']]},\n\n"
        f"I hope this message finds you well. {cells[COL['hook']]}\n\n"
        f"I was particularly drawn to your work on *{cells[COL['title']]}*, "
        f"specifically your investigation into {clean(cells[COL['finding']])}\n\n"
        f"**Tech Stack:** {cells[COL['tech']]}\n\n"
        f"I am currently seeking PhD opportunities for Fall 2025 and believe my "
        f"background in computational fluid dynamics aligns closely with your research "
        f"program. I would be grateful for the opportunity to discuss potential openings "
        f"in your group.\n\n"
        f"Thank you for your time and consideration.\n\nBest regards,\nKeshav"
    )

def generate(start=None, end=None):
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active
    total = ws.max_row - 1
    rs, re = start or 1, end or total
    lines = [
        "# US R1 Tier-1 Cold Email Previews\n",
        f"> Rows {rs}–{re} | Source: `US_R1_COLD_EMAIL_VAULT_V1.xlsx`\n",
        "---\n"
    ]
    for master_row in range(rs, re + 1):
        xlsx_row = master_row + 1
        if xlsx_row > ws.max_row:
            break
        cells = [ws.cell(row=xlsx_row, column=c+1).value for c in range(30)]
        doi   = cells[COL['doi']] or ""
        doi_link = f"[{doi}]({doi})" if doi.startswith("http") else doi
        body = build_body(cells)
        quoted = "\n".join(f"> {ln}" if ln else ">" for ln in body.split("\n"))
        lines += [
            f"## {master_row}. {cells[COL['first']]} {cells[COL['last']]} — {cells[COL['univ']]}\n",
            quoted, "\n",
            f"- **DOI:** {doi_link}\n",
            f"- **Year:** {cells[COL['year']]}\n",
            f"- **Venue:** {cells[COL['venue']]}\n",
            f"- **Tech Stack:** {cells[COL['tech']]}\n",
            "\n---\n"
        ]
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Written: {OUTPUT_PATH}  ({re-rs+1} entries)")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int)
    p.add_argument("--end",   type=int)
    a = p.parse_args()
    generate(a.start, a.end)
```

---

## 11. Git Commit Convention

```powershell
cd D:\Others\forGradSc\newones
git add -A
git commit -m "audit: Rows <START>-<END> | <N> DOIs verified, <M> re-synthesized

- Crossref HTTP-200 confirmed all flagship DOIs
- <M> broken DOIs replaced from OpenAlex cache and re-verified
- Tripartite findings rewritten with hard quantitative benchmarks
- Preview MD regenerated at COLD_EMAIL_PREVIEWS/"
git push origin main
```

---

*End of COLD_EMAIL_METHODOLOGY.md | Last updated: Rows 101–150 audit (US R1 Tier-1 dataset)*
