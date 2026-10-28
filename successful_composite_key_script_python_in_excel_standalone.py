#!/usr/bin/env python3
"""
Version 2: Production Composite-Key Classifier (The Successful Attempt)

This version resolves the opacity issues identified in V1 by:
1. Concatenating Vendor + Account + CostCenter + Description into a single CompositeText key.
2. Applying explicit false-positive guardrails (e.g., Vertex Inc tax software).
3. Utilizing dictionary rules for specific instance types (e.g., p4d.24xlarge).
4. Supporting 70/30 weighted splits for shared GPU/Cloud infrastructure.
5. Functioning natively within Excel using Python in Excel (`PY()`).
"""

import pandas as pd
import re

def run_v2_composite_classification(df):
    df_copy = df.copy()

    # 1. Construct Composite Text Key
    df_copy["CompositeText"] = (
        df_copy["Vendor"].fillna("") + " " +
        df_copy["Account"].fillna("") + " " +
        df_copy["CostCenter"].fillna("") + " " +
        df_copy["Description"].fillna("")
    ).str.lower()

    # 2. Advanced Rule Engine with Guardrails & Weighted Splits
    def classify_row_v2(row):
        text = row["CompositeText"]

        # Guardrail: Filter out non-AI false positives
        if "vertex inc" in text or "fireworks events" in text:
            return "Not_AI", "False Positive Guardrail", {}

        # Rule 1: R&D Model Training & Experiments
        if re.search(r"train|fine-?tun|experiment|research|prototype|eval|benchmark|sandbox|dev\b|staging|rlhf", text):
            return "R&D", "Model Training & Experiments", {}

        # Rule 2: Engineering Dev Tools & Observability
        if re.search(r"copilot|cursor|weights & biases|enterprise hub|observability", text):
            return "R&D", "Engineering Dev Tools & Observability", {}

        # Rule 3: Shared GPU Infrastructure Split (70% COGS / 30% R&D)
        if re.search(r"aws|azure|gcp|coreweave|lambda", text) and re.search(r"gpu|a100|h100|p4d\.24xlarge|p3\.8xlarge", text):
            return "Split", "Shared GPU Hosting Split", {"COGS": 0.7, "R&D": 0.3}

        # Rule 4: Customer-Facing Inference, Vector DBs, & Infrastructure
        if re.search(r"inference|serving|production|prod\b|customer|api usage|embedding|vector|hosting|endpoint|cortex ai|bedrock|vertex ai", text):
            return "COGS", "Customer-Facing Inference & Infrastructure", {}

        # Rule 5: Productized AI SaaS Apps
        if re.search(r"voice agent|revenue intelligence|transcription|pro plan|add-on|scale plan|elevenlabs|midjourney|gong", text):
            return "COGS", "Productized AI SaaS", {}

        # Rule 6: Sales & Marketing AI
        if re.search(r"marketing|sales|growth|copywriting|lead scor|outbound|campaign|seo|jasper|einstein", text):
            return "S&M", "Sales & Marketing AI", {}

        # Rule 7: G&A Internal Productivity
        if re.search(r"finance|legal|hr\b|admin|g&a|chatgpt team|chatgpt enterprise|compliance", text):
            return "G&A", "Internal G&A Productivity", {}

        return "Unclassified", "No Rule Matched", {}

    # 3. Process Rows & Expand Weighted Splits
    buckets, rules, splits = [], [], []
    for _, row in df_copy.iterrows():
        b, r, s = classify_row_v2(row)
        buckets.append(b)
        rules.append(r)
        splits.append(s)

    df_copy["Bucket"] = buckets
    df_copy["Rule"] = rules

    expanded_rows = []
    for idx, row in df_copy.iterrows():
        if splits[idx]:
            for b_name, pct in splits[idx].items():
                new_row = row.copy()
                new_row["Bucket"] = b_name
                new_row["Amount"] = row["Amount"] * pct
                new_row["Rule"] = f"{row['Rule']} ({pct:.0%})"
                expanded_rows.append(new_row)
        else:
            expanded_rows.append(row)

    result_df = pd.DataFrame(expanded_rows)
    return result_df

if __name__ == "__main__":
    try:
        data = pd.read_excel("data/ai_cost_ledger_complex.xlsx", sheet_name="ledger_input")
        classified = run_v2_composite_classification(data)
        print("=== V2 Composite Key Classification Output ===")
        print(classified[["Vendor", "Description", "Amount", "Bucket", "Rule"]])
    except FileNotFoundError:
        print("Please run from repo root with data/ai_cost_ledger_complex.xlsx present.")