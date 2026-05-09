"""
Master Pipeline Runner
Category B - Project 2: Pakistani Politician Image Classification
Run all steps in sequence: split → augment → train → evaluate → visualize
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    
    print("\n" + "="*70)
    print(f"▶️  {description}")
    print(f"    Script: {script_name}")
    print("="*70)
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        print(f"\n✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error in {script_name}!")
        print(f"   Exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Script not found: {script_name}")
        return False

def main():
    """Run complete pipeline"""
    
    print("\n" + "="*70)
    print("🚀 CATEGORY B - PROJECT 2 COMPLETE PIPELINE")
    print("Pakistani Politician Image Classification")
    print("="*70)
    
    scripts = [
        ("1_split_dataset.py", "Step 1: Split Dataset (75/15/10)"),
        ("2_augment_data.py", "Step 2: Data Augmentation (Training Set)"),
        ("3_train_models.py", "Step 3: Train CNN Models (ResNet50, EfficientNetB0)"),
        ("3_evaluate_models.py", "Step 4: Evaluate Models & Compute Metrics"),
        ("4_plot_curves.py", "Step 5: Generate Training Curves & Visualizations"),
    ]
    
    failed_scripts = []
    
    for script, description in scripts:
        if not Path(script).exists():
            print(f"\n❌ Script not found: {script}")
            failed_scripts.append(script)
            continue
        
        if not run_script(script, description):
            failed_scripts.append(script)
            
            # Ask to continue or stop
            while True:
                response = input(f"\nContinue despite error? (y/n): ").lower()
                if response in ['y', 'n']:
                    break
            
            if response == 'n':
                print("\n⛔ Pipeline stopped by user.")
                return False
    
    # Summary
    print("\n" + "="*70)
    print("📋 PIPELINE SUMMARY")
    print("="*70)
    
    if failed_scripts:
        print(f"\n❌ {len(failed_scripts)} script(s) failed:")
        for script in failed_scripts:
            print(f"   - {script}")
    else:
        print("\n✓ All scripts completed successfully!")
    
    print("\n📁 Output Directories:")
    print(f"   - dataset_split/  (train/val/test split)")
    print(f"   - models/         (trained models & history)")
    print(f"   - evaluation/     (metrics & visualizations)")
    
    print("\n📊 Generated Files:")
    print(f"   - Confusion matrices (PNG)")
    print(f"   - Training curves (PNG)")
    print(f"   - Model comparison (PNG)")
    print(f"   - Evaluation metrics (JSON)")
    
    print("\n" + "="*70)
    print("✓ PIPELINE COMPLETE!")
    print("Next: Review results in evaluation/ directory")
    print("="*70)
    
    return not failed_scripts

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
