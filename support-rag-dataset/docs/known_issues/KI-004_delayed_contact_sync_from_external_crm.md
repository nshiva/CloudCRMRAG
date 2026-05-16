---
doc_id: KI-004
doc_type: known_issue
product: CloudDesk CRM
module: Data Sync
title: "Delayed contact sync from external CRM"
status: fixed
affected_versions: "4.2.0-4.2.2"
fixed_version: "4.2.3"
last_updated: 2025-04-14
tags: ["data sync", "known-issue", "sync-delay-004"]
related_ids: []
---

# Known Issue KI-004: Delayed contact sync from external CRM

## Summary
Delayed contact sync from external CRM affects CloudDesk CRM customers running versions 4.2.0-4.2.2.

## Affected Versions
- 4.2.0-4.2.2

## Fixed Version
- 4.2.3

## Common Symptoms
- Contacts appear several hours late
- Customer sees stale contact records
- Sync status remains in pending state
- External CRM updates do not immediately appear

## Root Cause
The incremental sync cursor stalled when the external CRM returned partial pagination results.

## Workaround
Run a manual full sync for the affected workspace during off-peak hours.

## Permanent Resolution
Reset the workspace sync cursor and restart incremental sync.

## Escalation Guidance
Escalate to Data Platform if full sync fails or duplicate records are created.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
