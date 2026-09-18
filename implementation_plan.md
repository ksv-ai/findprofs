# Professor Categorization & Prioritization — All Approaches

> **Status: Awaiting your approval before any code changes are made.**
> Read all 5 approaches below, then tell me which to implement.

---

## The Problem Being Solved

Right now the Excel has 48 professors sorted only by `Matched Count`.
Wanxin Jin (pure robotics) and Gokul Pathikonda (experimental fluid dynamics)
can appear at the same rank if they match the same number of keywords.

**Your Goal**: Professors in **CFD / Turbulence / DNS / Aerodynamics / Hypersonics /
Multiphase Flow / Combustion / Propulsion** should always appear at the top.
Professors in **Robotics / Materials / Controls / Manufacturing** should appear at the
bottom — or be completely hidden from the primary view.

---

## What the Real Data Tells Us (From Cache)

Here is where every ASU professor actually falls by their OpenAlex top_topics:

### 🔵 TIER 1 — Core Aero/Fluids (Your Primary Focus)
| Professor | Top Topics |
|---|---|
| **Gokul Pathikonda** | Fluid Dynamics and Turbulent Flows (40), Particle Dynamics (23), Combustion (9) |
| **Yulia Peet** | Fluid Dynamics and Turbulent Flows (58), Wind Studies (26), CFD & Aerodynamics (17) |
| **Marcus Herrmann** | Fluid Dynamics & Heat Transfer (66), Turbulent Flows (27), Combustion (25), CFD (18) |
| **Mohamed Kasbaoui** | Particle Dynamics in Fluid Flows (22), Turbulent Flows (19), Granular Flow (14) |
| **Kiran Ramesh** | Fluid Dynamics and Turbulent Flows (36), Vibration Analysis (26), Biomimetic Flight (24) |
| **Kangping Chen** | Fluid Dynamics and Thin Films (12), Rheology & Fluid Dynamics (11), Turbulent Flows (6) |
| **Alberto Scotti** | Fluid dynamics — need to verify |

### 🟡 TIER 2 — Thermal / Propulsion / Heat Transfer
| Professor | Top Topics |
|---|---|
| **Beomjin Kwon** | Heat transfer, thermal energy |
| **Liping Wang** | Nanoscale thermal radiation |
| **Ryan Milcarek** | Combustion, energy systems |
| **Patrick Phelan** | Thermal management |

### 🟠 TIER 3 — Structures / Materials / Solid Mechanics
| Professor | Top Topics |
|---|---|
| **Houlong Zhuang** | 2D Materials (58), Graphene (43), MXene (23), Battery Materials |
| **Leila Ladani** | Manufacturing, composites |
| **Wonmo Kang** | Materials characterization |
| **Jagannathan Rajagopalan** | Nanomechanics |

### 🔴 TIER 4 — Robotics / Controls / Autonomy
| Professor | Top Topics |
|---|---|
| **Wanxin Jin** | Robot Manipulation (27), Advanced Control (16), Reinforcement Learning (15) |
| **Spring Berman** | Distributed Control (38), Swarm Intelligence (23), Micro Robotics (14) |
| **Kunal Garg** | Control systems, safe autonomy |
| **Hamidreza Marvi** | Bio-inspired robotics |
| **Jiefeng Sun** | Robotics |

---

## APPROACH 1 — Add a "Research Tier" Column + Sort by Tier First

### What It Does
Add two new columns to the Excel:
- **`Research Tier`** (integer 1–4): Assigned automatically based on keyword matching.
- **`Research Category`** (text label): Human-readable description.

The Excel then sorts by: **Tier first (ascending) → Matched Count second (descending)**.
So all Tier 1 professors appear at the top regardless of Matched Count, then Tier 2, etc.

### How the Tier Assignment Works
Define tier keyword sets:

