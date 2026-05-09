"""
Model Evaluation - Metrics, Confusion Matrix, Misclassified Samples
Category B - Project 2: Pakistani Politician Image Classification
Required: 90% accuracy, precision/recall/F1 per class, confusion matrix
"""

import os
import numpy as np
import pickle
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

class ModelEvaluator:
    """Evaluate model performance"""
    
    def __init__(self, model_path, class_names, img_size=224):
        self.model = tf.keras.models.load_model(model_path)
        self.class_names = class_names
        self.img_size = img_size
        self.model_name = Path(model_path).stem
        
    def evaluate_on_test_set(self, test_dir):
        """Evaluate model on test set"""
        
        # Create test generator
        test_datagen = ImageDataGenerator(
            rescale=1./255,
            preprocessing_function=self._get_preprocessing_fn()
        )
        
        test_generator = test_datagen.flow_from_directory(
            test_dir,
            target_size=(self.img_size, self.img_size),
            batch_size=32,
            class_mode='categorical',
            shuffle=False
        )
        
        # Predict
        print(f"\n📊 Evaluating {self.model_name}...")
        y_pred = self.model.predict(test_generator, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true = test_generator.classes
        
        return y_true, y_pred_classes, y_pred, test_generator
    
    def _get_preprocessing_fn(self):
        """Get preprocessing function based on model"""
        if 'resnet' in self.model_name.lower():
            return tf.keras.applications.resnet50.preprocess_input
        elif 'efficientnet' in self.model_name.lower():
            return tf.keras.applications.efficientnet.preprocess_input
        else:
            return lambda x: x / 255.0
    
    def compute_metrics(self, y_true, y_pred):
        """Compute evaluation metrics"""
        
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        
        print("\n" + "="*70)
        print(f"OVERALL METRICS - {self.model_name.upper()}")
        print("="*70)
        print(f"Accuracy:  {accuracy*100:.2f}%  {'✓ PASS' if accuracy >= 0.90 else '✗ FAIL (Need 90%)'}")
        print(f"Precision: {precision*100:.2f}%")
        print(f"Recall:    {recall*100:.2f}%")
        print(f"F1-Score:  {f1*100:.2f}%")
        print("="*70)
        
        return metrics
    
    def per_class_metrics(self, y_true, y_pred):
        """Compute per-class metrics"""
        
        print(f"\nPER-CLASS METRICS ({self.model_name}):")
        print("-"*70)
        print(f"{'Class':<30} {'Precision':>10} {'Recall':>10} {'F1-Score':>10}")
        print("-"*70)
        
        per_class = {}
        for i, class_name in enumerate(self.class_names):
            mask = y_true == i
            if mask.sum() == 0:
                continue
            
            p = precision_score(y_true, y_pred, labels=[i], zero_division=0)[0]
            r = recall_score(y_true, y_pred, labels=[i], zero_division=0)[0]
            f = f1_score(y_true, y_pred, labels=[i], zero_division=0)[0]
            
            per_class[class_name] = {
                'precision': p,
                'recall': r,
                'f1_score': f,
                'support': mask.sum()
            }
            
            print(f"{class_name:<30} {p*100:>9.2f}% {r*100:>9.2f}% {f*100:>9.2f}%")
        
        print("-"*70)
        return per_class
    
    def plot_confusion_matrix(self, y_true, y_pred, output_dir="evaluation"):
        """Plot and save confusion matrix"""
        
        Path(output_dir).mkdir(exist_ok=True)
        
        cm = confusion_matrix(y_true, y_pred)
        
        # Plot
        plt.figure(figsize=(16, 14))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.class_names,
                    yticklabels=self.class_names,
                    cbar_kws={'label': 'Count'})
        
        plt.title(f'Confusion Matrix - {self.model_name.upper()}', fontsize=16, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        output_path = Path(output_dir) / f"{self.model_name}_confusion_matrix.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Confusion matrix saved: {output_path}")
        plt.close()
        
        return cm
    
    def find_misclassified_samples(self, y_true, y_pred, y_pred_proba, test_generator, top_k=5):
        """Find and save top misclassified samples"""
        
        misclassified_indices = np.where(y_true != y_pred)[0]
        
        if len(misclassified_indices) == 0:
            print("✓ No misclassified samples!")
            return
        
        # Get confidence scores
        confidence = np.max(y_pred_proba, axis=1)
        
        # Sort by confidence (high confidence wrong predictions are most interesting)
        sorted_indices = misclassified_indices[np.argsort(-confidence[misclassified_indices])][:top_k]
        
        print(f"\n🔍 TOP {top_k} MISCLASSIFIED SAMPLES ({self.model_name}):")
        print("-"*70)
        
        fig, axes = plt.subplots(1, top_k, figsize=(20, 4))
        if top_k == 1:
            axes = [axes]
        
        for plot_idx, sample_idx in enumerate(sorted_indices):
            true_label = self.class_names[y_true[sample_idx]]
            pred_label = self.class_names[y_pred[sample_idx]]
            confidence_score = confidence[sample_idx]
            
            print(f"{plot_idx+1}. True: {true_label:25} | Pred: {pred_label:25} | Conf: {confidence_score*100:.1f}%")
            
            # Get image from generator
            # This is approximate - ideally you'd save image paths during prediction
            axes[plot_idx].text(0.5, 0.5, f"True: {true_label}\nPred: {pred_label}\nConf: {confidence_score*100:.1f}%",
                              ha='center', va='center', fontsize=10)
            axes[plot_idx].axis('off')
        
        print("-"*70)
        
        plt.suptitle(f'Top {top_k} Misclassified Samples - {self.model_name}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        output_path = Path("evaluation") / f"{self.model_name}_misclassified.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Misclassified samples visualization saved: {output_path}")
        plt.close()
    
    def save_results(self, metrics, per_class_metrics, cm, output_dir="evaluation"):
        """Save all results to JSON"""
        
        Path(output_dir).mkdir(exist_ok=True)
        
        results = {
            'model': self.model_name,
            'overall_metrics': metrics,
            'per_class_metrics': {k: {kk: float(vv) for kk, vv in v.items()} 
                                 for k, v in per_class_metrics.items()},
            'confusion_matrix': cm.tolist()
        }
        
        output_path = Path(output_dir) / f"{self.model_name}_results.json"
        with open(output_path, 'w') as f:
            import json
            json.dump(results, f, indent=2)
        
        print(f"✓ Results saved: {output_path}")

def main():
    """Main evaluation pipeline"""
    
    print("\n" + "="*70)
    print("📊 MODEL EVALUATION")
    print("="*70)
    
    # Load class names
    class_names_path = Path("models/class_names.pkl")
    if not class_names_path.exists():
        print("❌ Class names file not found!")
        return
    
    with open(class_names_path, 'rb') as f:
        class_names = pickle.load(f)
    
    print(f"Classes loaded: {len(class_names)}")
    
    # Paths
    TEST_DIR = "dataset_split/test"
    MODELS_DIR = "models"
    OUTPUT_DIR = "evaluation"
    
    if not Path(TEST_DIR).exists():
        print("❌ Test dataset not found!")
        return
    
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Evaluate each model
    model_paths = list(Path(MODELS_DIR).glob("*_final.h5"))
    
    all_results = {}
    
    for model_path in sorted(model_paths):
        evaluator = ModelEvaluator(str(model_path), class_names)
        
        # Evaluate
        y_true, y_pred, y_pred_proba, test_gen = evaluator.evaluate_on_test_set(TEST_DIR)
        
        # Metrics
        metrics = evaluator.compute_metrics(y_true, y_pred)
        per_class = evaluator.per_class_metrics(y_true, y_pred)
        
        # Visualizations
        cm = evaluator.plot_confusion_matrix(y_true, y_pred, OUTPUT_DIR)
        evaluator.find_misclassified_samples(y_true, y_pred, y_pred_proba, test_gen, top_k=5)
        
        # Save
        evaluator.save_results(metrics, per_class, cm, OUTPUT_DIR)
        
        all_results[evaluator.model_name] = metrics
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY - ALL MODELS")
    print("="*70)
    for model_name, metrics in all_results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy:  {metrics['accuracy']*100:.2f}%")
        print(f"  Precision: {metrics['precision']*100:.2f}%")
        print(f"  Recall:    {metrics['recall']*100:.2f}%")
        print(f"  F1-Score:  {metrics['f1_score']*100:.2f}%")
    print("="*70)

if __name__ == "__main__":
    main()
