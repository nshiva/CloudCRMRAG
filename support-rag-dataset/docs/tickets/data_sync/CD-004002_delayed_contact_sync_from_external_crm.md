---
doc_id: CD-004002
doc_type: support_ticket
ticket_id: CD-004002
product: CloudDesk CRM
module: Data Sync
title: "Delayed contact sync from external CRM - customer case 2"
customer: "NovaCloud Services"
customer_tier: enterprise
region: EU
status: resolved
severity: low
created_at: 2025-03-04
resolved_at: 2025-03-04
tags: ["data sync", "resolved", "ki-004"]
related_ids: ["KI-004", "TG-SYNC-DELAY-004"]
---

# Ticket CD-004002: Delayed contact sync from external CRM

## Customer
NovaCloud Services

## Customer Message
We are seeing this issue: Customer sees stale contact records.

Additional customer context:
- Customer tier: enterprise
- Region: EU
- Reported module: Data Sync

## Symptoms Observed
- Sync status remains in pending state
- Contacts appear several hours late
- External CRM updates do not immediately appear

## Investigation
- Support confirmed the issue belongs to the Data Sync module.
- The reported behavior matched known issue KI-004.
- The customer was running an affected version range: 4.2.0-4.2.2.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
The incremental sync cursor stalled when the external CRM returned partial pagination results.

## Resolution Applied
Reset the workspace sync cursor and restart incremental sync.

## Workaround Shared
Run a manual full sync for the affected workspace during off-peak hours.

## Final Customer Response
We reviewed the issue and confirmed it matches a known data sync behavior. 
The recommended resolution has been applied: Reset the workspace sync cursor and restart incremental sync.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 4.2.3.
