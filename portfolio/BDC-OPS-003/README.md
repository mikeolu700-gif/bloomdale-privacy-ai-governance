# BDC-OPS-003 | Cookie Consent, GPC and Website Tracking Governance

**BloomDale Capital LLC | Meridian Digital Holdings (fictional) | Portfolio demonstration**  
**Consolidated case study:** v1.1, 15 November 2026  
**Release decision:** **PRODUCTION HOLD**

## What is demonstrated

A fictional multi-jurisdiction consent management operating model spanning UK/EEA device access rules and applicable US state opt-out requirements. The case study links consent and GPC to the wider BDC-PRIV-001 and BDC-OPS-002 portfolio scenarios. All enterprise sites, risks, tracker inventory and findings are synthetic.

The self-contained prototype was reported as **15/15 passing automated Chromium checks** in the supplied v1.1 evidence; these are **prototype-only results**, not independently rerun as part of this repository packaging. Four mutation cases are described in the accompanying case study and scripts. **No production Meridian website has been tested.** The case study reports **0/16 production tests executed, 0/11 controls production-verified, and three Critical inherent risks still open**.

## Files and locations

- [`BDC-OPS-003_Consolidated_Consent_Tracking_Case_Study_v1.1.pdf`](BDC-OPS-003_Consolidated_Consent_Tracking_Case_Study_v1.1.pdf): primary 10-page case study.
- [`BDC-OPS-003_Consolidated_Consent_Tracking_Case_Study_v1.1.docx`](BDC-OPS-003_Consolidated_Consent_Tracking_Case_Study_v1.1.docx): editable companion.
- [`Phase-3B/`](Phase-3B/): interactive v1.1 consent banner/preference-center prototype and its README.
- [`Phase-4A/`](Phase-4A/): consolidated v1.1 compliance workbook and its README.
- [`Phase-4B/`](Phase-4B/): existing static baseline fixture (retain it), test scripts, screenshot evidence and fixture results; see README.

## Version reconciliation

Earlier Phase 3B and Phase 4A/4B README files described **v1.0 drafts** and stated that no browser tests had run. These README files have been revised to reflect the **new v1.1 prototype evidence** while keeping all production test statuses **Not executed**. The earlier Phase 4A v1.0 draft workbook and Phase 4B methodology are **not included in this uploaded v1.1 package** and should not be represented as uploaded or superseded without a separate review.

The existing `portfolio/cookie-scanning-test/index.html` and `Phase-4B/BDC-OPS-003_Phase4B_Controlled_Scan_Fixture_v1.0.html` are intentionally **not overwritten**. They remain tracker-free baseline pages. The v1.1 prototype is a separate file with harmless mock `.invalid` requests. Do not replace the public test page automatically.

## Limitations

GPC and region were simulated in the automated tests. The prototype does not verify server-side opt-out propagation, partner suppression, geolocation, live tags or HIPAA portal handling. Local browser storage is not an enterprise consent audit record. This portfolio demonstration is not legal advice or a claim of OneTrust affiliation.
