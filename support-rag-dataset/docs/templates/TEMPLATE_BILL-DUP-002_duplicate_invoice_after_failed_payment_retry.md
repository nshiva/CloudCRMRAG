---
doc_id: TEMPLATE-BILL-DUP-002
doc_type: response_template
product: CloudDesk CRM
module: Billing
title: "Customer response template: Duplicate invoice after failed payment retry"
last_updated: 2025-04-16
tags: ["billing", "template", "ki-002"]
related_ids: ["KI-002"]
---

# Customer Response Template: Duplicate invoice after failed payment retry

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known billing issue.

## What we found
A race condition in the invoice finalization worker caused the retry job to treat the pending invoice as missing.

## What we have done
Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.

## Temporary workaround
Pause automated payment retry for the affected subscription until invoice state is corrected.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
