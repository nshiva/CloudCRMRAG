---
doc_id: CD-009005
doc_type: support_ticket
ticket_id: CD-009005
product: CloudDesk CRM
module: Notifications
title: "Email notifications missing due to suppression list - customer case 5"
customer: "Atlas Learning"
customer_tier: growth
region: US
status: resolved
severity: medium
created_at: 2025-01-01
resolved_at: 2025-01-01
tags: ["notifications", "resolved", "ki-009"]
related_ids: ["KI-009", "TG-NOTIF-EMAIL-009"]
---

# Ticket CD-009005: Email notifications missing due to suppression list

## Customer
Atlas Learning

## Customer Message
This started today and appears related to email notifications missing due to suppression list.

Additional customer context:
- Customer tier: growth
- Region: US
- Reported module: Notifications

## Symptoms Observed
- Email provider shows suppressed recipient
- Ticket assignment email missing
- Customer does not receive email notifications

## Investigation
- Support confirmed the issue belongs to the Notifications module.
- The reported behavior matched known issue KI-009.
- The customer was running an affected version range: 7.0.0-7.0.2.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
Recipients were added to the suppression list after repeated soft bounces from their mail server.

## Resolution Applied
Remove the verified recipient from suppression list and send a test notification.

## Workaround Shared
Ask customer IT to allowlist CloudDesk notification domains.

## Final Customer Response
We reviewed the issue and confirmed it matches a known notifications behavior. 
The recommended resolution has been applied: Remove the verified recipient from suppression list and send a test notification.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 7.0.3.
