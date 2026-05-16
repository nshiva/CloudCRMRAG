---
doc_id: INC-2025-006
doc_type: incident_report
incident_id: INC-2025-006
product: CloudDesk CRM
module: Reporting
title: "Incident: CSV export fails for large reports"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["reporting", "incident", "ki-006"]
related_ids: ["KI-006"]
---

# Incident INC-2025-006: CSV export fails for large reports

## Summary
Multiple customers reported symptoms related to csv export fails for large reports.

## Impact
- Affected module: Reporting
- Affected versions: 6.1.0-6.1.8
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
The export worker exceeded memory limits when generating large CSV files synchronously.

## Mitigation
Ask the customer to reduce the date range or split the export by region.

## Resolution
Retry export using the asynchronous export pipeline.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 6.1.9.

## Related Known Issue
- KI-006
