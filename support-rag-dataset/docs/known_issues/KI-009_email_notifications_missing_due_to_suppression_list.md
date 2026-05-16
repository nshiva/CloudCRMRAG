---
doc_id: KI-009
doc_type: known_issue
product: CloudDesk CRM
module: Notifications
title: "Email notifications missing due to suppression list"
status: fixed
affected_versions: "7.0.0-7.0.2"
fixed_version: "7.0.3"
last_updated: 2025-04-08
tags: ["notifications", "known-issue", "notif-email-009"]
related_ids: []
---

# Known Issue KI-009: Email notifications missing due to suppression list

## Summary
Email notifications missing due to suppression list affects CloudDesk CRM customers running versions 7.0.0-7.0.2.

## Affected Versions
- 7.0.0-7.0.2

## Fixed Version
- 7.0.3

## Common Symptoms
- Customer does not receive email notifications
- Password reset email not delivered
- Ticket assignment email missing
- Email provider shows suppressed recipient

## Root Cause
Recipients were added to the suppression list after repeated soft bounces from their mail server.

## Workaround
Ask customer IT to allowlist CloudDesk notification domains.

## Permanent Resolution
Remove the verified recipient from suppression list and send a test notification.

## Escalation Guidance
Escalate to Messaging Operations if suppression removal does not restore delivery.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
