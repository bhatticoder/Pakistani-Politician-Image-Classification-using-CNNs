# 🚀 CATEGORY B - QUICK START GUIDE

## ⏱️ 5-Minute Setup

### Step 0: Before You Start
✅ Dataset uploaded on Kaggle (1,551 images)
✅ Download dataset locally or use current folder
✅ Python 3.8+ installed
✅ Internet connection (for downloading model weights)

---

## 🎯 Complete Pipeline (1 Command)

```bash
pip install -r requirements.txt
python run_pipeline.py
```

**That's it! Everything else runs automatically.**

---

## 📊 What Happens Automatically

```
run_pipeline.py
    │
    ├─→ 1_split_dataset.py
    │   └─→ Creates: dataset_split/train/ val/ test/
    │
    ├─→ 2_augment_data.py
    │   └─→ Doubles training images with augmentation
    │
    ├─→ 3_train_models.py
    │   ├─→ Trains ResNet50 (5-10 min)
    │   └─→ Trains EfficientNetB0 (5-10 min)
    │       Saves: models/*.h5
    │
    ├─→ 3_evaluate_models.py
    │   └─→ Computes metrics & visualizations
    │       Saves: evaluation/*.json, *.png
    │
    └─→ 4_plot_curves.py
        └─→ Generates training curves
            Saves: evaluation/*_curves.png
```

---

## 📁 Output Structure (After Running)

```
├── dataset_split/
│   ├── train/        (augmented training data)
│   ├── val/
│   └── test/
│
├── models/
│   ├── resnet50_final.h5
│   ├── efficientnet_b0_final.h5
│   ├── resnet50_history.pkl
│   ├── efficientnet_b0_history.pkl
│   └── class_names.pkl
│
└── evaluation/       ← **COPY THIS TO YOUR REPORT**
    ├── resnet50_results.json
    ├── resnet50_confusion_matrix.png
    ├── resnet50_training_curves.png
    ├── efficientnet_b0_results.json
    ├── efficientnet_b0_confusion_matrix.png
    ├── efficientnet_b0_training_curves.png
    └── model_comparison.png
```

---

## 💾 Minimum Install

```bash
# Only if you don't have requirements.txt
pip install tensorflow scikit-learn pillow matplotlib seaborn numpy
```

---

## ⏱️ Timing Estimate

| Step | Time | GPU | CPU |
|------|------|-----|-----|
| Split | < 1 min | - | - |
| Augmentation | ~1 min | - | - |
| Train ResNet50 | 5 min | 15 min | - |
| Train EfficientNet | 3 min | 10 min | - |
| Evaluate | ~2 min | - | - |
| Visualize | < 1 min | - | - |
| **TOTAL** | **~15 min** | **40 min** | **GPU RECOMMENDED** |

---

## 📝 For Your Report

### Copy These to Overleaf:

1. **Metrics Table**
   ```
   evaluation/resnet50_results.json
   evaluation/efficientnet_b0_results.json
   ```

2. **Confusion Matrices**
   ```
   evaluation/resnet50_confusion_matrix.png     ← Insert in report
   evaluation/efficientnet_b0_confusion_matrix.png
   ```

3. **Training Curves**
   ```
   evaluation/resnet50_training_curves.png      ← Insert in report
   evaluation/efficientnet_b0_training_curves.png
   evaluation/model_comparison.png
   ```

4. **Per-Class Analysis**
   - Open `.json` files
   - Extract precision/recall/F1 values
   - Create comparison tables

---

## 🐛 Troubleshooting

### ❓ "ModuleNotFoundError: No module named 'tensorflow'"
```bash
pip install -r requirements.txt
```

### ❓ "Out of Memory Error"
```python
# Edit 3_train_models.py, line 8
BATCH_SIZE = 16  # instead of 32
```

### ❓ "CUDA Error" (on GPU systems)
```bash
# Use CPU only
pip install tensorflow-cpu
```

### ❓ Script stops/hangs
- Check internet (downloading weights)
- Restart Python kernel
- Run individual script instead

---

## 🎯 Expected Results

✅ **Accuracy**: 90-95% (target ≥ 90%)
✅ **Precision**: 90-95%
✅ **Recall**: 90-95%
✅ **F1-Score**: 90-95%

Both models should exceed 90% accuracy on test set.

---

## 📋 Checklist Before Submitting

- [ ] `python run_pipeline.py` completes without errors
- [ ] `accuracy ≥ 90%` for both models
- [ ] All `.png` files generated in `evaluation/`
- [ ] All `.json` files with metrics in `evaluation/`
- [ ] Sample confusion matrix images look reasonable
- [ ] Training curves show convergence (not diverging)
- [ ] Copy images to Overleaf report
- [ ] Include metrics tables in report
- [ ] Commit all code to GitHub
- [ ] Record Kaggle dataset link

---

## 🤖 Individual Script Usage

If you need to run scripts separately (e.g., re-evaluate without training):

```bash
# Just split data
python 1_split_dataset.py

# Just evaluate (uses existing trained models)
python 3_evaluate_models.py

# Just plot results
python 4_plot_curves.py
```

---

## 📚 Full Documentation

- **Setup Details**: `TRAINING_GUIDE.md`
- **Implementation**: `IMPLEMENTATION_SUMMARY.md`
- **Kaggle Upload**: `KAGGLE_UPLOAD_GUIDE.md`
- **Code Comments**: Inside each `.py` file

---

## ✨ That's All!

```bash
pip install -r requirements.txt
python run_pipeline.py
# Wait 15-40 minutes...
# All results ready in evaluation/ folder! 🎉
```

**Good luck!** 🚀
