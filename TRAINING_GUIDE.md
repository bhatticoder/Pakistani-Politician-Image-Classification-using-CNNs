# Category B - Project 2: Pakistani Politician Image Classification

Complete CNN-based image classification pipeline for 16 Pakistani political figures.

## 📋 Project Requirements

✅ **Minimum 2 CNN Models**: ResNet-50, EfficientNetB0  
✅ **90% Accuracy Required**  
✅ **Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score (per class)  
✅ **Visualizations**: Confusion Matrix, Training Curves, Misclassified Samples  
✅ **Dataset**: 1,551 images across 16 classes  

---

## 🚀 Quick Start

### Step 1: Prepare Dataset
```bash
python 1_split_dataset.py
```
Splits dataset into:
- **Train**: 75% (1,163 images)
- **Validation**: 15% (232 images)  
- **Test**: 10% (156 images)

Output: `dataset_split/train/`, `dataset_split/val/`, `dataset_split/test/`

### Step 2: Data Augmentation (Training Only)
```bash
python 2_augment_data.py
```
Applies to training set:
- ✓ Rotation (-15° to +15°)
- ✓ Horizontal Flip
- ✓ Brightness Variation (70% - 130%)
- ✓ Zoom (80% - 100%)
- ✓ Random Crop (10%)

Creates 2 augmented versions per original image.

### Step 3: Train Models
```bash
python 3_train_models.py
```
Trains 2 models:
1. **ResNet50** - Transfer learning from ImageNet
2. **EfficientNetB0** - Lightweight efficient architecture

Configuration:
- Image Size: 224×224
- Batch Size: 32
- Epochs: 30
- Optimizer: Adam (lr=1e-4)
- Loss: Categorical Crossentropy

Output: `models/`
- `resnet50_final.h5` - Trained model
- `resnet50_history.pkl` - Training history
- `efficientnet_b0_final.h5` - Trained model
- `efficientnet_b0_history.pkl` - Training history
- `class_names.pkl` - Class mapping

### Step 4: Evaluate Models
```bash
python 3_evaluate_models.py
```
Computes:
- ✓ Overall Accuracy, Precision, Recall, F1-Score
- ✓ Per-class metrics
- ✓ Confusion Matrix (heatmap)
- ✓ Top 5 misclassified samples

Output: `evaluation/`
- `resnet50_results.json` - Metrics
- `resnet50_confusion_matrix.png` - Confusion matrix
- `resnet50_misclassified.png` - Misclassified samples
- `efficientnet_b0_results.json` - Metrics
- `efficientnet_b0_confusion_matrix.png` - Confusion matrix
- (Same for EfficientNet)

### Step 5: Visualize Results
```bash
python 4_plot_curves.py
```
Generates training curves:
- Training vs Validation Accuracy
- Training vs Validation Loss
- Model Comparison (all models)

Output: `evaluation/`
- `resnet50_training_curves.png`
- `efficientnet_b0_training_curves.png`
- `model_comparison.png`

---

## 📊 Dataset Structure

```
dataset_split/
├── train/          # 75% of data
│   ├── Imran_Khan/
│   ├── Nawaz_Sharif/
│   ├── ... (16 classes)
│
├── val/            # 15% of data
│   ├── Imran_Khan/
│   ├── ...
│
└── test/           # 10% of data
    ├── Imran_Khan/
    ├── ...
```

## 🎯 Expected Results

**Target Accuracy**: ≥ 90%

### Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| ResNet50 | ~92-95% | ~92-95% | ~92-95% | ~92-95% |
| EfficientNetB0 | ~90-93% | ~90-93% | ~90-93% | ~90-93% |

**Note**: Actual results depend on image quality and data augmentation effectiveness.

---

## 📦 Dependencies

```
tensorflow>=2.10
keras>=2.10
scikit-learn
numpy
pillow
matplotlib
seaborn
```

Install:
```bash
pip install tensorflow scikit-learn numpy pillow matplotlib seaborn
```

---

## 🏗️ Architecture Details

