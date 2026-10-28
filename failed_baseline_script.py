#!/usr/bin/env python3
"""
Version 1: Baseline / Plain Keyword Classifier (The Failed Attempt)

This script demonstrates the limitations of relying purely on plain string regex
against sparse description fields and raw cost center fallbacks.

Key Failure Points Discovered:
1. False Negatives: Missed GPU instances (p4d.24xlarge) due to lack of explicit "AI" keywords.
2. False Positives: Accidental matches on "vertex inc" (tax software) and "fireworks events".
3. Department Fallback Trap: Silent misclassification of ~$450K in customer-facing
   production infrastructure into R&D because cost center was "Engineering".
"""

import pandas as pd
import re

def run_v1_failed_classification(df):
    df_copy = df.copy()
    
    # Standard Plain Keyword Regex
    ai_keyword_regex = r"openai|anthropic|claude|gpt|llm|gemini|bedrock|sagemaker|vertex|copilot|cursor|pinecone|gpu|a100|h100|inference|fine-?tun|\bai\b"
    
    # 1. Filter AI Rows based on Vendor or Description alone
    def is_ai(row):
        text = f"{row.get('Vendor', '')} {row.get('Description', '')}".lower()
        return bool(re.search(ai_keyword_regex, text))

    df_copy["Is_AI"] = df_copy.apply(is_ai, axis=1)
    ai_df = df_copy[df_copy["Is_AI"]].copy()

    # 2. Naive Rule Engine (Description priority, Department fallback)
    def naive_classify(row):
        desc = str(row.get("Description", "")).lower()
        dept = str(row.get("CostCenter", "")).lower()

        # Rule A: R&D Explicit Keywords
        if re.search(r"train|fine-?tun|experiment|eval|benchmark|sandbox", desc):
            return "R&D", "R&D Keyword Match"
        
        # Rule B: COGS Explicit Keywords
        if re.search(r"inference|serving|production|prod\b|customer|vector", desc):
            return "COGS", "COGS Keyword Match"
        
        # Rule C: Department Fallback Trap (Engineering -> R&D)
        if re.search(r"eng|platform|product|data", dept):
            return "R&D", "Department Fallback (Engineering -> R&D)"
        
        # Rule D: G&A Fallback
        if re.search(r"finance|hr|admin|legal", dept):
            return "G&A", "Department Fallback (Admin -> G&A)"

        return "Unclassified", "No Rule"

    results = ai_df.apply(naive_classify, axis=1)
    ai_df["P&L_Bucket"], ai_df["Rule_Fired"] = zip(*results)
    
    return ai_df

if __name__ == "__main__":
    # Load test ledger
    try:
        data = pd.read_excel("data/ai_cost_ledger_complex.xlsx", sheet_name="ledger_input")
        classified = run_v1_failed_classification(data)
        print("=== V1 Failed Classification Output ===")
        print(classified[["Vendor", "Description", "CostCenter", "Amount", "P&L_Bucket", "Rule_Fired"]])
    except FileNotFoundError:
        print("Please run from repo root with data/ai_cost_ledger_complex.xlsx present.")