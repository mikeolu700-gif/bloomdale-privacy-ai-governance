# Phase 4B | Website Cookie Scanning and Test Evidence

## Existing baseline: retain unchanged

`BDC-OPS-003_Phase4B_Controlled_Scan_Fixture_v1.0.html` is **already in this GitHub folder**. It is a tracker-free static baseline with no working CMP or consent enforcement. A separate copy is hosted at `portfolio/cookie-scanning-test/index.html`. **Neither file is replaced by this upload.**

## New v1.1 evidence

- [`tests/run_tests.py`](tests/run_tests.py): supplied Playwright test script for the v1.1 prototype in `../Phase-3B/`.
- [`tests/mutation_check.py`](tests/mutation_check.py): supplied four-defect mutation checks.
- [`evidence/fixture_results.json`](evidence/fixture_results.json): 15 supplied prototype results.
- [`evidence/`](evidence/): F01–F15 screenshots from controlled prototype runs.

The supplied case study reports 15/15 prototype passes and detection of four planted defects. The evidence is **not** a scan of any production Meridian website. It does not demonstrate live vendor tracking, server-side GPC processing, partner suppression, or real geolocation. Production tests T01–T16 remain **Not executed**.

The earlier Word methodology `BDC-OPS-003_Phase4B_Website_Cookie_Scanning_Methodology_DRAFT_v1.0.docx` was referenced in the prior README but is **not included in the supplied v1.1 ZIP**. It remains a separate draft pending reconciliation.

## Run locally

From the `Phase-4B` directory, install Python Playwright and Chromium using the standard Playwright instructions, then execute the test scripts. Review their code and paths before running. Test results in the supplied evidence were not independently reproduced during ZIP preparation.

[Return to BDC-OPS-003](../README.md)
