"""
Task 3: Model Promotion
Train a second model variant, compare with champion, and promote if better.
"""

import json
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient

# Set MLflow tracking URI
mlflow.set_tracking_uri("file:///./mlruns")

# Load the result from Task 1 to determine the best model type
with open("results/step1_s1.json", "r") as f:
    task1_results = json.load(f)
    best_model_type = task1_results["best_model"]

# Load data
data = pd.read_csv("data/training_data.csv")
X = data[["temperature_c", "building_sqm", "occupancy_pct", "is_weekday"]]
y = data["energy_kwh"]

# Split data with same random state as Task 1 for consistency in comparison
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

client = MlflowClient()
registered_model_name = "powergrid-energy-kwh-predictor"

# Get champion version (version 1)
champion_version = client.get_model_version(registered_model_name, version=1)
champion_run_id = champion_version.run_id

# Get champion metrics
champion_run = client.get_run(champion_run_id)
champion_rmse = champion_run.data.metrics.get("rmse", float('inf'))
champion_mae = champion_run.data.metrics.get("mae", 0.0)
champion_r2 = champion_run.data.metrics.get("r2", 0.0)

print(f"Champion (Version 1) RMSE: {champion_rmse:.4f}")

# Train challenger (version 2) with random_state=99
print(f"Training challenger model with random_state=99...")
experiment_name = "powergrid-energy-kwh"
mlflow.set_experiment(experiment_name)

with mlflow.start_run(run_name="Challenger_model_v2"):
    if best_model_type == "SVR":
        challenger = SVR(kernel="rbf", C=100, epsilon=0.1, gamma="scale")
    else:  # GradientBoosting
        challenger = GradientBoostingRegressor(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5, 
            random_state=99
        )
    
    challenger.fit(X_train, y_train)
    
    y_pred_challenger = challenger.predict(X_test)
    challenger_mae = mean_absolute_error(y_test, y_pred_challenger)
    challenger_rmse = np.sqrt(mean_squared_error(y_test, y_pred_challenger))
    challenger_r2 = r2_score(y_test, y_pred_challenger)
    
    # Log parameters
    mlflow.log_param("model_type", best_model_type)
    if best_model_type == "SVR":
        mlflow.log_param("kernel", "rbf")
        mlflow.log_param("C", 100)
        mlflow.log_param("epsilon", 0.1)
        mlflow.log_param("gamma", "scale")
    else:
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("learning_rate", 0.1)
        mlflow.log_param("max_depth", 5)
        mlflow.log_param("random_state", 99)
    
    # Log metrics
    mlflow.log_metric("mae", challenger_mae)
    mlflow.log_metric("rmse", challenger_rmse)
    mlflow.log_metric("r2", challenger_r2)
    
    # Log tags
    mlflow.set_tag("priority", "high")
    
    # Log model
    mlflow.sklearn.log_model(challenger, "model")
    
    challenger_run_id = mlflow.active_run().info.run_id

print(f"Challenger (Version 2) RMSE: {challenger_rmse:.4f}")

# Register challenger as version 2
model_uri = f"runs:/{challenger_run_id}/model"
model_version_2 = mlflow.register_model(model_uri, registered_model_name)

print(f"Challenger registered as version {model_version_2.version}")

# Determine promotion
if challenger_rmse < champion_rmse:
    action = "promoted"
    # Set alias to version 2
    client.set_registered_model_alias(registered_model_name, "production", int(model_version_2.version))
    promoted_version = int(model_version_2.version)
    print(f"Challenger is better! Promoted to production.")
else:
    action = "kept"
    # Keep alias on version 1
    client.set_registered_model_alias(registered_model_name, "production", 1)
    promoted_version = 1
    print(f"Champion is better or equal. Keeping version 1 in production.")

# Prepare results
results = {
    "registered_model_name": registered_model_name,
    "alias_name": "production",
    "champion_version": 1,
    "challenger_version": int(model_version_2.version),
    "champion_rmse": round(champion_rmse, 4),
    "challenger_rmse": round(challenger_rmse, 4),
    "action": action,
    "promoted_version": promoted_version
}

# Save results
with open("results/step3_s7.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results/step3_s7.json")
