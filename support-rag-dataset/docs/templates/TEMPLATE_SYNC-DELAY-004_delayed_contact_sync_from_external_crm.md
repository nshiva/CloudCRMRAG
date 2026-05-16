---
doc_id: TEMPLATE-SYNC-DELAY-004
doc_type: response_template
product: CloudDesk CRM
module: Data Sync
title: "Customer response template: Delayed contact sync from external CRM"
last_updated: 2025-03-31
tags: ["data sync", "template", "ki-004"]
related_ids: ["KI-004"]
---

# Customer Response Template: Delayed contact sync from external CRM

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known data sync issue.

## What we found
The incremental sync cursor stalled when the external CRM returned partial pagination results.

## What we have done
Reset the workspace sync cursor and restart incremental sync.

## Temporary workaround
Run a manual full sync for the affected workspace during off-peak hours.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
