---
doc_id: INC-2025-003
doc_type: incident_report
incident_id: INC-2025-003
product: CloudDesk CRM
module: Integrations
title: "Incident: Webhook delivery delay during retry storm"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["integrations", "incident", "ki-003"]
related_ids: ["KI-003"]
---

# Incident INC-2025-003: Webhook delivery delay during retry storm

## Summary
Multiple customers reported symptoms related to webhook delivery delay during retry storm.

## Impact
- Affected module: Integrations
- Affected versions: 5.0.0-5.0.3
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
A retry storm occurred after third-party endpoint timeouts caused repeated retries without per-customer backoff.

## Mitigation
Ask the customer to temporarily reduce webhook subscription volume or disable non-critical endpoints.

## Resolution
Increase retry backoff and drain the webhook queue for the affected workspace.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 5.0.4.

## Related Known Issue
- KI-003
