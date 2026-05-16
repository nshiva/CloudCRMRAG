---
doc_id: TEMPLATE-EXP-CSV-006
doc_type: response_template
product: CloudDesk CRM
module: Reporting
title: "Customer response template: CSV export fails for large reports"
last_updated: 2025-03-27
tags: ["reporting", "template", "ki-006"]
related_ids: ["KI-006"]
---

# Customer Response Template: CSV export fails for large reports

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known reporting issue.

## What we found
The export worker exceeded memory limits when generating large CSV files synchronously.

## What we have done
Retry export using the asynchronous export pipeline.

## Temporary workaround
Ask the customer to reduce the date range or split the export by region.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
