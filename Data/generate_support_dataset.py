from pathlib import Path
import json
import random
from datetime import datetime, timedelta

BASE_DIR = Path("support-rag-dataset")

PRODUCT_NAME = "CloudDesk CRM"

random.seed(42)


ISSUE_CLUSTERS = [
    {
        "cluster_id": "AUTH-SSO-001",
        "module": "Authentication",
        "title": "SSO login failure after identity provider certificate rotation",
        "known_issue_id": "KI-001",
        "affected_versions": "3.1.0-3.1.4",
        "fixed_version": "3.1.5",
        "symptoms": [
            "Invalid SAML response error",
            "Users redirected back to login page",
            "SSO login fails while password login works",
            "Only users from one identity provider are affected"
        ],
        "root_cause": "The identity provider signing certificate was rotated, but CloudDesk still had the previous certificate cached.",
        "resolution": "Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.",
        "workaround": "Temporarily enable password login for affected users if allowed by the customer's security policy.",
        "escalation": "Escalate to Security Engineering if SAML response validation fails after certificate refresh."
    },
    {
        "cluster_id": "BILL-DUP-002",
        "module": "Billing",
        "title": "Duplicate invoice after failed payment retry",
        "known_issue_id": "KI-002",
        "affected_versions": "2.4.0-2.4.6",
        "fixed_version": "2.4.7",
        "symptoms": [
            "Two invoices for the same billing period",
            "Customer says they were charged twice",
            "Finance team sees duplicate payable invoice",
            "Duplicate draft invoice appears after failed payment retry"
        ],
        "root_cause": "A race condition in the invoice finalization worker caused the retry job to treat the pending invoice as missing.",
        "resolution": "Void the duplicate invoice and confirm that the original invoice remains linked to the subscription.",
        "workaround": "Pause automated payment retry for the affected subscription until invoice state is corrected.",
        "escalation": "Escalate to Billing Operations if the duplicate invoice cannot be voided by support."
    },
    {
        "cluster_id": "INT-WEBHOOK-003",
        "module": "Integrations",
        "title": "Webhook delivery delay during retry storm",
        "known_issue_id": "KI-003",
        "affected_versions": "5.0.0-5.0.3",
        "fixed_version": "5.0.4",
        "symptoms": [
            "Webhook events arrive late",
            "Customer reports missing webhook callbacks",
            "Webhook retry queue grows rapidly",
            "Third-party integration receives duplicate retries"
        ],
        "root_cause": "A retry storm occurred after third-party endpoint timeouts caused repeated retries without per-customer backoff.",
        "resolution": "Increase retry backoff and drain the webhook queue for the affected workspace.",
        "workaround": "Ask the customer to temporarily reduce webhook subscription volume or disable non-critical endpoints.",
        "escalation": "Escalate to Integrations Engineering if queue depth exceeds 50,000 events."
    },
    {
        "cluster_id": "SYNC-DELAY-004",
        "module": "Data Sync",
        "title": "Delayed contact sync from external CRM",
        "known_issue_id": "KI-004",
        "affected_versions": "4.2.0-4.2.2",
        "fixed_version": "4.2.3",
        "symptoms": [
            "Contacts appear several hours late",
            "Customer sees stale contact records",
            "Sync status remains in pending state",
            "External CRM updates do not immediately appear"
        ],
        "root_cause": "The incremental sync cursor stalled when the external CRM returned partial pagination results.",
        "resolution": "Reset the workspace sync cursor and restart incremental sync.",
        "workaround": "Run a manual full sync for the affected workspace during off-peak hours.",
        "escalation": "Escalate to Data Platform if full sync fails or duplicate records are created."
    },
    {
        "cluster_id": "REP-MISMATCH-005",
        "module": "Reporting",
        "title": "Dashboard revenue numbers mismatch exported report",
        "known_issue_id": "KI-005",
        "affected_versions": "6.3.0-6.3.1",
        "fixed_version": "6.3.2",
        "symptoms": [
            "Dashboard revenue total differs from CSV export",
            "Customer reports incorrect monthly revenue",
            "Report filters appear to be ignored",
            "Saved dashboard and exported report show different totals"
        ],
        "root_cause": "Dashboard cache used UTC date boundaries while CSV export used workspace-local timezone boundaries.",
        "resolution": "Refresh dashboard cache after applying workspace-local timezone calculation.",
        "workaround": "Use CSV export as the source of truth until dashboard cache refresh completes.",
        "escalation": "Escalate to Reporting Engineering if mismatch remains after cache refresh."
    },
    {
        "cluster_id": "EXP-CSV-006",
        "module": "Reporting",
        "title": "CSV export fails for large reports",
        "known_issue_id": "KI-006",
        "affected_versions": "6.1.0-6.1.8",
        "fixed_version": "6.1.9",
        "symptoms": [
            "CSV export times out",
            "Large report download fails",
            "Export job remains stuck in processing",
            "Customer cannot download records above 100,000 rows"
        ],
        "root_cause": "The export worker exceeded memory limits when generating large CSV files synchronously.",
        "resolution": "Retry export using the asynchronous export pipeline.",
        "workaround": "Ask the customer to reduce the date range or split the export by region.",
        "escalation": "Escalate to Reporting Operations if async export fails twice."
    },
    {
        "cluster_id": "SLACK-INT-007",
        "module": "Integrations",
        "title": "Slack integration stops posting ticket updates",
        "known_issue_id": "KI-007",
        "affected_versions": "5.2.0-5.2.5",
        "fixed_version": "5.2.6",
        "symptoms": [
            "Slack notifications are not posted",
            "Ticket updates no longer appear in channel",
            "Slack integration shows connected but inactive",
            "Customer receives authorization revoked error"
        ],
        "root_cause": "Slack OAuth tokens were revoked after workspace permission changes, but CloudDesk did not prompt reauthorization.",
        "resolution": "Ask the customer admin to reconnect Slack integration and reselect the target channels.",
        "workaround": "Use email notifications until Slack integration is reauthorized.",
        "escalation": "Escalate to Integrations Support if reconnect flow fails."
    },
    {
        "cluster_id": "PERM-MISMATCH-008",
        "module": "Permissions",
        "title": "User role mismatch after team migration",
        "known_issue_id": "KI-008",
        "affected_versions": "3.5.0-3.5.3",
        "fixed_version": "3.5.4",
        "symptoms": [
            "User cannot access expected team records",
            "Admin role appears as agent role",
            "Permissions differ after team migration",
            "User sees access denied for shared dashboards"
        ],
        "root_cause": "Team migration copied workspace membership but did not recalculate inherited role grants.",
        "resolution": "Recalculate inherited permissions for the affected team and confirm role mapping.",
        "workaround": "Manually assign the affected user to the required role until recalculation completes.",
        "escalation": "Escalate to Identity Platform if permission recalculation fails."
    },
    {
        "cluster_id": "NOTIF-EMAIL-009",
        "module": "Notifications",
        "title": "Email notifications missing due to suppression list",
        "known_issue_id": "KI-009",
        "affected_versions": "7.0.0-7.0.2",
        "fixed_version": "7.0.3",
        "symptoms": [
            "Customer does not receive email notifications",
            "Password reset email not delivered",
            "Ticket assignment email missing",
            "Email provider shows suppressed recipient"
        ],
        "root_cause": "Recipients were added to the suppression list after repeated soft bounces from their mail server.",
        "resolution": "Remove the verified recipient from suppression list and send a test notification.",
        "workaround": "Ask customer IT to allowlist CloudDesk notification domains.",
        "escalation": "Escalate to Messaging Operations if suppression removal does not restore delivery."
    },
    {
        "cluster_id": "API-RATE-010",
        "module": "Performance",
        "title": "API requests fail due to rate limit confusion",
        "known_issue_id": "KI-010",
        "affected_versions": "8.0.0-8.0.1",
        "fixed_version": "8.0.2",
        "symptoms": [
            "API returns 429 errors",
            "Customer says API is down",
            "Bulk import fails midway",
            "Retry logic causes additional throttling"
        ],
        "root_cause": "Customers exceeded the per-minute workspace API limit, and retry logic did not respect Retry-After headers.",
        "resolution": "Update integration retry logic to honor Retry-After headers and reduce batch size.",
        "workaround": "Temporarily lower request concurrency and schedule bulk imports during off-peak hours.",
        "escalation": "Escalate to API Platform only if 429 errors occur below documented rate limits."
    },
]


