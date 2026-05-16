---
doc_id: INC-2025-002
doc_type: incident_report
incident_id: INC-2025-002
product: CloudDesk CRM
module: Billing
title: "Incident: Duplicate invoice after failed payment retry"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["billing", "incident", "ki-002"]
related_ids: ["KI-002"]
---

# Incident INC-2025-002: Duplicate invoice after failed payment retry

## Summary
Multiple customers reported symptoms related to duplicate invoice after failed payment retry.

## Impact
- Affected module: Billing
- Affected versions: 2.4.0-2.4.6
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
A race condition in the invoice finalization worker caused the retry job to treat the pending invoice as missing.

## Mitigation
Pause automated payment retry for the affected subscription until invoice state is corrected.

## Resolution
Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 2.4.7.

## Related Known Issue
- KI-002