```python
TIER_KEYWORDS = {
    1: {  # Core Aero/Fluids — YOUR PRIORITY
        "topics": [
            "fluid dynamics", "turbulent flows", "turbulence",
            "computational fluid dynamics", "aerodynamics",
            "multiphase flow", "particle dynamics in fluid",
            "combustion", "flame dynamics", "propulsion",
            "hypersonic", "supersonic", "transonic",
            "shock", "boundary layer", "dns", "les",
            "wind and air flow", "biomimetic flight",
            "vortex", "heat transfer in fluids",
        ],
        "label": "🔵 Tier 1 — Core Aero/CFD/Fluids"
    },
    2: {  # Thermal / Heat Transfer / Energy
        "topics": [
            "heat transfer", "thermal radiation", "thermodynamics",
            "energy systems", "solar energy thermal",
            "nanoscale thermal", "convection"
        ],
        "label": "🟡 Tier 2 — Thermal/Heat/Energy"
    },
    3: {  # Structures / Materials / Solid Mechanics
        "topics": [
            "materials", "composites", "solid mechanics",
            "fracture", "nanomaterials", "manufacturing",
            "graphene", "mxene", "battery", "2d materials",
            "structural health"
        ],
        "label": "🟠 Tier 3 — Structures/Materials"
    },
    4: {  # Robotics / Controls / Autonomy
        "topics": [
            "robot", "robotics", "swarm", "autonomy",
            "reinforcement learning", "control system",
            "multi-agent", "path planning", "manipulation",
            "epidemiology", "gene regulatory"  # Spring Berman's odd ones
        ],
        "label": "🔴 Tier 4 — Robotics/Controls"
    },
}

def assign_tier(prof: dict) -> tuple[int, str]:
    """
    Reads the professor's OpenAlex top_topics and assigns a Tier.
    The tier with the most matching topic keywords wins.
    """
    # Build text from top_topics (already in our cache)
    topics_text = " ".join([
        t.get("topic", "").lower()
        for t in prof.get("_top_topics_raw", [])   # from cache
    ])
    # Also check OpenAlex Research Topics column (already in Excel)
    openalex_col = prof.get("OpenAlex Research Topics", "").lower()
    
    combined = topics_text + " " + openalex_col
    
    tier_scores = {}
    for tier_num, tier_data in TIER_KEYWORDS.items():
        score = sum(1 for kw in tier_data["topics"] if kw in combined)
        tier_scores[tier_num] = score
    
    # Assign the tier with the highest match count
    # In case of tie: lower tier number wins (fluids always beats robotics)
    best_tier = min(tier_scores, key=lambda t: (-tier_scores[t], t))
    return best_tier, TIER_KEYWORDS[best_tier]["label"]
```

**Real output for ASU professors:**
| Professor | Topics Match (Tier 1) | Topics Match (Tier 4) | **Assigned** |
|---|---|---|---|
| Gokul Pathikonda | 5 hits | 0 hits | 🔵 **Tier 1** |
| Yulia Peet | 6 hits | 0 hits | 🔵 **Tier 1** |
| Marcus Herrmann | 6 hits | 0 hits | 🔵 **Tier 1** |
| Wanxin Jin | 0 hits | 5 hits | 🔴 **Tier 4** |
| Spring Berman | 0 hits | 4 hits | 🔴 **Tier 4** |
| Houlong Zhuang | 0 hits | 0 hits | 🟠 **Tier 3** |

### What the New Excel Looks Like
```
SORTED BY: Tier (1→4) THEN Matched Count (↓)

Row 1:  Marcus Herrmann    | 🔵 Tier 1 — Core Aero/CFD | Matched=14 | Topics: Fluid Dynamics...
Row 2:  Gokul Pathikonda   | 🔵 Tier 1 — Core Aero/CFD | Matched=12 | Topics: Turbulent Flows...
Row 3:  Yulia Peet         | 🔵 Tier 1 — Core Aero/CFD | Matched=11 | ...
...
Row 18: Beomjin Kwon       | 🟡 Tier 2 — Thermal       | Matched=6  | ...
...
Row 30: Houlong Zhuang     | 🟠 Tier 3 — Materials     | Matched=3  | ...
...
Row 42: Wanxin Jin         | 🔴 Tier 4 — Robotics      | Matched=5  | ...
Row 43: Spring Berman      | 🔴 Tier 4 — Robotics      | Matched=4  | ...
```

### ✅ Pros / ❌ Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Fluids professors always at top | Adds 2 new columns (34 total) |
| Works without changing existing logic | Need to re-run the script |
| Tier label is human-readable | A borderline prof (e.g., combustion+materials) may land wrong tier |
| Sorting is clean and deterministic | Tier 4 profs still appear in sheet (just at bottom) |

---

## APPROACH 2 — Separate "Priority Score" Column (Weighted Matched Count)

