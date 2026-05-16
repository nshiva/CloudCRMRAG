---
doc_id: TEMPLATE-API-RATE-010
doc_type: response_template
product: CloudDesk CRM
module: Performance
title: "Customer response template: API requests fail due to rate limit confusion"
last_updated: 2025-04-20
tags: ["performance", "template", "ki-010"]
related_ids: ["KI-010"]
---

# Customer Response Template: API requests fail due to rate limit confusion

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known performance issue.

## What we found
Customers exceeded the per-minute workspace API limit, and retry logic did not respect Retry-After headers.

## What we have done
Update integration retry logic to honor Retry-After headers and reduce batch size.

## Temporary workaround
Temporarily lower request concurrency and schedule bulk imports during off-peak hours.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
