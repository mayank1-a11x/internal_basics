"""
Task 2: Model Versioning
Register the best model from Task 1 in the MLflow Model Registry.
"""

import json
import pickle
import mlflow
import mlflow.sklearn
from mlflow.entities.metric import Metric
from mlflow import MlflowClient

# Set MLflow tracking URI
mlflow.set_tracking_uri("file:///./mlruns")

# Read the best run ID from Task 1
with open("models/best_run_id.txt", "r") as f:
    best_run_id = f.read().strip()

# Get best model metrics
client = MlflowClient()
run = client.get_run(best_run_id)
metrics = run.data.metrics

# Registered model name
registered_model_name = "powergrid-energy-kwh-predictor"

# Register the model
print(f"Registering model: {registered_model_name}")
try:
    # Try to get existing model
    model_version = client.get_registered_model(registered_model_name)
except:
    # Create new registered model
    pass

# Register model from the best run
model_uri = f"runs:/{best_run_id}/model"
model_version = mlflow.register_model(model_uri, registered_model_name)

print(f"Model registered successfully!")
print(f"Registered model name: {registered_model_name}")
print(f"Version: {model_version.version}")
print(f"Run ID: {best_run_id}")

# Prepare results
results = {
    "registered_model_name": registered_model_name,
    "version": int(model_version.version),
    "run_id": best_run_id,
    "source_metric": "rmse",
    "source_metric_value": round(metrics.get("rmse", 0.0), 4)
}

# Save results
with open("results/step2_s6.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results/step2_s6.json")
