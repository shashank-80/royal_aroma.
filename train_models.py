import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

def train_pipelines():
    os.makedirs("models", exist_ok=True)
    
    if not os.path.exists("dataset/perfume_data.csv"):
        raise FileNotFoundError("Run dataset_generator.py first to establish source files.")
        
    df = pd.read_csv("dataset/perfume_data.csv")
    
    # Feature Engineering Target Vectors
    feature_cols = ['Gender', 'Age_Group', 'Occasion', 'Season', 'Longevity', 'Projection']
    target_col = 'Fragrance_Family'
    
    encoders = {}
    X = pd.DataFrame()
    
    for col in feature_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    target_le = LabelEncoder()
    y = target_le.fit_transform(df[target_col])
    encoders[target_col] = target_le
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model 1: Random Forest
    rf_model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Model 2: XGBoost
    xgb_model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_train, y_train)
    
    # Save Pipeline Artifactory
    joblib.dump(rf_model, "models/rf_perfume_model.pkl")
    joblib.dump(xgb_model, "models/xgb_perfume_model.pkl")
    joblib.dump(encoders, "models/label_encoders.pkl")
    
    print("Machine Learning Models trained and cached inside /models/ directory.")

if __name__ == "__main__":
    train_pipelines()