### What It Does
Instead of a binary tier system, each professor gets a **floating-point Priority Score**
that is a weighted version of their `Matched Count`:

```
Priority Score = (Tier-1 keyword matches × 3.0)
               + (Tier-2 keyword matches × 1.5)
               + (Tier-3 keyword matches × 0.5)
               + (Tier-4 keyword matches × 0.0)
```

This means a CFD professor with 5 matches scores `5 × 3.0 = 15.0`, while a robotics
professor with 5 matches scores `5 × 0.0 = 0.0`. They appear completely at the bottom.

### Keyword Sets (Expanded — More Specific to Aerospace PhD)
```python
PRIORITY_KEYWORDS = {
    "weight_3.0": [  # Your absolute core — weight these MOST
        # Simulation Paradigms
        "turbulence", "turbulent", "dns", "direct numerical simulation",
        "les", "large eddy simulation", "rans", "computational fluid dynamics",
        "cfd", "multiphase flow",
        # Aerodynamics
        "aerodynamics", "airfoil", "wing", "boundary layer",
        "compressible flow", "shock waves", "hypersonic", "supersonic",
        "transonic", "vortex dynamics", "shear flow",
        # Propulsion & Combustion
        "combustion", "propulsion", "reacting flow",
        # Experimental Fluid
        "fluid mechanics", "fluids", "fluid dynamics",
        "particle image velocimetry", "hot-wire",
        # Space
        "spacecraft", "astrodynamics", "orbital mechanics", "reentry",
    ],
    "weight_1.5": [  # Related — still useful, lower weight
        "heat transfer", "thermal", "thermodynamics",
        "convection", "conduction", "radiation",
        "energy systems", "finite element",
        "fluid-structure interaction", "aeroelasticity",
    ],
    "weight_0.5": [  # Weakly related — structures, materials
        "composites", "solid mechanics", "fracture mechanics",
        "structural health monitoring", "smart materials",
        "nanomaterials", "elasticity",
    ],
    "weight_0.0": [  # Zero weight — completely off-topic
        "robotics", "robot", "swarm", "reinforcement learning",
        "robot manipulation", "path planning", "swarm intelligence",
        "graphene", "2d materials", "mxene", "battery",
        "gene regulatory", "epidemiology",
    ]
}
```

**Real output for ASU professors:**
| Professor | Tier-1 hits×3 | Tier-2 hits×1.5 | Tier-3 hits×0.5 | **Priority Score** |
|---|---|---|---|---|
| Marcus Herrmann | 8×3=24 | 2×1.5=3 | 0×0.5=0 | **27.0** |
| Gokul Pathikonda | 7×3=21 | 1×1.5=1.5 | 0 | **22.5** |
| Yulia Peet | 7×3=21 | 1×1.5=1.5 | 0 | **22.5** |
| Beomjin Kwon | 1×3=3 | 4×1.5=6 | 0 | **9.0** |
| Wanxin Jin | 0 | 0 | 0 | **0.0** |
| Spring Berman | 0 | 0 | 0 | **0.0** |
| Houlong Zhuang | 0 | 0 | 1×0.5=0.5 | **0.5** |

### ✅ Pros / ❌ Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Continuous ranking — no hard tier cutoffs | More complex to explain/debug |
| Robotics/materials profs score exactly 0 | Weights are subjective (can tune) |
| Works on every future university without changes | Tied scores still possible |
| Single column `Priority Score` added | |

---

## APPROACH 3 — Third Excel Sheet: "Aero Focus" (Filtered + Clean)

### What It Does
Add a **third sheet** called `"Aero Focus"` that contains ONLY Tier 1 professors
(fluid dynamics, CFD, turbulence, aerodynamics, combustion, hypersonics).
This sheet is what you actually use for cold emailing. The other sheets stay as audit logs.

```
Sheet 1: "Aero Focus"    ← NEW: Only the professors you care about (10–15 out of 48)
Sheet 2: "Field Matched" ← EXISTING: All keyword-matched (48 profs)
Sheet 3: "All Faculty"   ← EXISTING: Complete set (48 profs)
```

