"""
Verification script to validate all MLOps lab requirements are met
"""

import json
import os
from pathlib import Path

def verify_project():
    """Verify all project requirements are met"""
    
    base_path = Path(".")
    results = {
        "status": "✓ PASS",
        "checks": []
    }
    
    # Check 1: Directory structure
    required_dirs = ["data", "src", "models", "results"]
    for dir_name in required_dirs:
        path = base_path / dir_name
        if path.is_dir():
            results["checks"].append(f"✓ Directory {dir_name}/ exists")
        else:
            results["checks"].append(f"✗ Directory {dir_name}/ MISSING")
            results["status"] = "✗ FAIL"
    
    # Check 2: Data files
    data_files = [
        ("data/training_data.csv", 25),
        ("data/new_data.csv", 20)
    ]
    for file_path, expected_rows in data_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                rows = len(lines) - 1  # Exclude header
                if rows == expected_rows:
                    results["checks"].append(f"✓ {file_path} ({rows} rows)")
                else:
                    results["checks"].append(f"✗ {file_path} has {rows} rows, expected {expected_rows}")
                    results["status"] = "✗ FAIL"
        else:
            results["checks"].append(f"✗ {file_path} MISSING")
            results["status"] = "✗ FAIL"
    
    # Check 3: Source files
    src_files = [
        "src/train.py",
        "src/register_model.py",
        "src/promote_model.py",
        "src/retrain.py"
    ]
    for file_path in src_files:
        if os.path.exists(file_path):
            results["checks"].append(f"✓ {file_path} exists")
        else:
            results["checks"].append(f"✗ {file_path} MISSING")
            results["status"] = "✗ FAIL"
    
    # Check 4: Results JSON files
    results_files = [
        "results/step1_s1.json",
        "results/step2_s6.json",
        "results/step3_s7.json",
        "results/step4_s8.json"
    ]
    
    for file_path in results_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
                results["checks"].append(f"✓ {file_path} (valid JSON)")
            except json.JSONDecodeError:
                results["checks"].append(f"✗ {file_path} (invalid JSON)")
                results["status"] = "✗ FAIL"
        else:
            results["checks"].append(f"✗ {file_path} MISSING")
            results["status"] = "✗ FAIL"
    
    # Check 5: Configuration files
    config_files = [
        "requirements.txt",
        ".gitignore",
        "README.md"
    ]
    for file_path in config_files:
        if os.path.exists(file_path):
            results["checks"].append(f"✓ {file_path} exists")
        else:
            results["checks"].append(f"✗ {file_path} MISSING")
    
    # Check 6: Validate results content
    try:
        with open("results/step1_s1.json", 'r') as f:
            step1 = json.load(f)
            if step1.get("best_model") in ["SVR", "GradientBoosting"]:
                results["checks"].append("✓ Task 1: Best model selected")
            else:
                results["checks"].append("✗ Task 1: Invalid best model")
                results["status"] = "✗ FAIL"
        
        with open("results/step2_s6.json", 'r') as f:
            step2 = json.load(f)
            if step2.get("version") == 1:
                results["checks"].append("✓ Task 2: Model registered as v1")
            else:
                results["checks"].append("✗ Task 2: Invalid version")
                results["status"] = "✗ FAIL"
        
        with open("results/step3_s7.json", 'r') as f:
            step3 = json.load(f)
            if step3.get("alias_name") == "production":
                results["checks"].append("✓ Task 3: Production alias configured")
            else:
                results["checks"].append("✗ Task 3: Missing production alias")
                results["status"] = "✗ FAIL"
        
        with open("results/step4_s8.json", 'r') as f:
            step4 = json.load(f)
            if step4.get("combined_data_rows") == 45:
                results["checks"].append("✓ Task 4: Combined data = 45 rows")
            else:
                results["checks"].append("✗ Task 4: Invalid combined data rows")
                results["status"] = "✗ FAIL"
            
            if step4.get("action") in ["promoted", "kept_champion"]:
                results["checks"].append("✓ Task 4: Valid promotion decision")
            else:
                results["checks"].append("✗ Task 4: Invalid promotion decision")
                results["status"] = "✗ FAIL"
    
    except Exception as e:
        results["checks"].append(f"✗ Error validating results: {str(e)}")
        results["status"] = "✗ FAIL"
    
    return results

if __name__ == "__main__":
    print("="*70)
    print("MLOps Lab Verification")
    print("="*70)
    
    verify_results = verify_project()
    
    for check in verify_results["checks"]:
        print(check)
    
    print("="*70)
    print(f"Status: {verify_results['status']}")
    print("="*70)
