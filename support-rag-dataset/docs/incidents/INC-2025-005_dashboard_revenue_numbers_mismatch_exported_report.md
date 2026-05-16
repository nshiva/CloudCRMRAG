---
doc_id: INC-2025-005
doc_type: incident_report
incident_id: INC-2025-005
product: CloudDesk CRM
module: Reporting
title: "Incident: Dashboard revenue numbers mismatch exported report"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["reporting", "incident", "ki-005"]
related_ids: ["KI-005"]
---

# Incident INC-2025-005: Dashboard revenue numbers mismatch exported report

## Summary
Multiple customers reported symptoms related to dashboard revenue numbers mismatch exported report.

## Impact
- Affected module: Reporting
- Affected versions: 6.3.0-6.3.1
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
Dashboard cache used UTC date boundaries while CSV export used workspace-local timezone boundaries.

## Mitigation
Use CSV export as the source of truth until dashboard cache refresh completes.

## Resolution
Refresh dashboard cache after applying workspace-local timezone calculation.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 6.3.2.

## Related Known Issue
- KI-005