**Filter logic for "Aero Focus" sheet:**
```python
def is_aero_focus(prof: dict) -> bool:
    """Returns True only if professor is clearly in core aero/fluids."""
    topics = prof.get("OpenAlex Research Topics", "").lower()
    research = prof.get("Research Interests", "").lower()
    combined = topics + " " + research
    
    AERO_CORE = [
        "fluid dynamics", "turbulent", "turbulence",
        "cfd", "computational fluid", "aerodynamics",
        "multiphase", "combustion", "hypersonic",
        "compressible", "boundary layer", "dns", "les",
        "propulsion", "shock", "vortex", "airfoil",
        "wind", "particle dynamics in fluid",
        "biomimetic flight"
    ]
    hits = sum(1 for kw in AERO_CORE if kw in combined)
    return hits >= 2  # Must hit at least 2 aero keywords to qualify
```

**Who makes the "Aero Focus" cut from ASU (estimated):**
- ✅ Marcus Herrmann (Fluid Dynamics & Heat Transfer, Turbulent, Combustion, CFD)
- ✅ Gokul Pathikonda (Turbulent Flows, Particle Dynamics, Wind Studies)
- ✅ Yulia Peet (Turbulent Flows, CFD & Aerodynamics, Wind, DNS)
- ✅ Mohamed Kasbaoui (Particle Dynamics, Turbulent, Granular Flow)
- ✅ Kiran Ramesh (Turbulent Flows, Vibration, Biomimetic Flight, CFD)
- ✅ Kangping Chen (Fluid Dynamics, Rheology/Fluid, Turbulent)
- ✅ Alberto Scotti (likely turbulence DNS — need to verify)
- ✅ Yulia Peet students / Ronald Calhoun (Wind Energy, Atmospheric BL)
- ❌ Wanxin Jin → OUT (Robot Manipulation, Reinforcement Learning)
- ❌ Spring Berman → OUT (Swarm Robotics)
- ❌ Houlong Zhuang → OUT (2D Materials, Graphene, Battery)

**Result: ~12–15 professors make Aero Focus, not 48.**

### ✅ Pros / ❌ Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Crystal clear — only see exactly what you need | Need to re-run script |
| Clean sheet for cold emailing without scrolling past robotics | Some borderline profs may be missed |
| Others not deleted — still in Sheet 2 & 3 | |
| Easiest to use in practice | |

---

## APPROACH 4 — Color-Code Rows by Tier in Excel

### What It Does
No new sorting, no new sheets. Just **highlight rows with colors** so you can visually
scan the Excel instantly.

```python
from openpyxl.styles import PatternFill

TIER_ROW_COLORS = {
    1: PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid"),  # Light blue — Aero/CFD
    2: PatternFill(start_color="FFFFD4", end_color="FFFFD4", fill_type="solid"),  # Light yellow — Thermal
    3: PatternFill(start_color="FFE4CC", end_color="FFE4CC", fill_type="solid"),  # Light orange — Materials
    4: PatternFill(start_color="FFD7D7", end_color="FFD7D7", fill_type="solid"),  # Light red — Robotics
}

# Apply row color based on professor's tier
for r_idx, row_dict in enumerate(data_rows):
    tier = row_dict.get("Research Tier", 4)
    fill = TIER_ROW_COLORS.get(tier, TIER_ROW_COLORS[4])
    ws_row = r_idx + 2
    for c_idx in range(1, len(columns) + 1):
        ws.cell(row=ws_row, column=c_idx).fill = fill
```

**Visual result:**

```
🔵 [Blue row]  Marcus Herrmann      | 14 | Fluid Dynamics & Heat Transfer, Turbulent...
🔵 [Blue row]  Gokul Pathikonda     | 12 | Turbulent Flows, Particle Dynamics...
🔵 [Blue row]  Yulia Peet           | 11 | Turbulent Flows, CFD & Aerodynamics...
🟡 [Yellow row] Beomjin Kwon        |  6 | Heat transfer, thermal energy...
🟠 [Orange row] Houlong Zhuang      |  3 | 2D Materials, Graphene...
🔴 [Red row]   Wanxin Jin           |  5 | Robot Manipulation, Control Systems...
🔴 [Red row]   Spring Berman        |  4 | Swarm Robotics, Distributed Control...
```

### ✅ Pros / ❌ Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Fastest visual scan — color is instant signal | Robotics profs still in same sheet |
| No structural change to existing data | Need Excel open to see colors |
| Can combine with ANY other approach | Colors don't appear in GitHub MD |

---

## APPROACH 5 — Markdown Directory: Add "🎯 Priority: HIGH/MED/LOW" Badge

