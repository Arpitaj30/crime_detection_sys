import pandas as pd
import numpy as np
from xgboost import XGBClassifier
import joblib

df = pd.read_csv('vadodara_crime_dataset_expanded (2).csv')
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
df["Lat"] = pd.to_numeric(df["Lat"], errors="coerce")
df["Lon"] = pd.to_numeric(df["Lon"], errors="coerce")

# Aggregate area stats for last 180 days
recent = df[df["Date"] > (pd.Timestamp.today() - pd.Timedelta(days=180))]
area_agg = recent.groupby("Area").agg(
    RecentCount=('Incident_ID', 'count'),
    RecentHigh=('Severity', lambda x: (x == "High").sum()),
    RecentMedium=('Severity', lambda x: (x == "Medium").sum()),
    AvgRiskLabel=('Risk_Label', lambda x: x.map({"Low": 0, "Medium": 1, "High": 2}).mean()),
    Lat=('Lat', 'mean'),
    Lon=('Lon', 'mean')
).reset_index()

def zone_class(row):
    if row.RecentHigh >= 2 or row.AvgRiskLabel > 1.2:
        return 2
    elif row.RecentHigh == 1 or row.AvgRiskLabel > 0.7:
        return 1
    return 0
area_agg["ZoneRisk"] = area_agg.apply(zone_class, axis=1)

X = area_agg[["RecentCount","RecentHigh","RecentMedium","AvgRiskLabel"]]
y = area_agg["ZoneRisk"].values

n_classes = len(np.unique(y))
if n_classes == 2:
    # Binary classification: relabel y for safety (should always be [0,1])
    y = y - y.min()
    model = XGBClassifier(
        n_estimators=100, max_depth=3, use_label_encoder=False,
        eval_metric="mlogloss", random_state=42)
elif n_classes > 2:
    # Multiclass classification
    model = XGBClassifier(
        n_estimators=100, max_depth=3, use_label_encoder=False,
        eval_metric="mlogloss", random_state=42, objective="multi:softmax", num_class=n_classes)
else:
    raise ValueError("Not enough class labels for training.")

model.fit(X, y)
joblib.dump((model, area_agg), "zone_risk_xgb.pkl")
print(f"Zone risk model trained with {n_classes} classes and saved to zone_risk_xgb.pkl")

def broken_function(
