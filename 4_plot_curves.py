"""
Training & Validation Curves Visualization
Category B - Project 2: Pakistani Politician Image Classification
Plot accuracy and loss curves from training history
"""

import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def plot_training_history(model_name, history_dict, output_dir="evaluation"):
    """Plot training and validation curves"""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy
    axes[0].plot(history_dict['accuracy'], label='Training Accuracy', linewidth=2)
    axes[0].plot(history_dict['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[0].set_title(f'{model_name} - Accuracy', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Loss
    axes[1].plot(history_dict['loss'], label='Training Loss', linewidth=2)
    axes[1].plot(history_dict['val_loss'], label='Validation Loss', linewidth=2)
    axes[1].set_title(f'{model_name} - Loss', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = Path(output_dir) / f"{model_name}_training_curves.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Training curves saved: {output_path}")
    plt.close()

def plot_model_comparison(history_dict, output_dir="evaluation"):
    """Plot all models side by side"""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy comparison
    for model_name, history in history_dict.items():
        axes[0].plot(history['val_accuracy'], label=model_name, linewidth=2)
    
    axes[0].set_title('Validation Accuracy Comparison', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Loss comparison
    for model_name, history in history_dict.items():
        axes[1].plot(history['val_loss'], label=model_name, linewidth=2)
    
    axes[1].set_title('Validation Loss Comparison', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_path = Path(output_dir) / "model_comparison.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Model comparison saved: {output_path}")
    plt.close()

def main():
    """Plot training curves"""
    
    print("\n" + "="*70)
    print("📈 TRAINING CURVES VISUALIZATION")
    print("="*70)
    
    MODELS_DIR = "models"
    OUTPUT_DIR = "evaluation"
    
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Load all history files
    history_files = list(Path(MODELS_DIR).glob("*_history.pkl"))
    
    if not history_files:
        print("❌ No training history files found!")
        return
    
    all_histories = {}
    
    for hist_file in sorted(history_files):
        model_name = hist_file.stem.replace("_history", "")
        
        with open(hist_file, 'rb') as f:
            history = pickle.load(f)
        
        print(f"\nProcessing: {model_name}")
        
        # Plot individual
        plot_training_history(model_name, history, OUTPUT_DIR)
        
        # Store for comparison
        all_histories[model_name] = history
    
    # Plot comparison
    if len(all_histories) > 1:
        print("\nGenerating model comparison...")
        plot_model_comparison(all_histories, OUTPUT_DIR)
    
    print("\n" + "="*70)
    print("✓ All visualizations saved in:", OUTPUT_DIR)
    print("="*70)

if __name__ == "__main__":
    main()
