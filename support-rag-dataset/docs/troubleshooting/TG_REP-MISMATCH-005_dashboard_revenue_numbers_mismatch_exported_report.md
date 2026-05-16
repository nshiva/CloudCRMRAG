---
doc_id: TG-REP-MISMATCH-005
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Reporting
title: "Troubleshooting: Dashboard revenue numbers mismatch exported report"
version: 1.0
last_updated: 2025-03-20
severity_default: medium
tags: ["reporting", "troubleshooting", "rep-mismatch-005"]
related_ids: ["KI-005"]
---

# Troubleshooting: Dashboard revenue numbers mismatch exported report

## When to Use This Guide
Use this guide when a customer reports symptoms related to dashboard revenue numbers mismatch exported report.

## Symptoms
- Dashboard revenue total differs from CSV export
- Customer reports incorrect monthly revenue
- Report filters appear to be ignored
- Saved dashboard and exported report show different totals

## Initial Checks
1. Confirm the customer is using an affected version: 6.3.0-6.3.1.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 6.3.2.

## Recommended Resolution
Refresh dashboard cache after applying workspace-local timezone calculation.

## Workaround
Use CSV export as the source of truth until dashboard cache refresh completes.

## When to Escalate
Escalate to Reporting Engineering if mismatch remains after cache refresh.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
