# scoring_engine.py
# Quantitative control effectiveness scoring engine
# Evaluates controls across multiple risk dimensions
# and assigns risk ratings aligned to CCO framework logic

import pandas as pd
import numpy as np

# Scoring weights across dimensions
WEIGHTS = {
    'assessment_score': 0.35,
    'frequency_penalty': 0.25,
    'regulatory_impact': 0.20,
    'operational_impact': 0.15,
    'staleness_penalty': 0.05
}

def calculate_effectiveness_score(row):
    """
    Composite control effectiveness score (0-100).
    Higher score = more effective control.
    Lower score = weaker control, higher risk.
    """

    # Base assessment score (0-100 from audit assessment)
    base = row['assessment_score'] * WEIGHTS['assessment_score']

    # Frequency penalty — more failures = lower score
    freq_penalty = max(0, 25 - (row['frequency_of_failure'] * 5))
    freq_component = freq_penalty * WEIGHTS['frequency_penalty']

    # Regulatory impact component
    reg_score = (4 - row['regulatory_impact_score']) * 8
    reg_component = reg_score * WEIGHTS['regulatory_impact']

    # Operational impact component
    ops_score = (4 - row['operational_impact_score']) * 8
    ops_component = ops_score * WEIGHTS['operational_impact']

    # Staleness penalty
    staleness = max(0, 20 - (row['days_since_assessment'] / 5))
    staleness_component = staleness * WEIGHTS['staleness_penalty']

    # Automation bonus
    automation_bonus = row.get('automation_bonus', 0)

    total = (base + freq_component + reg_component +
             ops_component + staleness_component + automation_bonus)

    return round(min(total, 100), 2)

def assign_risk_rating(score):
    """
    Map effectiveness score to risk rating.
    Lower effectiveness = higher risk.
    """
    if score >= 80:
        return 'Low Risk'
    elif score >= 60:
        return 'Medium Risk'
    elif score >= 40:
        return 'High Risk'
    else:
        return 'Critical Risk'

def assign_rag_status(score):
    """RAG status for Power BI dashboard reporting."""
    if score >= 80:
        return 'Green'
    elif score >= 60:
        return 'Amber'
    else:
        return 'Red'

def score_controls(df):
    df = df.copy()
    df['effectiveness_score'] = df.apply(
        calculate_effectiveness_score, axis=1
    )
    df['risk_rating'] = df['effectiveness_score'].apply(assign_risk_rating)
    df['rag_status'] = df['effectiveness_score'].apply(assign_rag_status)
    return df.sort_values('effectiveness_score', ascending=True)

def generate_mi_summary(df):
    """
    Generate MI report summary for senior stakeholder review.
    Mirrors CCO reporting output.
    """
    print("\n" + "="*55)
    print("CONTROL EFFECTIVENESS MI REPORT")
    print("="*55)
    print(f"Total controls assessed : {len(df)}")
    print(f"Average effectiveness   : {df['effectiveness_score'].mean():.1f}/100")
    print(f"\nRAG Summary:")
    rag_counts = df['rag_status'].value_counts()
    for status, count in rag_counts.items():
        print(f"  {status:6} : {count} controls")
    print(f"\nTop 5 Weakest Controls (Escalation Priority):")
    weak = df.nsmallest(5, 'effectiveness_score')[
        ['control_id', 'business_unit', 'control_name',
         'effectiveness_score', 'risk_rating', 'rag_status']
    ]
    print(weak.to_string(index=False))
    print("="*55)

if __name__ == "__main__":
    from preprocess import load_data, preprocess
    df = load_data("../data/control_assessments.csv")
    df = preprocess(df)
    df = score_controls(df)
    generate_mi_summary(df)
    df.to_csv("../reports/control_effectiveness_scores.csv", index=False)
    print("\nResults saved to reports/control_effectiveness_scores.csv")
