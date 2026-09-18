# R1 Aggregate Faculty Discovery Pipeline

This directory contains the multi-university automated discovery tools that query global bibliographic APIs (e.g., OpenAlex) and aggregate faculty across all Carnegie R1 research institutions.

---

## Files in this Directory

* **`scrape_all_r1_profs.py`**: The main multi-threaded script that systematically iterates through R1 universities to query OpenAlex and university endpoints.
* **`find_advisor.py`**: Heuristic matching and scoring tool to identify potential graduate advisors based on recent publication activity and keyword relevance.
* **`get_concepts.py`**: Utility to query OpenAlex concept taxonomy IDs.
* **`r1_universities.txt`**: Clean list of target Carnegie R1 Doctoral Universities (Very High Research Activity).
* **`test_openalex_stanford.py` & `test_works.py`**: Diagnostic scripts testing OpenAlex author resolution, pagination, and concept filters.
* **Aggregated Output Datasets**:
  - `r1_all_universities_faculty.xlsx`
  - `r1_professor_leads.xlsx`
  - Associated checkpoint caches
