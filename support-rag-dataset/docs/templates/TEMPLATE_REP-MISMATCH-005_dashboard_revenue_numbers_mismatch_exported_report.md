---
doc_id: TEMPLATE-REP-MISMATCH-005
doc_type: response_template
product: CloudDesk CRM
module: Reporting
title: "Customer response template: Dashboard revenue numbers mismatch exported report"
last_updated: 2025-03-20
tags: ["reporting", "template", "ki-005"]
related_ids: ["KI-005"]
---

# Customer Response Template: Dashboard revenue numbers mismatch exported report

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known reporting issue.

## What we found
Dashboard cache used UTC date boundaries while CSV export used workspace-local timezone boundaries.

## What we have done
Refresh dashboard cache after applying workspace-local timezone calculation.

## Temporary workaround
Use CSV export as the source of truth until dashboard cache refresh completes.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
