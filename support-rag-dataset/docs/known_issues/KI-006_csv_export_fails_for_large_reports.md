---
doc_id: KI-006
doc_type: known_issue
product: CloudDesk CRM
module: Reporting
title: "CSV export fails for large reports"
status: fixed
affected_versions: "6.1.0-6.1.8"
fixed_version: "6.1.9"
last_updated: 2025-02-15
tags: ["reporting", "known-issue", "exp-csv-006"]
related_ids: []
---

# Known Issue KI-006: CSV export fails for large reports

## Summary
CSV export fails for large reports affects CloudDesk CRM customers running versions 6.1.0-6.1.8.

## Affected Versions
- 6.1.0-6.1.8

## Fixed Version
- 6.1.9

## Common Symptoms
- CSV export times out
- Large report download fails
- Export job remains stuck in processing
- Customer cannot download records above 100,000 rows

## Root Cause
The export worker exceeded memory limits when generating large CSV files synchronously.

## Workaround
Ask the customer to reduce the date range or split the export by region.

## Permanent Resolution
Retry export using the asynchronous export pipeline.

## Escalation Guidance
Escalate to Reporting Operations if async export fails twice.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