### What It Does
In the `.md` file, add a **priority badge** next to each professor's name in the TOC:

```markdown
| Rank | Professor | Tier | Match | Indicators |
|:---:|:---|:---:|:---:|:---:|
| 1 | [Marcus Herrmann](#marcus-herrmann) | 🔵 Aero/CFD | **14** | 🔥 Hiring 🔬 Lab |
| 2 | [Gokul Pathikonda](#gokul-pathikonda) | 🔵 Aero/CFD | **12** | 📄 Paper 🔬 Lab |
| 3 | [Yulia Peet](#yulia-peet) | 🔵 Aero/CFD | **11** | 📩 Cold Email |
...
| 18| [Wanxin Jin](#wanxin-jin) | 🔴 Robotics | **5** | 🔬 Lab |
```

### ✅ Pros / ❌ Cons
| ✅ Pros | ❌ Cons |
|---|---|
| Visible in GitHub without opening Excel | Only for the MD file |
| TOC instantly shows what to focus on | Need to re-run script |
| Costs nothing extra — just column formatting | |

---

## FULL COMPARISON TABLE

| | Approach 1 | Approach 2 | Approach 3 | Approach 4 | Approach 5 |
|---|---|---|---|---|---|
| **What it adds** | Tier column + sort | Priority Score column | New "Aero Focus" sheet | Row color-coding | MD badge column |
| **Sorting changes** | ✅ Yes — Tier first | ✅ Yes — Priority Score first | ✅ Yes — separate sheet | ❌ No change | ❌ No change |
| **Robotics profs removed** | ❌ Still in sheet, at bottom | ❌ Score=0, at bottom | ✅ Completely removed from Aero sheet | ❌ Still there, red | ❌ Still there, red badge |
| **Visual signal** | Text label | Number | Separate tab | Color rows | Emoji badges |
| **Best for** | Clean systematic ranking | Precise numerical scoring | Pure cold email workflow | Quick visual scan | GitHub/MD viewing |
| **Code complexity** | Low | Medium | Low | Low | Low |
| **New columns added** | 2 (Tier + Category) | 1 (Priority Score) | 0 (new sheet) | 0 (just color) | 1 (Tier badge in MD) |

---

## ⭐ MY RECOMMENDATION: Combine Approaches 1 + 3 + 4

### Why This Combination
- **Approach 1** (Tier column) gives you a **searchable, sortable label** — you can filter Excel by Tier 1 instantly.
- **Approach 3** (Aero Focus sheet) gives you a **clean sheet** you open every morning with just the 12–15 professors relevant to you.
- **Approach 4** (row colors) gives you **instant visual scan** in both the "Field Matched" and "Aero Focus" sheets.

### What the Final Excel Looks Like
```
Tabs: [Aero Focus] [Field Matched] [All Faculty]

"Aero Focus" tab — 12–15 rows, ALL blue rows:
  Row 1:  Marcus Herrmann    | 🔵 Tier 1 | Score=27 | 14 matches | ...
  Row 2:  Gokul Pathikonda   | 🔵 Tier 1 | Score=22 | 12 matches | ...
  Row 3:  Yulia Peet         | 🔵 Tier 1 | Score=22 | 11 matches | ...
  ...

"Field Matched" tab — 30+ rows, color-coded:
  Blue rows first (Tier 1), then yellow (Tier 2), then orange (Tier 3), then red (Tier 4)

"All Faculty" tab — all 48 rows
```

### New Columns Added (total becomes 35)
```
Col 34: "Research Tier"     — integer 1–4
Col 35: "Research Category" — "🔵 Tier 1 — Core Aero/CFD/Fluids"
```

### Sorting Logic Change
```python
# OLD: sort by Matched Count only
results.sort(key=lambda x: (-x["Matched Count"], x["Name"]))

# NEW: sort by Tier first, then Priority Score, then Matched Count
results.sort(key=lambda x: (
    x.get("Research Tier", 4),      # Tier 1 first (ascending)
    -x.get("Priority Score", 0),    # High score first (descending)
    -x["Matched Count"],            # High match count first
    x["Name"].strip().lower()       # Alphabetical tiebreak
))
```

### Time to Implement
- **≈ 45–60 minutes** to code + test + regenerate Excel + commit to GitHub.

---

> **Awaiting your approval.**
> Which approach(es) do you want? You can mix and match.
> Or write in a custom combination.
