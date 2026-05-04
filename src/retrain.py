"""
Task 4: Retraining Pipeline
Retrain model on combined data and decide whether to promote.
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

# Load original task 1 results to determine best model type
with open("results/step1_s1.json", "r") as f:
    task1_results = json.load(f)
    best_model_type = task1_results["best_model"]

# Load original training data
original_data = pd.read_csv("data/training_data.csv")
original_rows = len(original_data)

# Load new data
new_data = pd.read_csv("data/new_data.csv")
new_rows = len(new_data)

# Combine datasets
combined_data = pd.concat([original_data, new_data], ignore_index=True)
combined_rows = len(combined_data)

print(f"Original data rows: {original_rows}")
print(f"New data rows: {new_rows}")
print(f"Combined data rows: {combined_rows}")

# Prepare features and target
X_combined = combined_data[["temperature_c", "building_sqm", "occupancy_pct", "is_weekday"]]
y_combined = combined_data["energy_kwh"]

# Split combined data - use original random state and test size to have comparable test set with original
# For fair comparison, we should use the same test set as Task 1
# Get original training data to extract the same test set
original_X = original_data[["temperature_c", "building_sqm", "occupancy_pct", "is_weekday"]]
original_y = original_data["energy_kwh"]
X_train_orig, X_test, y_train_orig, y_test = train_test_split(
    original_X, original_y, test_size=0.2, random_state=42
)

# Now train on combined data but evaluate on same test set
X_train_combined, _, y_train_combined, _ = train_test_split(
    X_combined, y_combined, test_size=0.2, random_state=42
)

# Get champion version metrics from Task 3
with open("results/step3_s7.json", "r") as f:
    task3_results = json.load(f)
    champion_rmse = task3_results["champion_rmse"]
    promoted_version = task3_results["promoted_version"]

client = MlflowClient()
registered_model_name = "powergrid-energy-kwh-predictor"

print(f"\nChampion version: {promoted_version} with RMSE: {champion_rmse}")

# Train new model on combined data
print(f"Retraining {best_model_type} on combined data...")
experiment_name = "powergrid-energy-kwh"
mlflow.set_experiment(experiment_name)

with mlflow.start_run(run_name="Retrained_model"):
    if best_model_type == "SVR":
        retrained = SVR(kernel="rbf", C=100, epsilon=0.1, gamma="scale")
    else:  # GradientBoosting
        retrained = GradientBoostingRegressor(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5, 
            random_state=42
        )
    
    retrained.fit(X_train_combined, y_train_combined)
    
    # Evaluate on the SAME test set as original for fair comparison
    y_pred_retrained = retrained.predict(X_test)
    retrained_mae = mean_absolute_error(y_test, y_pred_retrained)
    retrained_rmse = np.sqrt(mean_squared_error(y_test, y_pred_retrained))
    retrained_r2 = r2_score(y_test, y_pred_retrained)
    
    # Log parameters
    mlflow.log_param("model_type", best_model_type)
    mlflow.log_param("trained_on", "combined_data")
    if best_model_type == "SVR":
        mlflow.log_param("kernel", "rbf")
        mlflow.log_param("C", 100)
        mlflow.log_param("epsilon", 0.1)
        mlflow.log_param("gamma", "scale")
    else:
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("learning_rate", 0.1)
        mlflow.log_param("max_depth", 5)
        mlflow.log_param("random_state", 42)
    
    # Log metrics
    mlflow.log_metric("mae", retrained_mae)
    mlflow.log_metric("rmse", retrained_rmse)
    mlflow.log_metric("r2", retrained_r2)
    
    # Log tags
    mlflow.set_tag("priority", "high")
    
    # Log model
    mlflow.sklearn.log_model(retrained, "model")
    
    retrained_run_id = mlflow.active_run().info.run_id

print(f"Retrained model RMSE: {retrained_rmse:.4f}")

# Calculate improvement
improvement = champion_rmse - retrained_rmse
min_improvement_threshold = 0.5

print(f"Improvement: {improvement:.4f}")
print(f"Min improvement threshold: {min_improvement_threshold}")

# Determine if to promote
if improvement >= min_improvement_threshold:
    action = "promoted"
    # Register as new version and promote
    model_uri = f"runs:/{retrained_run_id}/model"
    new_version = mlflow.register_model(model_uri, registered_model_name)
    # Move production alias to new version
    client.set_registered_model_alias(registered_model_name, "production", int(new_version.version))
    print(f"Retrained model promoted to production as version {new_version.version}")
else:
    action = "kept_champion"
    print(f"Retrained model did not improve enough. Keeping champion in production.")

# Prepare results
results = {
    "original_data_rows": original_rows,
    "new_data_rows": new_rows,
    "combined_data_rows": combined_rows,
    "champion_rmse": champion_rmse,
    "retrained_rmse": round(retrained_rmse, 4),
    "improvement": round(improvement, 4),
    "min_improvement_threshold": min_improvement_threshold,
    "action": action,
    "comparison_metric": "rmse"
}

# Save results
with open("results/step4_s8.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results/step4_s8.json")
