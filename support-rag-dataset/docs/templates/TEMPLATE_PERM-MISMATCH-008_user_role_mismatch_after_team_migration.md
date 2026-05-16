---
doc_id: TEMPLATE-PERM-MISMATCH-008
doc_type: response_template
product: CloudDesk CRM
module: Permissions
title: "Customer response template: User role mismatch after team migration"
last_updated: 2025-04-28
tags: ["permissions", "template", "ki-008"]
related_ids: ["KI-008"]
---

# Customer Response Template: User role mismatch after team migration

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known permissions issue.

## What we found
Team migration copied workspace membership but did not recalculate inherited role grants.

## What we have done
Recalculate inherited permissions for the affected team and confirm role mapping.

## Temporary workaround
Manually assign the affected user to the required role until recalculation completes.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
