## Quick Reference Guide

### 📊 View Results

#### View All Results Files
```bash
cat results/step1_s1.json  # Task 1
cat results/step2_s6.json  # Task 2
cat results/step3_s7.json  # Task 3
cat results/step4_s8.json  # Task 4
```

#### Launch MLflow Dashboard
```bash
cd c:\Users\jhama\Desktop\MLOPs_Lab_CIE
mlflow ui --backend-store-uri file:///./mlruns
```
Then visit: `http://localhost:5000`

---

### 🔍 Key Findings

**Best Performing Model:**
- Algorithm: SVR (Support Vector Regression)
- Test RMSE: 117.66 kWh
- Test MAE: 110.06 kWh
- Test R²: -0.0174

**Promotion Decisions:**
1. **Task 3:** Champion maintained (v1 vs v2 equal RMSE)
2. **Task 4:** Champion maintained (retrained model 21.5 kWh worse)

**Production Model:**
- Registered Name: `powergrid-energy-kwh-predictor`
- Current Version: 1
- Alias: `production`

---

### 📈 Performance Metrics Comparison

| Model | RMSE | MAE | R² |
|-------|------|-----|-----|
| SVR (Champion) | 117.66 | 110.06 | -0.02 |
| GradientBoosting | 166.60 | 137.87 | -1.04 |
| Challenger (v2) | 117.66 | - | - |
| Retrained | 139.14 | - | - |

---

### 📁 File Locations

```
results/
├── step1_s1.json    → Experiment results & best model selection
├── step2_s6.json    → Model registration details
├── step3_s7.json    → Promotion workflow decision
└── step4_s8.json    → Retraining & final promotion decision

models/
├── best_model_task1.pkl  → Serialized best model
└── best_run_id.txt       → MLflow run ID reference

mlruns/              → MLflow tracking directory
```

---

### 🔧 Running Individual Tasks

Each task can be run independently after Task 1:

```bash
# Task 1: Train and compare models
python src/train.py

# Task 2: Register the best model
python src/register_model.py

# Task 3: Evaluate challenger and promote if better
python src/promote_model.py

# Task 4: Retrain on combined data and decide
python src/retrain.py
```

---

### 🎯 Task 1: Experiment Tracking Results

**Best Model:** SVR

Metrics:
- MAE: 110.059 kWh
- RMSE: 117.6633 kWh (✓ Best)
- R²: -0.0174

Features used:
- temperature_c
- building_sqm
- occupancy_pct
- is_weekday

Test set: 20% of 25 training records (5 samples)

---

### 🔐 Task 2: Model Registration Results

- **Registered Model Name:** powergrid-energy-kwh-predictor
- **Version:** 1
- **Run ID:** 654bbc677e9149ab90efe1797ce60a88
- **Algorithm:** SVR
- **Source Metric:** RMSE = 117.6633

Registered and ready for promotion workflow.

---

### 🚀 Task 3: Promotion Workflow Results

**Champion vs Challenger:**
- Champion (v1): RMSE = 117.6633
- Challenger (v2): RMSE = 117.6633

**Decision:** KEPT (equal performance)
- Challenger random_state: 99
- Champion remains in production
- "production" alias → Version 1

---

### 🔄 Task 4: Retraining Results

**Data Combination:**
- Original: 25 rows
- New: 20 rows
- Total: 45 rows

**Performance:**
- Champion RMSE: 117.6633
- Retrained RMSE: 139.136
- Improvement: -21.4727 (negative = worse)

**Threshold Check:**
- Improvement Required: ≥ 0.5
- Actual Improvement: -21.4727
- **Decision:** KEPT_CHAMPION ✓

Champion model remains in production.

---

### 📝 Data Details

**Training Data (25 records):**
- Temperature: 15-43°C
- Building Size: 60-490 m²
- Occupancy: 22-98%
- Energy: 244-681 kWh

**New Data (20 records):**
- Temperature: 30-89°C (higher distribution)
- Building Size: 56-478 m²
- Occupancy: 60-185% (out of bounds, data quality issue)
- Energy: 518-1004 kWh (higher usage)

**Note:** New data shows distribution shift with higher temperatures and energy consumption.

---

### 🔗 MLflow Model Registry

**Command to view:**
```bash
mlflow models ls
```

**Model details:**
```bash
mlflow models describe --model-name powergrid-energy-kwh-predictor
```

**Versions:**
```bash
mlflow models versions --model-name powergrid-energy-kwh-predictor
```

---

### ✅ Checklist

- [x] Task 1: Train SVR and GradientBoosting → SVR wins
- [x] Task 2: Register best model as v1 → powergrid-energy-kwh-predictor
- [x] Task 3: Train challenger v2 → Equal to champion, keep v1
- [x] Task 4: Retrain on combined data → Worse than champion, keep v1
- [x] Results saved to results/*.json
- [x] MLflow experiments tracked
- [x] Model versions managed
- [x] Production alias set

**Status:** ✅ ALL COMPLETE

---

**Last Updated:** May 4, 2026  
**Project:** MLOps Lab - PowerGrid Energy Consumption Prediction
