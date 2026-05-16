---
doc_id: TG-BILL-DUP-002
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Billing
title: "Troubleshooting: Duplicate invoice after failed payment retry"
version: 1.0
last_updated: 2025-04-25
severity_default: medium
tags: ["billing", "troubleshooting", "bill-dup-002"]
related_ids: ["KI-002"]
---

# Troubleshooting: Duplicate invoice after failed payment retry

## When to Use This Guide
Use this guide when a customer reports symptoms related to duplicate invoice after failed payment retry.

## Symptoms
- Two invoices for the same billing period
- Customer says they were charged twice
- Finance team sees duplicate payable invoice
- Duplicate draft invoice appears after failed payment retry

## Initial Checks
1. Confirm the customer is using an affected version: 2.4.0-2.4.6.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 2.4.7.

## Recommended Resolution
Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.

## Workaround
Pause automated payment retry for the affected subscription until invoice state is corrected.

## When to Escalate
Escalate to Billing Operations if the duplicate invoice cannot be voided by support.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
