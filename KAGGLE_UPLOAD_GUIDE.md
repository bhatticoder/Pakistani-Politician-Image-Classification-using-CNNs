# Kaggle Upload Guide - Pakistani Politician Dataset

## Step 1: Get Kaggle API Credentials

1. **Go to Kaggle Account Settings**
   - Visit: https://www.kaggle.com/account
   - Click on "Account" tab
   - Scroll down to "API" section
   - Click **"Create New Token"**
   - This downloads `kaggle.json`

2. **Place the Credentials File**
   - Create folder: `C:\Users\Mudasar Bhatti\.kaggle\`
   - Move the downloaded `kaggle.json` into this folder
   - Verify the location: `C:\Users\Mudasar Bhatti\.kaggle\kaggle.json`

## Step 2: Create Dataset on Kaggle Website

1. Go to: https://www.kaggle.com/datasets/create/new
2. Fill in the details:
   - **Title**: `Pakistani Politicians Face Recognition Dataset`
   - **Public URL Slug**: `pakistani-politicians-face-dataset` (or your choice)
   - **Description**: 
     ```
     A dataset containing 1400+ facial images of 16 Pakistani public figures for 
     CNN-based image classification. Classes include politicians and military officials.
     
     Dataset Structure:
     - 16 classes (politicians)
     - 80-144 images per class
     - Total: 1400+ images
     - Used for deep learning and face recognition tasks.
     ```
   - **License**: Select "CC0: Public Domain"
   - **Visibility**: Select "Private" (you can make it public later)

3. Click **"Create"**
4. Note your dataset slug from the URL: `https://www.kaggle.com/datasets/YOUR_USERNAME/YOUR_SLUG`

## Step 3: Upload Dataset

Once you have the `kaggle.json` file in place and dataset created on Kaggle:

### For **First Time Upload** (Create):
```powershell
cd "g:\Fast\Semester 6\DataSet for Project 2"
python upload_dataset.py --create
```

### For **Subsequent Updates** (Version):
```powershell
cd "g:\Fast\Semester 6\DataSet for Project 2"
python upload_dataset.py --update --message "Updated with more images"
```

## Dataset Statistics

| Politician | Image Count |
|-----------|------------|
| Asad_Umar | 64 ⚠️ (Below 80 minimum) |
| asif_zardari | 96 ✓ |
| Benazir_Bhutto | 142 ✓ |
| Bilawal Bhutto | 80 ✓ |
| Imran_Khan | 102 ✓ |
| Khawaja_Asif | 94 ✓ |
| Maryam Nawaz | 80 ✓ |
| Mohsin naqvi | 80 ✓ |
| Nawaz_Sharif | 93 ✓ |
| pervaiz_elahi | 80 ✓ |
| Pervez_Musharraf | 95 ✓ |
| Shah_Mahmood_Qureshi | 144 ✓ |
| Shehbaz_Sharif | 88 ✓ |
| Sheikh Rasheed Ahmed | 80 ✓ |
| shireen_mazari | 83 ✓ |
| Siraj-ul-Haq | 80 ✓ |
| **TOTAL** | **1,551** |

**⚠️ Action Required**: Asad_Umar needs 16 more images to meet the 80-image minimum.

## Troubleshooting

### Error: `kaggle: command not found`
```powershell
python -m kaggle --version
```

### Error: `Credentials not found`
- Verify `C:\Users\Mudasar Bhatti\.kaggle\kaggle.json` exists
- Check file permissions are readable
- Restart PowerShell after placing the file

### Error: `Dataset not found`
- Make sure you created the dataset on Kaggle website first
- Check the dataset slug matches exactly

## Next Steps After Upload

1. Share dataset link with your team
2. Download and process for model training:
   - Split into train/val/test (75/15/10)
   - Apply data augmentation on training set
3. Build CNN models (ResNet-50, EfficientNet, etc.)
4. Train and evaluate

---
