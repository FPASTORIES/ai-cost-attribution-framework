# Studying AI Cost Allocation & Financial Operations (FinOps)

Notes, test datasets, and experimental Python scripts documenting my journey in "learning in public" about usage-based AI token bills, vendor invoices, and corporate P&L classification (COGS, R&D, S&M, and G&A).

> 📌 Companion Substack Article: Read the full analytical write-up and narrative notes on Substack:
> [I'm an FP&A Professional Studying AI Economics—Here's What I Learned About Reconciling LLM Bills](https://substack.com)

## Why I Started Looking Into This

Coming from a corporate finance and accounting background, month-end software close always felt fairly predictable: seat licenses were standard, cloud servers scaled on known schedules, and invoices matched purchase orders.

Generative AI and token-based pricing challenge many of those traditional financial habits:
1. Token Cost Is Non-Deterministic: Variations in context window length, retry loops, and agent depth cause two identical prompts to incur vastly different token costs.
2. No Source-Level Resource Tag: API calls and coding assistants (Cursor, Claude Code, GitHub Copilot) do not leave durable infrastructure tags on vendor invoices.
3. Environment Blending: A single vendor account (e.g., OpenAI, Anthropic, AWS) serves customer-facing production features, R&D fine-tuning, and internal team tools simultaneously.

I created this repository to experiment with rules-based classification methods and explore how finance teams can move from simply transcribing an AI invoice to understanding what actually drove the spend.

## The 3-Stage Financial Mechanics I Explored

In my research across FinOps literature and technical documentation, I pieced together three interconnected stages of AI cost attribution:

  [1. Month-End Close]  -->  [2. Gross Margin (P&L)]  -->  [3. Unit Economics]
  Reconcile & Attribute        Classify COGS vs R&D          Track Cost per Outcome
    (Two-Bridge Close)           (GAAP Accounting)             (Strategic FP&A)

1. Two-Bridge Reconciliation: Bridging internal request telemetry logs -> Provider Cost APIs -> Final Settlement Invoices to account for unmetered scripts, console tests, prepaid credits, and tier reserves.
2. P&L Classification (GAAP): Exploring how to distinguish COGS (customer inference, vector databases, production observability) from OpEx (R&D fine-tuning, staging environments) and SG&A (internal enterprise seats).
3. Strategic Unit Economics: Translating technical token metrics (cost per 1M tokens) into business outcome metrics (cost per resolved ticket, cost per active user cohort, cost per agent run).

## Repository Structure

.
├── README.md                          # Overview & notes
├── data/
│   └── cost_ledger.csv                # 15-row sample test ledger
└── scripts/
    ├── classify_ai_costs_v1_failed.py # Baseline script ($450K R&D trap)
    └── classify_ai_costs_v2_composite.py # Composite key script

## Lessons Learned: My Initial Script Failure

To understand the opacity of AI spend firsthand, I wrote a basic Python script (classify_ai_costs_v1_failed.py) using keyword rules to parse a sample general ledger.

It was a humbling experiment that highlighted why automated classification is tricky:
- The Cryptic Memo Problem: Real AP memos like INV-0093821 usage Aug-Oct or AWS strings like p4d.24xlarge lacked explicit "AI" or "production" keywords, causing them to fall through simple regex rules.
- The Department Fallback Trap: Defaulting to engineering cost centers when descriptions were sparse caused over $450,000 of production customer-facing hosting to be misclassified into R&D instead of COGS.

### Testing the Composite Key Approach

In the updated experiment (classify_ai_costs_v2_composite.py), I tested concatenating Vendor + Account + CostCenter + Description into a single CompositeText string. This provided enough context to identify cryptic cloud line items, filter out false positives, and apply weighted splits (e.g., 70% COGS / 30% R&D for shared GPU clusters).

## Running the Experiments (Python or Excel)

Option A: Testing in Excel with Python in Excel (PY())
1. Open data/cost_ledger.csv in Microsoft Excel.
2. Format the dataset as an Excel Table named CostLedger.
3. In a new cell, type =PY and paste the code from scripts/classify_ai_costs_v2_composite.py.
4. Reference the table using df = CostLedger.copy().

Option B: Running Standalone Python
Clone the repository and run either script directly from your terminal:

git clone https://github.com/your-username/ai-cost-allocation-framework.git
cd ai-cost-allocation-framework
python scripts/classify_ai_costs_v1_failed.py
python scripts/classify_ai_costs_v2_composite.py

## Sample Output From Test Dataset

Running classify_ai_costs_v2_composite.py against the 15-row sample ledger yields:

- COGS (7 rows, $205,370.00 / 72.8%): Production inference, vector DB, 70% GPU cluster split
- R&D (6 rows, $68,680.00 / 24.3%): Model training jobs, Copilot, 30% GPU cluster split
- S&M (1 row, $7,500.00 / 2.7%): Revenue intelligence & sales scoring AI
- G&A (1 row, $1,100.00 / 0.4%): Internal ChatGPT Team seats
- Not_AI (2 rows, $1,000.00): Excluded tax software & offsite entertainment guardrails

## Sources & Further Reading

- Finout: "FinOps for AI Agents: A Four-Step Allocation Framework"
- Ben Murray (The SaaS CFO): "What Should Be Included in AI COGS"
- Spendline: "How to Reconcile OpenAI and Anthropic Invoices"
- CloudZero: "State of AI Costs Report"
- ICONIQ Growth: "State of AI Report & Gross Margin Benchmarks"

## License

This repository is shared under the MIT License for educational purposes. Feel free to fork and test with your own sample ledger structures.
