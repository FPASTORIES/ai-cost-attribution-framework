Studying AI Cost Allocation & Financial Operations (FinOps)
A learning project: exploring how to reconcile AI usage, classify costs, and connect token spend to business outcomes.

This repository is where I'm documenting what I learn about AI costs, vendor invoices, and how these costs should be classified in a company's P&L.

Coming from a corporate finance and accounting background, I'm using sample data and Python scripts to explore how finance teams can make sense of AI spending. The focus is on token-based API bills, cloud infrastructure costs, and deciding whether a cost belongs in COGS, R&D, S&M, or G&A.

📌 Companion Substack article


I'm an FP&A Professional Studying AI Economics—Here's What I Learned About Reconciling LLM Bills
Why I Started Looking Into This
In traditional software environments, month-end close is relatively straightforward. License costs are usually predictable, cloud infrastructure follows known usage patterns, and invoices can often be matched to purchase orders.

AI makes things a little more complicated.
- The same prompt can cost different amounts. Longer context windows, retries, and multi-step AI agents can all increase token usage and the final bill.
- Invoices don't tell the whole story. Tools such as Cursor, Claude Code, and GitHub Copilot don't always provide the level of detail finance needs to understand exactly where the cost came from.
- One vendor account can serve several purposes. The same OpenAI, Anthropic, or AWS account might support customer-facing products, R&D experiments, and internal employee tools.
I wanted to understand how finance teams could deal with these challenges instead of simply recording the invoice and moving on.

So I built a small experiment using sample general ledger data and Python to test different ways of classifying AI-related costs.
The Three Things I Wanted to Understand
The workflow at a glance: Reconcile the bill → Classify the cost → Measure unit economics.

I approached the problem in three stages, starting with the month-end close and working toward more strategic financial analysis.

1. Month-end close: Can I reconcile the bill?

The first step is understanding the difference between internal usage logs, provider cost reports, and the final invoice. I wanted to explore how to account for differences caused by unmetered scripts, console testing, prepaid credits, and reserved usage tiers.

2. P&L classification: Where should the cost go?

Not every AI expense belongs in COGS. Customer-facing inference, vector databases, and production observability may belong in COGS, while model training and staging environments may belong in R&D. Internal AI tools used by sales or corporate teams may instead fall under S&M or G&A.

The challenge is figuring out how to make those decisions consistently, based on how the resource is actually being used.

3. Unit economics: What are we getting for the money?

A cost per million tokens is useful, but it doesn't tell the entire business story. I also wanted to explore how technical usage data could be translated into measures such as cost per resolved support ticket, cost per active user cohort, or cost per AI agent run.

The bigger question is how to connect AI usage to the financial outcomes that business leaders care about.
Repository Structure
The project is organized into a sample ledger and two versions of the classification script:
.
├── README.md
├── data/
│   └── cost_ledger.csv
└── scripts/
    ├── classify_ai_costs_v1_failed.py
    └── classify_ai_costs_v2_composite.py
The sample ledger contains 15 rows. The two scripts show my first attempt at classification and the revised approach I tested afterward.
What Went Wrong With My First Script
My first version, classify_ai_costs_v1_failed.py, used simple keyword rules to classify costs from the general ledger.

It worked for some obvious descriptions, but real-world-style data quickly exposed its limitations.
1. The description wasn't always helpful
An AP memo such as INV-0093821 usage Aug-Oct doesn't tell you much about the underlying expense. Similarly, an AWS instance name such as p4d.24xlarge doesn't explicitly say whether the resource was used for production or R&D.

Because my rules relied heavily on keywords, some of these entries weren't classified correctly.
2. The department fallback created a bigger problem
When the description didn't provide enough information, the script fell back on the engineering cost center.

That assumption caused more than $145000 of production customer-facing hosting costs to be classified as R&D instead of COGS in my test scenario.

This was the most important lesson from the first attempt: a rule that seems reasonable at first can create a significant reporting error when applied to the wrong data.
Testing a Better Approach: Composite Keys
The change: use more than the transaction description when deciding how to classify a cost.

In classify_ai_costs_v2_composite.py, I tried combining four fields into one text field:

Vendor + Account + CostCenter + Description

I called this CompositeText.

Instead of looking at the transaction description in isolation, give the script more context before making a classification decision.

This helped identify some of the less obvious cloud costs and filter out false positives. I also tested weighted allocations for shared resources, such as splitting a GPU cluster 70% to COGS and 30% to R&D.

This is still an experiment using sample data, not a production-ready accounting system. The results depend on the quality of the underlying data and the classification rules. Shared costs, in particular, need a defensible allocation basis rather than an arbitrary percentage.
How to Run the Experiments
Choose the option that fits your workflow: Excel with Python in Excel, or standalone Python.
Option A: Try It in Excel with Python in Excel
1. Open data/cost_ledger.csv in Microsoft Excel.
2. Format the data as an Excel Table named CostLedger.
3. In a Python cell, use the table as your starting DataFrame:
df = CostLedger.copy()
4. Copy the relevant classification logic from scripts/classify_ai_costs_v2_composite.py into the Python cell and adapt it to work with the table.
Option B: Run the Scripts in Python
Clone the repository and run the scripts from your terminal:
git clone https://github.com/your-username/ai-cost-allocation-framework.git
cd ai-cost-allocation-framework

python scripts/classify_ai_costs_v1_failed.py
python scripts/classify_ai_costs_v2_composite.py

Results From the Sample Dataset
Classification results from the 15-row test ledger

Running the revised script against the 15-row sample ledger produced the following classification results:
Classification	Rows	Amount	Share
COGS	7	$200,971	
R&D	6	$66,790	
S&M	1	$8,400	
G&A	1	$1,100
Not_AI	2	$1,000	Excluded


COGS includes production inference, vector database costs, and the allocated 70% share of the GPU cluster. R&D includes model training jobs, Copilot, and the remaining 30% of that shared cluster.

Not_AI captures two entries, including tax software and offsite entertainment, that the rules exclude from AI cost allocation.

These figures are outputs from the sample dataset, not industry benchmarks. The purpose of the exercise was to test the classification logic and see how a change in approach could affect the resulting P&L.
Sources and Further Reading
Resources I explored while learning about AI cost allocation, cloud spending, and SaaS economics:

These are some of the resources I explored while learning more about AI cost allocation, cloud spending, and SaaS economics:
Spendline —https://www.spendline.ai/guides/reconcile-openai-anthropic-invoices/
Finout — https://www.finout.io/blog/finops-for-ai-agents-a-four-step-allocation-framework
The SaaS CFO — https://www.thesaascfo.com/what-should-be-included-in-ai-cogs/
License
This repository is shared under the MIT License for educational purposes. Feel free to fork it and experiment with your own sample ledger structures and classification rules.
