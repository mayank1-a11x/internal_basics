# MLOps Lab: PowerGrid Energy Consumption Prediction

## Overview
This project demonstrates a complete MLOps workflow for predicting energy consumption in commercial buildings managed by PowerGrid.

## Project Structure
```
MLOPs_Lab_CIE/
├── data/
│   ├── training_data.csv          # 25 rows of training data
│   └── new_data.csv               # 20 rows of new data with shifted distributions
├── src/
│   ├── train.py                   # Task 1: Train and compare models
│   ├── register_model.py          # Task 2: Register models in MLflow Registry
│   ├── promote_model.py           # Task 3: Promote best model to production
│   └── retrain.py                 # Task 4: Retrain on combined data
├── models/
│   ├── best_model_task1.pkl       # Best model from Task 1
│   └── best_run_id.txt            # MLflow run ID of best model
├── results/
│   ├── step1_s1.json              # Task 1 results
│   ├── step2_s6.json              # Task 2 results
│   ├── step3_s7.json              # Task 3 results
│   └── step4_s8.json              # Task 4 results
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── run_all_tasks.py              # Master script to run all tasks
└── README.md                      # This file
```

## Features
- **temperature_c**: Room temperature in Celsius (15-45°C)
- **building_sqm**: Building area in square meters (50-500 m²)
- **occupancy_pct**: Building occupancy percentage (20-100%)
- **is_weekday**: Binary indicator (1=weekday, 0=weekend)
- **energy_kwh**: Energy consumption in kilowatt-hours (target variable)

## Tasks

### Task 1: Experiment Tracking & Model Comparison
Train SVR and GradientBoosting models with MLflow tracking.

**Outputs:**
- Logs hyperparameters, metrics (MAE, RMSE, R²), and tags to MLflow
- Selects best model by RMSE
- Saves results to `results/step1_s1.json`

**Run:**
```bash
python src/train.py
```

### Task 2: Model Versioning
Register the best model in MLflow Model Registry.

**Outputs:**
- Registers model with name `powergrid-energy-kwh-predictor`
- Records version number and run ID
- Saves results to `results/step2_s6.json`

**Run:**
```bash
python src/register_model.py
```

### Task 3: Model Promotion
Set up promotion workflow with alias management.

**Outputs:**
- Trains second model variant with random_state=99
- Registers as version 2
- Compares with version 1 (champion)
- Moves "production" alias if version 2 is better
- Saves results to `results/step3_s7.json`

**Run:**
```bash
python src/promote_model.py
```

### Task 4: Retraining Pipeline
Retrain on combined data and decide on promotion.

**Outputs:**
- Combines training_data.csv + new_data.csv
- Retrains the same model type from Task 1
- Compares against champion on same test set
- Promotes only if RMSE improves by ≥0.5
- Saves results to `results/step4_s8.json`

**Run:**
```bash
python src/retrain.py
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tasks
Execute all tasks sequentially:
```bash
python run_all_tasks.py
```

Or run individually:
```bash
python src/train.py                 # Task 1
python src/register_model.py        # Task 2
python src/promote_model.py         # Task 3
python src/retrain.py               # Task 4
```

## MLflow Integration

### View MLflow Dashboard
```bash
mlflow ui --backend-store-uri file:///./mlruns
```

The dashboard will be available at `http://localhost:5000`

### MLflow Artifacts
- Experiment: `powergrid-energy-kwh`
- Registered Model: `powergrid-energy-kwh-predictor`
- Aliases: `production`

## Results Summary

Each task generates a JSON file in the `results/` directory:

- **step1_s1.json**: Model comparison metrics
- **step2_s6.json**: Model registration details
- **step3_s7.json**: Promotion decision and version comparison
- **step4_s8.json**: Retraining results and promotion decision

## Dependencies

| Package | Version |
|---------|---------|
| pandas | 2.0.3 |
| numpy | 1.24.3 |
| scikit-learn | 1.3.0 |
| mlflow | 2.10.0 |

## Notes

- All tasks use the same random_state=42 for reproducibility (except Task 3 challenger with random_state=99)
- Test set is fixed across all tasks for fair comparison (20% test split)
- RMSE is the primary metric for model comparison
- Production alias is managed via MLflow Model Registry
- Combined data in Task 4 = 25 (original) + 20 (new) = 45 rows

## Author
MLOps Engineer - PowerGrid

## Date
May 2026
