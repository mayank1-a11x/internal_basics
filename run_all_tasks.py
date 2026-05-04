"""
Master script to execute all MLOps tasks sequentially
"""

import subprocess
import sys
import os

os.chdir(r"c:\Users\jhama\Desktop\MLOPs_Lab_CIE")

tasks = [
    ("Task 1: Experiment Tracking & Model Comparison", "python src/train.py"),
    ("Task 2: Model Versioning", "python src/register_model.py"),
    ("Task 3: Model Promotion", "python src/promote_model.py"),
    ("Task 4: Retraining Pipeline", "python src/retrain.py")
]

print("="*70)
print("MLOps Lab - PowerGrid Energy Consumption Prediction")
print("="*70)

for task_name, command in tasks:
    print(f"\n{'='*70}")
    print(f"Running: {task_name}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✓ {task_name} completed successfully")
        else:
            print(f"✗ {task_name} failed with return code {result.returncode}")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error running {task_name}: {str(e)}")
        sys.exit(1)

print(f"\n{'='*70}")
print("All tasks completed successfully!")
print(f"{'='*70}")
print("\nResults saved to:")
print("  - results/step1_s1.json (Task 1: Experiment Tracking)")
print("  - results/step2_s6.json (Task 2: Model Versioning)")
print("  - results/step3_s7.json (Task 3: Model Promotion)")
print("  - results/step4_s8.json (Task 4: Retraining Pipeline)")
