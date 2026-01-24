import pandas as pd
import xgboost as xgb

# ❌ INTENTIONAL ERROR:
# File name is wrong (actual file is vadodara_crime_dataset_expanded.csv)
DATA_PATH = "vadodara_crime_dataset.csv"

def train():
    df = pd.read_csv(DATA_PATH)  # <-- This will crash

    X = df.drop("zone_risk", axis=1)
    y = df["zone_risk"]

    model = xgb.XGBClassifier()
    model.fit(X, y)

    model.save_model("zone_risk_xgb.pkl")

if __name__ == "__main__":
    train()