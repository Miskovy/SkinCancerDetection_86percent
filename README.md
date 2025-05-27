## 🔬 Skin Cancer Detection System
An AI-powered dermatological analysis tool using deep learning for automated skin cancer detection. This comprehensive system combines state-of-the-art computer vision with an intuitive user interface to provide accessible preliminary screening capabilities.
## 🎯 Project Overview
This project implements an end-to-end machine learning solution for binary classification of skin lesions as malignant or benign. Built using MobileNetV2 architecture with transfer learning, the system processes dermoscopic images and provides confidence-scored predictions with risk assessments.
## ⚕️ Medical Disclaimer
This tool is for educational and research purposes only. Always consult healthcare professionals for medical diagnosis and treatment decisions.
## 🚀 Features

Advanced CNN Architecture: MobileNetV2-based model with transfer learning
RESTful API: Flask-based web service for model serving
Desktop GUI: Modern Tkinter interface with professional design
Real-time Analysis: Instant image processing with confidence scoring
Risk Assessment: Categorized risk levels with medical recommendations
Multi-format Support: JPEG, PNG, BMP, and GIF image compatibility

## 🛠️ Technical Stack
ComponentTechnologyDeep LearningTensorFlow, Keras, MobileNetV2Backend APIFlask, PIL, NumPyFrontend GUIPython Tkinter, PILData ProcessingPandas, scikit-learnModel TrainingTransfer Learning, Data Augmentation
## 📊 Dataset
HAM10000 (Human Against Machine with 10000 training sets)

10,015 dermoscopic images
7 different skin lesion categories
Binary classification: Malignant vs Benign
Stratified data splitting for balanced training

🏗️ Architecture

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Tkinter GUI   │    │   Flask API     │    │  TensorFlow     │
│                 │◄──►│                 │◄──►│  MobileNetV2    │
│ • Image Upload  │    │ • Preprocessing │    │  Model          │
│ • Results View  │    │ • Prediction    │    │ • Binary Class  │
│ • Risk Analysis │    │ • JSON Response │    │ • Confidence    │
└─────────────────┘    └─────────────────┘    └─────────────────┘


🚦 Getting Started
Prerequisites
bashPython 3.8+
TensorFlow 2.x
Flask
Tkinter
PIL (Pillow)
NumPy
Pandas
scikit-learn
requests
Installation

Clone the repository

bashgit clone https://github.com/yourusername/skin-cancer-detection.git
cd skin-cancer-detection

Install dependencies

bashpip install -r requirements.txt

Download the trained model
Place your mobilenetv2_checkpoint.h5 file in the project root directory.

Usage
1. Start the Flask API Server
bashpython flask_api.py
Server will start at http://127.0.0.1:5000
2. Launch the GUI Application
bashpython gui_app.py
3. API Usage (Optional)
pythonimport requests
import base64

with open('skin_image.jpg', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()

response = requests.post('http://127.0.0.1:5000/predict', 
                        json={'image': img_data})
result = response.json()
# 📈 Model Performance

Architecture: MobileNetV2 with custom classification head
Input Size: 224×224×3 RGB images
Classes: Binary (Malignant/Benign)
Training: Transfer learning with data augmentation
Optimization: Adam optimizer with learning rate scheduling

# 🖥️ GUI Features
Main Interface

Modern Design: Professional medical application styling
Image Upload: Drag-and-drop or file browser selection
Real-time Preview: Immediate image display with metadata
Analysis Progress: Visual progress indication during processing

Results Display

Primary Prediction: Clear malignant/benign classification
Confidence Score: Percentage confidence with color coding
Risk Assessment: Categorized risk levels (Low/Moderate/High)
Detailed Breakdown: Class probabilities with descriptions
Medical Recommendations: Professional guidance based on results

# 🔧 API Endpoints
Health Check
GET /health
Response: {"status": "healthy", "model_loaded": true}
Prediction
POST /predict
Body: {"image": "base64_encoded_image"}
Response: {
  "success": true,
  "prediction": {
    "predicted_class": "Benign",
    "confidence": 0.85,
    "all_probabilities": [...]
  }
}
# 📁 Project Structure
skin-cancer-detection/
├── train_model.py          # Model training script
├── flask_api.py           # Flask API server
├── gui_app.py            # Tkinter GUI application
├── mobilenetv2_checkpoint.h5  # Trained model weights
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── data/                 # Dataset directory (if included)
🔬 Model Training
The training script (train_model.py) includes:

Data preprocessing and augmentation
MobileNetV2 transfer learning setup
Training with callbacks (checkpointing, early stopping)
Model evaluation and performance metrics

To retrain the model:
bashpython train_model.py
# 🤝 Contributing

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
# 🙏 Acknowledgments

HAM10000 Dataset: Harvard Dataverse for providing the dermoscopic image dataset
MobileNetV2: Google Research for the efficient CNN architecture
Medical Community: For advancing dermatological AI research

# 📞 Contact
Your Name - mazenkhairy48@yahoo.com
Project Link: https://www.kaggle.com/code/mazenkhairymiskovy/skin-cancer-detection-model-using-cnn-86
