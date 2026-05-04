"""
Task 1: Experiment Tracking & Model Comparison
Train SVR and GradientBoosting models on training data with MLflow tracking.
"""

import json
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
import os

# Set MLflow tracking URI
mlflow.set_tracking_uri("file:///./mlruns")

# Create experiment
experiment_name = "powergrid-energy-kwh"
try:
    experiment_id = mlflow.create_experiment(experiment_name)
except:
    experiment = mlflow.get_experiment_by_name(experiment_name)
    experiment_id = experiment.experiment_id

mlflow.set_experiment(experiment_name)

# Load data
data = pd.read_csv("data/training_data.csv")
X = data[["temperature_c", "building_sqm", "occupancy_pct", "is_weekday"]]
y = data["energy_kwh"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Store results
results = {
    "experiment_name": experiment_name,
    "models": [],
    "best_model": "",
    "best_metric_name": "rmse",
    "best_metric_value": float('inf')
}

# Model 1: SVR
print("Training SVR model...")
with mlflow.start_run(run_name="SVR_model"):
    svr = SVR(kernel="rbf", C=100, epsilon=0.1, gamma="scale")
    svr.fit(X_train, y_train)
    
    y_pred_svr = svr.predict(X_test)
    mae_svr = mean_absolute_error(y_test, y_pred_svr)
    rmse_svr = np.sqrt(mean_squared_error(y_test, y_pred_svr))
    r2_svr = r2_score(y_test, y_pred_svr)
    
    # Log parameters
    mlflow.log_param("model_type", "SVR")
    mlflow.log_param("kernel", "rbf")
    mlflow.log_param("C", 100)
    mlflow.log_param("epsilon", 0.1)
    mlflow.log_param("gamma", "scale")
    
    # Log metrics
    mlflow.log_metric("mae", mae_svr)
    mlflow.log_metric("rmse", rmse_svr)
    mlflow.log_metric("r2", r2_svr)
    
    # Log tags
    mlflow.set_tag("priority", "high")
    
    # Log model
    mlflow.sklearn.log_model(svr, "model")
    
    svr_run_id = mlflow.active_run().info.run_id
    
    results["models"].append({
        "name": "SVR",
        "mae": round(mae_svr, 4),
        "rmse": round(rmse_svr, 4),
        "r2": round(r2_svr, 4),
        "run_id": svr_run_id
    })
    
    if rmse_svr < results["best_metric_value"]:
        results["best_model"] = "SVR"
        results["best_metric_value"] = round(rmse_svr, 4)
        best_model = svr
        best_run_id = svr_run_id
    
    print(f"SVR - MAE: {mae_svr:.4f}, RMSE: {rmse_svr:.4f}, R²: {r2_svr:.4f}")

# Model 2: GradientBoosting
print("Training GradientBoosting model...")
with mlflow.start_run(run_name="GradientBoosting_model"):
    gb = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    gb.fit(X_train, y_train)
    
    y_pred_gb = gb.predict(X_test)
    mae_gb = mean_absolute_error(y_test, y_pred_gb)
    rmse_gb = np.sqrt(mean_squared_error(y_test, y_pred_gb))
    r2_gb = r2_score(y_test, y_pred_gb)
    
    # Log parameters
    mlflow.log_param("model_type", "GradientBoosting")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("learning_rate", 0.1)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("random_state", 42)
    
    # Log metrics
    mlflow.log_metric("mae", mae_gb)
    mlflow.log_metric("rmse", rmse_gb)
    mlflow.log_metric("r2", r2_gb)
    
    # Log tags
    mlflow.set_tag("priority", "high")
    
    # Log model
    mlflow.sklearn.log_model(gb, "model")
    
    gb_run_id = mlflow.active_run().info.run_id
    
    results["models"].append({
        "name": "GradientBoosting",
        "mae": round(mae_gb, 4),
        "rmse": round(rmse_gb, 4),
        "r2": round(r2_gb, 4),
        "run_id": gb_run_id
    })
    
    if rmse_gb < results["best_metric_value"]:
        results["best_model"] = "GradientBoosting"
        results["best_metric_value"] = round(rmse_gb, 4)
        best_model = gb
        best_run_id = gb_run_id
    
    print(f"GradientBoosting - MAE: {mae_gb:.4f}, RMSE: {rmse_gb:.4f}, R²: {r2_gb:.4f}")

# Save best model
os.makedirs("models", exist_ok=True)
import pickle
with open(f"models/best_model_task1.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open(f"models/best_run_id.txt", "w") as f:
    f.write(best_run_id)

# Save results
os.makedirs("results", exist_ok=True)
with open("results/step1_s1.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nBest model: {results['best_model']} with RMSE: {results['best_metric_value']}")
print("Results saved to results/step1_s1.json")
