# brain-tumor-classification-and-detection

<h3>Image Classification Using Baseline CNN, U-Net, and Inception Models</h3>

<p>This repository presents a comparative study of different deep learning architectures for image classification tasks in computer vision. A baseline CNN, U-Net, and Inception-based models were implemented and evaluated to analyze their performance across multiple metrics.</p>

## 🧠 Models Implemented
### Baseline CNN
- Simple convolutional architecture
- Used as a performance reference model

### U-Net 
- Encoder–decoder architecture
- Adapted for classification by modifying the output layers

### Inception Model
- Multi-scale convolutional filters
- Designed to capture diverse spatial features

## 📂 Dataset

The dataset used in this project was obtained from Kaggle:

**Brain Tumors Dataset**  
Author: Mohammad Hossein  
Source: Kaggle

The dataset contains MRI images of brain tumors categorized into multiple classes and is commonly used for image classification tasks in medical imaging.

### Dataset Details
- Image type: MRI scans
- Number of classes: 4
- Image size: 128 × 128 (resized during preprocessing)
- Format: JPG / PNG
- Split: Train / Validation

The dataset was downloaded using the Kaggle API:


```bash
kaggle datasets download -d mohammadhossein77/brain-tumors-dataset
```

## 📊 Evaluation Metrics


- Accuracy
- Precision
- Recall
- F1-score
- AUC
  
## 👁️ Visualization

<p>the outputs of individual layers were visualized to better understand feature extraction at different network depths. Model architecture and layer-wise visualizations were generated using the visualkeras library.</p>

## 🧩 Technologies Used

- Python
- TensorFlow / Keras
- NumPy
- Matplotlib
- Scikit-learn

## 📄 References

- U-Net  Olaf Ronneberger, Philipp Fischer, Thomas Brox. "U-Net: Convolutional Networks for Biomedical Image Segmentation" (2015) https://arxiv.org/abs/1505.04597v1
- Inception v2 Model Christian Szegedy, et al. "Going Deeper with Convolutions" (2015) https://arxiv.org/abs/1409.4842

<B>In the future, I plan to investigate a wider range of deep learning architectures and continue strengthening my research perspective in computer vision
