---
doc_id: CD-002003
doc_type: support_ticket
ticket_id: CD-002003
product: CloudDesk CRM
module: Billing
title: "Duplicate invoice after failed payment retry - customer case 3"
customer: "Summit Foods"
customer_tier: startup
region: US
status: resolved
severity: low
created_at: 2025-01-18
resolved_at: 2025-01-18
tags: ["billing", "resolved", "ki-002"]
related_ids: ["KI-002", "TG-BILL-DUP-002"]
---

# Ticket CD-002003: Duplicate invoice after failed payment retry

## Customer
Summit Foods

## Customer Message
Can you check why finance team sees duplicate payable invoice for our workspace?

Additional customer context:
- Customer tier: startup
- Region: US
- Reported module: Billing

## Symptoms Observed
- Two invoices for the same billing period
- Duplicate draft invoice appears after failed payment retry
- Customer says they were charged twice

## Investigation
- Support confirmed the issue belongs to the Billing module.
- The reported behavior matched known issue KI-002.
- The customer was running an affected version range: 2.4.0-2.4.6.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
A race condition in the invoice finalization worker caused the retry job to treat the pending invoice as missing.

## Resolution Applied
Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.

## Workaround Shared
Pause automated payment retry for the affected subscription until invoice state is corrected.

## Final Customer Response
We reviewed the issue and confirmed it matches a known billing behavior. 
The recommended resolution has been applied: Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 2.4.7.
