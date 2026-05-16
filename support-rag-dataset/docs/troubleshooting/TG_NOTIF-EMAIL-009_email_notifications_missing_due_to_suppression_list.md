---
doc_id: TG-NOTIF-EMAIL-009
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Notifications
title: "Troubleshooting: Email notifications missing due to suppression list"
version: 1.0
last_updated: 2025-03-24
severity_default: medium
tags: ["notifications", "troubleshooting", "notif-email-009"]
related_ids: ["KI-009"]
---

# Troubleshooting: Email notifications missing due to suppression list

## When to Use This Guide
Use this guide when a customer reports symptoms related to email notifications missing due to suppression list.

## Symptoms
- Customer does not receive email notifications
- Password reset email not delivered
- Ticket assignment email missing
- Email provider shows suppressed recipient

## Initial Checks
1. Confirm the customer is using an affected version: 7.0.0-7.0.2.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 7.0.3.

## Recommended Resolution
Remove the verified recipient from suppression list and send a test notification.

## Workaround
Ask customer IT to allowlist CloudDesk notification domains.

## When to Escalate
Escalate to Messaging Operations if suppression removal does not restore delivery.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
