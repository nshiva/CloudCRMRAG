---
doc_id: INC-2025-008
doc_type: incident_report
incident_id: INC-2025-008
product: CloudDesk CRM
module: Permissions
title: "Incident: User role mismatch after team migration"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["permissions", "incident", "ki-008"]
related_ids: ["KI-008"]
---

# Incident INC-2025-008: User role mismatch after team migration

## Summary
Multiple customers reported symptoms related to user role mismatch after team migration.

## Impact
- Affected module: Permissions
- Affected versions: 3.5.0-3.5.3
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
Team migration copied workspace membership but did not recalculate inherited role grants.

## Mitigation
Manually assign the affected user to the required role until recalculation completes.

## Resolution
Recalculate inherited permissions for the affected team and confirm role mapping.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 3.5.4.

## Related Known Issue
- KI-008
