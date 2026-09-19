# Directory Inspection & Research Tools Guide

This folder contains all individual specialized testing, exploration, API inspection, and diagnostic scripts used during the development of the Arizona State University (SEMTE) faculty scraper and lab intelligence pipeline.

---

## Key Diagnostic & Extraction Scripts

### 1. Lab Intelligence & Site Scraping
* **`test_deep_lab_scrape.py`**: Prototype script that accesses faculty lab websites, searching for recruitment notices, technical prerequisites, federal funding agencies, and software repository links.
* **`inspect_lab_sites.py`**: Probes live lab websites to analyze HTML structure, navigation links, and headings.
* **`check_active_labs.py`**: Verifies lab names and research group assignments across active faculty.

### 2. Faculty Directory API & Filtering
* **`find_asu_api.py` & `test_asu.py`**: Initial reverse-engineering of the Pitchfork search widget on the SEMTE directory page.
* **`dump_asu_profs.py`**: Queries the ASU search REST endpoint with exclusion parameters to dump faculty payloads.
* **`test_faculty_filter.py` & `test_exclude.py`**: Validates filtering of non-Aero/ME faculty in SEMTE.
* **`inspect_asu_record.py`**: Dumps all 50+ raw JSON keys for an individual faculty member record.

### 3. Emeritus & Active Faculty Verification
* **`check_edu_web.py`**: Validates extraction of education credentials and lab website links while confirming strict exclusion of retired and emeritus professors.
* **`check_office_phone.py` & `test_all_offices.py`**: Inspects profile HTML microdata to extract physical office locations (campus, building, and room numbers).

### 4. Google Scholar & Citation Resolvers
* **`fetch_all_asu_scholar_ids.py`**: Iterates through ASU faculty profile pages to harvest direct 12-character Google Scholar User IDs (`user=...`).
* **`check_profile_scholar.py`**: Verifies profile HTML structures for embedded Google Scholar URLs.
* **`check_openalex_cites.py` & `inspect_openalex_author.py`**: Evaluates OpenAlex API integration for citation metrics.

---

## Running Individual Test Tools

Any tool can be executed directly with Python:

```bash
python test_deep_lab_scrape.py
python check_active_labs.py
```