### ResNet50
- **Base**: ResNet50 (ImageNet pretrained)
- **Frozen Layers**: Yes (transfer learning)
- **Top Layers**:
  - Global Average Pooling
  - Dense 512 (ReLU, Dropout 30%)
  - Dense 256 (ReLU, Dropout 20%)
  - Dense 16 (Softmax for 16 classes)
- **Parameters**: ~25M

### EfficientNetB0
- **Base**: EfficientNetB0 (ImageNet pretrained)
- **Frozen Layers**: Yes (transfer learning)
- **Top Layers**: Same as ResNet50
- **Parameters**: ~5.3M (more efficient)

---

## 📈 Training Strategy

1. **Transfer Learning**: Freeze pretrained weights
2. **Learning Rate**: 1e-4 (small for fine-tuning)
3. **Batch Size**: 32
4. **Early Stopping**: Stop if val_loss doesn't improve for 5 epochs
5. **Learning Rate Reduction**: 50% reduction after 3 epochs without improvement
6. **Checkpoint**: Save best model based on validation accuracy

---

## 🔍 Evaluation Metrics

### Overall Performance
- **Accuracy**: Correct predictions / Total predictions
- **Precision**: True Positives / (True Positives + False Positives)
- **Recall**: True Positives / (True Positives + False Negatives)
- **F1-Score**: Harmonic mean of Precision and Recall

### Per-Class Analysis
Each politician gets individual metrics to identify:
- Easy vs hard to classify
- Class-specific misclassification patterns

### Confusion Matrix
Shows which classes are confused with each other:
- Diagonal = correct predictions
- Off-diagonal = misclassifications

---

## 🐛 Troubleshooting

### Out of Memory Error
Reduce batch size in training scripts:
```python
BATCH_SIZE = 16  # instead of 32
```

### Low Accuracy (<90%)
1. Check if data augmentation is applied
2. Increase EPOCHS in `3_train_models.py`
3. Collect more images for problematic classes
4. Try other pretrained models (ResNet101, EfficientNetB2)

### Missing Class Files
Run `1_split_dataset.py` again to regenerate split

---

## 📁 Output Files

After running all scripts:

```
dataset_split/          # Split dataset
├── train/
├── val/
└── test/

models/                 # Trained models
├── resnet50_final.h5
├── resnet50_history.pkl
├── efficientnet_b0_final.h5
├── efficientnet_b0_history.pkl
└── class_names.pkl

evaluation/            # Results & visualizations
├── resnet50_results.json
├── resnet50_confusion_matrix.png
├── resnet50_training_curves.png
├── resnet50_misclassified.png
├── efficientnet_b0_results.json
├── efficientnet_b0_confusion_matrix.png
├── efficientnet_b0_training_curves.png
├── efficientnet_b0_misclassified.png
└── model_comparison.png
```

---

## 📝 Notes for Report

Include in your Overleaf IEEE format report:

### Dataset Collection
- Total images: 1,551
- Classes: 16 politicians
- Image sources: Google Images, Wikipedia, News websites
- Preprocessing: Resized to 224×224, normalized

### Methodology
- Train/Val/Test Split: 75/15/10
- Data Augmentation: Applied only to training set
- Augmentation techniques: Rotation, Flip, Brightness, Zoom, Crop
- Models: ResNet50, EfficientNetB0
- Framework: TensorFlow/Keras

### Results
- Include confusion matrix heatmaps
- Per-class precision/recall/F1 tables
- Training curves (accuracy & loss)
- Top 5 misclassified samples analysis
- Overall accuracy vs. 90% requirement

### Challenges
- Class imbalance (Asad_Umar had fewer images)
- Similarity between some politicians (family members)
- Image quality variations
- Computational resource management

---

## ✅ Submission Checklist

- [ ] Dataset uploaded to Kaggle
- [ ] All scripts run successfully
- [ ] Accuracy ≥ 90%
- [ ] Confusion matrices generated
- [ ] Training curves visualized
- [ ] Per-class metrics computed
- [ ] Report written (Overleaf IEEE)
- [ ] GitHub repository created
- [ ] Code committed with descriptive messages
- [ ] README.md included

---

**Good luck with your project!** 🎯

For questions, refer to individual script docstrings or the main README.
