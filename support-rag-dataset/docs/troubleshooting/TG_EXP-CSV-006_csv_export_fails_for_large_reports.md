---
doc_id: TG-EXP-CSV-006
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Reporting
title: "Troubleshooting: CSV export fails for large reports"
version: 1.0
last_updated: 2025-03-14
severity_default: medium
tags: ["reporting", "troubleshooting", "exp-csv-006"]
related_ids: ["KI-006"]
---

# Troubleshooting: CSV export fails for large reports

## When to Use This Guide
Use this guide when a customer reports symptoms related to csv export fails for large reports.

## Symptoms
- CSV export times out
- Large report download fails
- Export job remains stuck in processing
- Customer cannot download records above 100,000 rows

## Initial Checks
1. Confirm the customer is using an affected version: 6.1.0-6.1.8.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 6.1.9.

## Recommended Resolution
Retry export using the asynchronous export pipeline.

## Workaround
Ask the customer to reduce the date range or split the export by region.

## When to Escalate
Escalate to Reporting Operations if async export fails twice.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
