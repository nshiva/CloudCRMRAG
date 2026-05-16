---
doc_id: KI-005
doc_type: known_issue
product: CloudDesk CRM
module: Reporting
title: "Dashboard revenue numbers mismatch exported report"
status: fixed
affected_versions: "6.3.0-6.3.1"
fixed_version: "6.3.2"
last_updated: 2025-02-03
tags: ["reporting", "known-issue", "rep-mismatch-005"]
related_ids: []
---

# Known Issue KI-005: Dashboard revenue numbers mismatch exported report

## Summary
Dashboard revenue numbers mismatch exported report affects CloudDesk CRM customers running versions 6.3.0-6.3.1.

## Affected Versions
- 6.3.0-6.3.1

## Fixed Version
- 6.3.2

## Common Symptoms
- Dashboard revenue total differs from CSV export
- Customer reports incorrect monthly revenue
- Report filters appear to be ignored
- Saved dashboard and exported report show different totals

## Root Cause
Dashboard cache used UTC date boundaries while CSV export used workspace-local timezone boundaries.

## Workaround
Use CSV export as the source of truth until dashboard cache refresh completes.

## Permanent Resolution
Refresh dashboard cache after applying workspace-local timezone calculation.

## Escalation Guidance
Escalate to Reporting Engineering if mismatch remains after cache refresh.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
