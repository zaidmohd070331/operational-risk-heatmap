# preprocess.py
# Data loading and preprocessing for control effectiveness scoring

import pandas as pd
import numpy as np

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['last_assessed'] = pd.to_datetime(df['last_assessed'])
    return df

def preprocess(df):
    df = df.copy()

    # Days since last assessment (staleness indicator)
    reference_date = pd.Timestamp('2024-03-01')
    df['days_since_assessment'] = (
        reference_date - df['last_assessed']
    ).dt.days

    # Encode impact levels
    impact_map = {'Low': 1, 'Medium': 2, 'High': 3}
    df['regulatory_impact_score'] = df['regulatory_impact'].map(impact_map)
    df['operational_impact_score'] = df['operational_impact'].map(impact_map)

    # Automation bonus (automated controls are more reliable)
    df['automation_bonus'] = df['is_automated'].apply(
        lambda x: 5 if x == 1 else 0
    )

    return df

if __name__ == "__main__":
    df = load_data("../data/control_assessments.csv")
    df = preprocess(df)
    print("Preprocessing complete.")
    print(df[['control_id', 'days_since_assessment',
              'regulatory_impact_score',
              'operational_impact_score']].to_string())
