# Studying AI Cost Allocation & Financial Operations (FinOps)

Notes, test datasets, and experimental Python scripts documenting my journey in "learning in public" about usage-based AI token bills, vendor invoices, and corporate P&L classification (**COGS**, **R&D**, **S&M**, and **G&A**).

> 📌 **Companion Substack Article:** Read the full analytical write-up and narrative notes on Substack:  
> **[I'm an FP&A Professional Studying AI Economics—Here's What I Learned About Reconciling LLM Bills](https://substack.com)**

---

## 💡 Why I Started Looking Into This

Coming from a corporate finance and accounting background, month-end software close always felt fairly predictable: seat licenses were standard, cloud servers scaled on known schedules, and invoices matched purchase orders.

Generative AI and token-based pricing challenge many of those traditional financial habits:
1. **Token Cost Is Non-Deterministic:** Variations in context window length, retry loops, and agent depth cause two identical prompts to incur vastly different token costs.
2. **No Source-Level Resource Tag:** API calls and coding assistants (Cursor, Claude Code, GitHub Copilot) do not leave durable infrastructure tags on vendor invoices.
3. **Environment Blending:** A single vendor account (e.g., OpenAI, Anthropic, AWS) serves customer-facing production features, R&D fine-tuning, and internal team tools simultaneously.

I created this repository to experiment with rules-based classification methods and explore how finance teams can move from simply transcribing an AI invoice to understanding what actually drove the spend.

---

## 🧭 The 3-Stage Financial Mechanics I Explored
1. **Two-Bridge Reconciliation:** Bridging internal request telemetry logs $\rightarrow$ Provider Cost APIs $\rightarrow$ Final Settlement Invoices to account for unmetered scripts, console tests, prepaid credits, and tier reserves.
2. **P&L Classification (GAAP):** Exploring how to distinguish COGS (customer inference, vector databases, production observability) from OpEx (R&D fine-tuning, staging environments) and SG&A (internal enterprise seats).
3. **Strategic Unit Economics:** Translating technical token metrics (*cost per 1M tokens*) into business outcome metrics (*cost per resolved ticket*, *cost per active user cohort*, *cost per agent run*).

---

## 📂 Repository Structure

```text
.
├── README.md                          # Repository overview & notes
├── data/
│   └── cost_ledger.csv                # 15-row sample test ledger with edge cases
└── scripts/
    ├── classify_ai_costs_v1_failed.py # Baseline script showing the $450K R&D misclassification trap
    └── classify_ai_costs_v2_composite.py # Updated script testing composite text keys & weighted splits

In my research across FinOps literature and technical documentation, I pieced together three interconnected stages of AI cost attribution:
