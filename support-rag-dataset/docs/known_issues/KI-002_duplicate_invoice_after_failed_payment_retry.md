---
doc_id: KI-002
doc_type: known_issue
product: CloudDesk CRM
module: Billing
title: "Duplicate invoice after failed payment retry"
status: fixed
affected_versions: "2.4.0-2.4.6"
fixed_version: "2.4.7"
last_updated: 2025-03-24
tags: ["billing", "known-issue", "bill-dup-002"]
related_ids: []
---

# Known Issue KI-002: Duplicate invoice after failed payment retry

## Summary
Duplicate invoice after failed payment retry affects CloudDesk CRM customers running versions 2.4.0-2.4.6.

## Affected Versions
- 2.4.0-2.4.6

## Fixed Version
- 2.4.7

## Common Symptoms
- Two invoices for the same billing period
- Customer says they were charged twice
- Finance team sees duplicate payable invoice
- Duplicate draft invoice appears after failed payment retry

## Root Cause
A race condition in the invoice finalization worker caused the retry job to treat the pending invoice as missing.

## Workaround
Pause automated payment retry for the affected subscription until invoice state is corrected.

## Permanent Resolution
Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.

## Escalation Guidance
Escalate to Billing Operations if the duplicate invoice cannot be voided by support.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
