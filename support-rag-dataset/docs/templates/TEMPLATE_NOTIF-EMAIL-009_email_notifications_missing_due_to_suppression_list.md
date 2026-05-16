---
doc_id: TEMPLATE-NOTIF-EMAIL-009
doc_type: response_template
product: CloudDesk CRM
module: Notifications
title: "Customer response template: Email notifications missing due to suppression list"
last_updated: 2025-04-14
tags: ["notifications", "template", "ki-009"]
related_ids: ["KI-009"]
---

# Customer Response Template: Email notifications missing due to suppression list

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known notifications issue.

## What we found
Recipients were added to the suppression list after repeated soft bounces from their mail server.

## What we have done
Remove the verified recipient from suppression list and send a test notification.

## Temporary workaround
Ask customer IT to allowlist CloudDesk notification domains.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
