---
doc_id: TEMPLATE-INT-WEBHOOK-003
doc_type: response_template
product: CloudDesk CRM
module: Integrations
title: "Customer response template: Webhook delivery delay during retry storm"
last_updated: 2025-03-21
tags: ["integrations", "template", "ki-003"]
related_ids: ["KI-003"]
---

# Customer Response Template: Webhook delivery delay during retry storm

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known integrations issue.

## What we found
A retry storm occurred after third-party endpoint timeouts caused repeated retries without per-customer backoff.

## What we have done
Increase retry backoff and drain the webhook queue for the affected workspace.

## Temporary workaround
Ask the customer to temporarily reduce webhook subscription volume or disable non-critical endpoints.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
