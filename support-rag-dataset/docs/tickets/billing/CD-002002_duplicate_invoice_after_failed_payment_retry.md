---
doc_id: CD-002002
doc_type: support_ticket
ticket_id: CD-002002
product: CloudDesk CRM
module: Billing
title: "Duplicate invoice after failed payment retry - customer case 2"
customer: "Northstar Logistics"
customer_tier: enterprise
region: APAC
status: resolved
severity: low
created_at: 2025-03-20
resolved_at: 2025-03-20
tags: ["billing", "resolved", "ki-002"]
related_ids: ["KI-002", "TG-BILL-DUP-002"]
---

# Ticket CD-002002: Duplicate invoice after failed payment retry

## Customer
Northstar Logistics

## Customer Message
This started today and appears related to duplicate invoice after failed payment retry.

Additional customer context:
- Customer tier: enterprise
- Region: APAC
- Reported module: Billing

## Symptoms Observed
- Duplicate draft invoice appears after failed payment retry
- Customer says they were charged twice
- Two invoices for the same billing period

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