CUSTOMER_NAMES = [
    "BluePeak Finance",
    "Northstar Logistics",
    "Evergreen Retail",
    "BrightPath Health",
    "Atlas Learning",
    "Summit Foods",
    "Riverstone Analytics",
    "NovaCloud Services",
    "Pioneer Legal",
    "UrbanCart"
]

TIERS = ["startup", "growth", "enterprise"]
REGIONS = ["US", "EU", "APAC"]
SEVERITIES = ["low", "medium", "high"]


def ensure_dirs():
    folders = [
        BASE_DIR / "docs" / "known_issues",
        BASE_DIR / "docs" / "troubleshooting",
        BASE_DIR / "docs" / "tickets",
        BASE_DIR / "docs" / "incidents",
        BASE_DIR / "docs" / "templates",
        BASE_DIR / "docs" / "policies",
        BASE_DIR / "docs" / "product",
        BASE_DIR / "eval",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def yaml_list(items):
    return "[" + ", ".join(f'"{item}"' for item in items) + "]"


def random_date(days_back=180):
    base = datetime(2025, 5, 1)
    dt = base - timedelta(days=random.randint(1, days_back))
    return dt.strftime("%Y-%m-%d")


def slugify(text):
    return (
        text.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(",", "")
        .replace(".", "")
    )


def generate_known_issue(cluster):
    content = f"""
---
doc_id: {cluster["known_issue_id"]}
doc_type: known_issue
product: {PRODUCT_NAME}
module: {cluster["module"]}
title: "{cluster["title"]}"
status: fixed
affected_versions: "{cluster["affected_versions"]}"
fixed_version: "{cluster["fixed_version"]}"
last_updated: {random_date(90)}
tags: {yaml_list([cluster["module"].lower(), "known-issue", cluster["cluster_id"].lower()])}
related_ids: []
---

# Known Issue {cluster["known_issue_id"]}: {cluster["title"]}

## Summary
{cluster["title"]} affects CloudDesk CRM customers running versions {cluster["affected_versions"]}.

## Affected Versions
- {cluster["affected_versions"]}

## Fixed Version
- {cluster["fixed_version"]}

## Common Symptoms
{chr(10).join(f"- {s}" for s in cluster["symptoms"])}

## Root Cause
{cluster["root_cause"]}

## Workaround
{cluster["workaround"]}

## Permanent Resolution
{cluster["resolution"]}

## Escalation Guidance
{cluster["escalation"]}

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
"""
    filename = f'{cluster["known_issue_id"]}_{slugify(cluster["title"])}.md'
    write_file(BASE_DIR / "docs" / "known_issues" / filename, content)


def generate_troubleshooting_guide(cluster):
    checks = [
        f"Confirm the customer is using an affected version: {cluster['affected_versions']}.",
        "Collect the customer workspace ID, region, and time of first occurrence.",
        "Check whether the issue affects one user, one workspace, or multiple customers.",
        "Search historical tickets for the same symptoms and module.",
        "Apply the documented workaround only if it does not create data loss or security risk.",
        f"Confirm whether the customer can upgrade to fixed version {cluster['fixed_version']}."
    ]

    content = f"""
---
doc_id: TG-{cluster["cluster_id"]}
doc_type: troubleshooting_guide
product: {PRODUCT_NAME}
module: {cluster["module"]}
title: "Troubleshooting: {cluster["title"]}"
version: 1.0
last_updated: {random_date(60)}
severity_default: medium
tags: {yaml_list([cluster["module"].lower(), "troubleshooting", cluster["cluster_id"].lower()])}
related_ids: ["{cluster["known_issue_id"]}"]
---

# Troubleshooting: {cluster["title"]}

## When to Use This Guide
Use this guide when a customer reports symptoms related to {cluster["title"].lower()}.

## Symptoms
{chr(10).join(f"- {s}" for s in cluster["symptoms"])}

## Initial Checks
{chr(10).join(f"{i + 1}. {check}" for i, check in enumerate(checks))}

## Recommended Resolution
{cluster["resolution"]}

## Workaround
{cluster["workaround"]}

## When to Escalate
{cluster["escalation"]}

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
"""
    filename = f'TG_{cluster["cluster_id"]}_{slugify(cluster["title"])}.md'
    write_file(BASE_DIR / "docs" / "troubleshooting" / filename, content)


def generate_ticket(cluster, index):
    ticket_id = f"CD-{cluster['cluster_id'].split('-')[-1]}{index:03d}"
    customer = random.choice(CUSTOMER_NAMES)
    tier = random.choice(TIERS)
    region = random.choice(REGIONS)
    severity = random.choice(SEVERITIES)

    symptom = random.choice(cluster["symptoms"])
    created_at = random_date(150)
    resolved_at = created_at

    customer_phrases = [
        f"We are seeing this issue: {symptom}.",
        f"Our team says {symptom.lower()} and it is blocking daily work.",
        f"Can you check why {symptom.lower()} for our workspace?",
        f"This started today and appears related to {cluster['title'].lower()}."
    ]

    investigation_steps = [
        f"Support confirmed the issue belongs to the {cluster['module']} module.",
        f"The reported behavior matched known issue {cluster['known_issue_id']}.",
        f"The customer was running an affected version range: {cluster['affected_versions']}.",
        "No evidence of permanent data loss was found.",
        "Support compared the case with previous resolved tickets in the same cluster."
    ]

    content = f"""
---
doc_id: {ticket_id}
doc_type: support_ticket
ticket_id: {ticket_id}
product: {PRODUCT_NAME}
module: {cluster["module"]}
title: "{cluster["title"]} - customer case {index}"
customer: "{customer}"
customer_tier: {tier}
region: {region}
status: resolved
severity: {severity}
created_at: {created_at}
resolved_at: {resolved_at}
tags: {yaml_list([cluster["module"].lower(), "resolved", cluster["known_issue_id"].lower()])}
related_ids: ["{cluster["known_issue_id"]}", "TG-{cluster["cluster_id"]}"]
---

# Ticket {ticket_id}: {cluster["title"]}

## Customer
{customer}

## Customer Message
{random.choice(customer_phrases)}

Additional customer context:
- Customer tier: {tier}
- Region: {region}
- Reported module: {cluster["module"]}

## Symptoms Observed
{chr(10).join(f"- {s}" for s in random.sample(cluster["symptoms"], k=min(3, len(cluster["symptoms"]))))}

## Investigation
{chr(10).join(f"- {step}" for step in investigation_steps)}

## Root Cause
{cluster["root_cause"]}

## Resolution Applied
{cluster["resolution"]}

## Workaround Shared
{cluster["workaround"]}

## Final Customer Response
We reviewed the issue and confirmed it matches a known {cluster["module"].lower()} behavior. 
The recommended resolution has been applied: {cluster["resolution"]}
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version {cluster["fixed_version"]}.
"""
    folder = BASE_DIR / "docs" / "tickets" / slugify(cluster["module"])
    filename = f"{ticket_id}_{slugify(cluster['title'])}.md"
    write_file(folder / filename, content)


def generate_incident(cluster):
    incident_id = f"INC-2025-{cluster['cluster_id'].split('-')[-1]}"
    started_at = "2025-03-08T09:20:00Z"
    resolved_at = "2025-03-08T12:05:00Z"

    content = f"""
---
doc_id: {incident_id}
doc_type: incident_report
incident_id: {incident_id}
product: {PRODUCT_NAME}
module: {cluster["module"]}
title: "Incident: {cluster["title"]}"
severity: sev2
started_at: {started_at}
resolved_at: {resolved_at}
tags: {yaml_list([cluster["module"].lower(), "incident", cluster["known_issue_id"].lower()])}
related_ids: ["{cluster["known_issue_id"]}"]
---

# Incident {incident_id}: {cluster["title"]}

## Summary
Multiple customers reported symptoms related to {cluster["title"].lower()}.

## Impact
- Affected module: {cluster["module"]}
- Affected versions: {cluster["affected_versions"]}
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
{cluster["root_cause"]}

## Mitigation
{cluster["workaround"]}

## Resolution
{cluster["resolution"]}

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version {cluster["fixed_version"]}.

## Related Known Issue
- {cluster["known_issue_id"]}
"""
    filename = f"{incident_id}_{slugify(cluster['title'])}.md"
    write_file(BASE_DIR / "docs" / "incidents" / filename, content)


def generate_response_template(cluster):
    content = f"""
---
doc_id: TEMPLATE-{cluster["cluster_id"]}
doc_type: response_template
product: {PRODUCT_NAME}
module: {cluster["module"]}
title: "Customer response template: {cluster["title"]}"
last_updated: {random_date(45)}
tags: {yaml_list([cluster["module"].lower(), "template", cluster["known_issue_id"].lower()])}
related_ids: ["{cluster["known_issue_id"]}"]
---

# Customer Response Template: {cluster["title"]}

Hi {{customer_name}},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known {cluster["module"].lower()} issue.

## What we found
{cluster["root_cause"]}

## What we have done
{cluster["resolution"]}

## Temporary workaround
{cluster["workaround"]}

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
"""
    filename = f"TEMPLATE_{cluster['cluster_id']}_{slugify(cluster['title'])}.md"
    write_file(BASE_DIR / "docs" / "templates" / filename, content)


def generate_product_doc(cluster):
    content = f"""
---
doc_id: PROD-{cluster["cluster_id"]}
doc_type: product_article
product: {PRODUCT_NAME}
module: {cluster["module"]}
title: "{cluster["module"]} module behavior overview"
last_updated: {random_date(120)}
tags: {yaml_list([cluster["module"].lower(), "product-doc"])}
related_ids: []
---

# {cluster["module"]} Module Behavior Overview

The {cluster["module"]} module in CloudDesk CRM supports customer workflows related to {cluster["module"].lower()}.

## Expected Behavior
CloudDesk attempts to provide reliable and auditable behavior for all {cluster["module"].lower()} operations.

## Common Support Areas
Support teams commonly review:
{chr(10).join(f"- {s}" for s in cluster["symptoms"])}

## Operational Notes
Customers on enterprise plans may require faster escalation when the issue blocks production workflows.

## Support Guidance
Before escalating, support should collect:
- Workspace ID
- Customer tier
- Region
- Affected version
- First observed timestamp
- Screenshots or error messages when available
"""
    filename = f"PROD_{cluster['cluster_id']}_{slugify(cluster['module'])}_overview.md"
    write_file(BASE_DIR / "docs" / "product" / filename, content)


def generate_policies():
    escalation_policy = f"""
---
doc_id: POLICY-ESCALATION-001
doc_type: escalation_policy
product: {PRODUCT_NAME}
title: "Support escalation rules"
last_updated: 2025-04-10
tags: ["policy", "escalation", "support"]
related_ids: []
---

# Support Escalation Rules

## Escalate to Engineering
Escalate when:
- A customer-facing error affects more than 10 workspaces.
- A valid API request fails repeatedly with 5xx errors.
- A documented workaround does not resolve the issue.
- Data loss, duplication, or corruption is suspected.

## Escalate to Billing Operations
Escalate when:
- Refunds exceed $5,000.
- Duplicate invoices cannot be voided by support.
- Tax calculation errors affect finalized invoices.

## Escalate to Security
Escalate when:
- Unauthorized access is suspected.
- SSO or MFA failure affects all admin users.
- Audit logs show unexpected login activity.

## Escalate to Messaging Operations
Escalate when:
- Suppression list removal does not restore email delivery.
- Notification delivery is delayed for multiple enterprise customers.

## Escalate to API Platform
Escalate when:
- 429 errors occur below documented rate limits.
- Valid authenticated API requests repeatedly fail with server errors.
"""
    write_file(BASE_DIR / "docs" / "policies" / "POLICY_ESCALATION_001_support_escalation_rules.md", escalation_policy)

    severity_policy = f"""
---
doc_id: POLICY-SEVERITY-001
doc_type: severity_policy
product: {PRODUCT_NAME}
title: "Support severity classification"
last_updated: 2025-04-12
tags: ["policy", "severity", "support"]
related_ids: []
---

# Support Severity Classification

## Severity Low
Use low severity when:
- The issue has a clear workaround.
- Only one non-critical user is affected.
- There is no customer-facing outage.

## Severity Medium
Use medium severity when:
- A team workflow is partially blocked.
- A documented feature behaves inconsistently.
- A workaround exists but is inconvenient.

## Severity High
Use high severity when:
- Production usage is blocked.
- Billing, authentication, or data sync is affected.
- Multiple users or workspaces are impacted.

## Severity Critical
Use critical severity when:
- Data loss is suspected.
- Unauthorized access is suspected.
- A widespread service outage is active.
"""
    write_file(BASE_DIR / "docs" / "policies" / "POLICY_SEVERITY_001_support_severity_classification.md", severity_policy)


def generate_eval_questions():
    questions = []

    for cluster in ISSUE_CLUSTERS:
        questions.append({
            "question": f"A customer reports {cluster['symptoms'][0].lower()}. What should support do?",
            "expected_sources": [
                cluster["known_issue_id"],
                f"TG-{cluster['cluster_id']}"
            ],
            "expected_answer_points": [
                cluster["resolution"],
                cluster["workaround"],
                cluster["escalation"]
            ]
        })

        questions.append({
            "question": f"What versions are affected by {cluster['title'].lower()}?",
            "expected_sources": [
                cluster["known_issue_id"]
            ],
            "expected_answer_points": [
                cluster["affected_versions"],
                cluster["fixed_version"]
            ]
        })

        questions.append({
            "question": f"Should support escalate when {cluster['title'].lower()} continues after workaround?",
            "expected_sources": [
                cluster["known_issue_id"],
                "POLICY-ESCALATION-001"
            ],
            "expected_answer_points": [
                cluster["escalation"]
            ]
        })

        questions.append({
            "question": f"Draft a customer response for {cluster['title'].lower()}.",
            "expected_sources": [
                f"TEMPLATE-{cluster['cluster_id']}",
                cluster["known_issue_id"]
            ],
            "expected_answer_points": [
                cluster["resolution"],
                cluster["workaround"]
            ]
        })

    adversarial = [
        {
            "question": "Can support permanently delete customer billing records to fix duplicate invoices?",
            "expected_behavior": "refuse_or_correct",
            "expected_sources": ["POLICY-ESCALATION-001", "KI-002"],
            "expected_answer_points": [
                "Do not delete billing records",
                "Void the duplicate invoice",
                "Escalate to Billing Operations if duplicate cannot be voided"
            ]
        },
        {
            "question": "Can the assistant guarantee that no customer data was affected in every incident?",
            "expected_behavior": "refuse_or_correct",
            "expected_sources": [],
            "expected_answer_points": [
                "Do not guarantee without evidence",
                "Use only cited incident reports"
            ]
        },
        {
            "question": "If a customer asks for a refund above $5,000, should frontline support approve it immediately?",
            "expected_behavior": "refuse_or_correct",
            "expected_sources": ["POLICY-ESCALATION-001"],
            "expected_answer_points": [
                "Escalate to Billing Operations",
                "Refunds above $5,000 require escalation"
            ]
        }
    ]

    questions.extend(adversarial)

    eval_path = BASE_DIR / "eval" / "questions.jsonl"
    with eval_path.open("w", encoding="utf-8") as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")


def generate_readme():
    content = f"""
# {PRODUCT_NAME} Synthetic Support RAG Dataset

This dataset is a fictional customer support knowledge base for a SaaS product called **{PRODUCT_NAME}**.

It is designed for building and evaluating a RAG-based AI Customer Support Resolution Assistant.

## Dataset Contents

- Product knowledge articles
- Troubleshooting guides
- Historical support tickets
- Known issues
- Incident reports
- Response templates
- Support escalation policies
- Evaluation questions

## Important

This dataset is fully synthetic. It does not contain real customer data, real company data, or confidential information.

## Suggested RAG Use Cases

- Answer support questions with citations
- Retrieve similar historical tickets
- Recommend known resolutions
- Suggest escalation paths
- Draft customer responses
- Evaluate hallucination handling

## Recommended Ingestion Flow

1. Read Markdown files from `docs/`
2. Parse YAML front matter as metadata
3. Chunk Markdown content
4. Generate embeddings
5. Store chunks and metadata in a vector database
6. Use `eval/questions.jsonl` to test retrieval and answer quality
"""
    write_file(BASE_DIR / "README.md", content)


def main():
    ensure_dirs()

    for cluster in ISSUE_CLUSTERS:
        generate_known_issue(cluster)
        generate_troubleshooting_guide(cluster)
        generate_incident(cluster)
        generate_response_template(cluster)
        generate_product_doc(cluster)

        for i in range(1, 6):
            generate_ticket(cluster, i)

    generate_policies()
    generate_eval_questions()
    generate_readme()

    print(f"Dataset generated at: {BASE_DIR.resolve()}")
    print("Approximate documents generated:")
    print("- Known issues:", len(ISSUE_CLUSTERS))
    print("- Troubleshooting guides:", len(ISSUE_CLUSTERS))
    print("- Incidents:", len(ISSUE_CLUSTERS))
    print("- Response templates:", len(ISSUE_CLUSTERS))
    print("- Product docs:", len(ISSUE_CLUSTERS))
    print("- Support tickets:", len(ISSUE_CLUSTERS) * 5)
    print("- Policies: 2")
    print("- Eval questions:", len(ISSUE_CLUSTERS) * 4 + 3)


if __name__ == "__main__":
    main()