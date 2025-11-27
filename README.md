# 🥔 PotatoDoc AI - Potato Disease Classification System

> An end-to-end AI-powered solution for detecting potato leaf diseases using Deep Learning and Computer Vision

[![Live Demo](https://img.shields.io/badge/Demo-Live-success)](your-vercel-url-here)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.5.0-orange.svg)](https://www.tensorflow.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Platform-4285F4)](https://cloud.google.com/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)


---

## 🌟 Overview

**PotatoDoc AI** is an intelligent crop disease detection system that helps farmers and agricultural professionals identify potato leaf diseases quickly and accurately. Using state-of-the-art Convolutional Neural Networks (CNN), the system can detect **Early Blight**, **Late Blight**, and **Healthy** potato leaves with over **99% accuracy**.

### 🎯 Problem Statement

Potato diseases are a major threat to global food security, causing significant crop losses every year. Early and accurate detection is crucial for:
- Preventing disease spread
- Reducing pesticide overuse
- Increasing crop yield
- Saving farmers' time and resources

Traditional methods require expert knowledge and are time-consuming. This AI solution democratizes disease detection, making it accessible to everyone.

---

## ✨ Key Features

- 🔍 **Real-time Disease Detection** - Get instant results in seconds
- 🎯 **High Accuracy** - 99%+ classification accuracy
- 📱 **Mobile Responsive** - Works on any device
- 🖼️ **Drag & Drop Upload** - Easy-to-use interface
- ☁️ **Cloud Deployed** - Scalable and always available
- 🌐 **API Access** - RESTful API for integration
- 📊 **Confidence Scoring** - Transparent prediction confidence

---

## 🚀 Live Demo

**🌐 Web Application:** [PotatoDoc AI](https://potatodoc-ai.vercel.app/)

Try uploading a potato leaf image and see the magic! ✨

---

## 🛠️ Tech Stack

### Machine Learning
- **TensorFlow 2.5.0** - Deep learning framework
- **Keras** - High-level neural networks API
- **CNN (Convolutional Neural Network)** - Image classification architecture
- **Python 3.9+** - Programming language

### Backend
- **Google Cloud Functions** - Serverless deployment (h5 model)
- **FastAPI** - Local API development (saved_model format)
- **Google Cloud Storage** - Model storage

### Frontend
- **HTML / CSS** - Structure and styling
- **JavaScript** - Interactive functionality
- **Vercel** - Frontend hosting

### Tools & Libraries
- **NumPy** - Numerical computing
- **Pillow (PIL)** - Image processing
- **Google Cloud SDK** - Deployment tools

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 99%+ |
| **Classes** | 3 (Early Blight, Late Blight, Healthy) |
| **Input Size** | 256 x 256 (RGB) |
| **Model Type** | Convolutional Neural Network |
| **Framework** | TensorFlow/Keras |

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   GCP API    │─────▶│  CNN Model  │
│  (Vercel)   │      │  (Serverless)│      │   (.h5)     │
└─────────────┘      └──────────────┘      └─────────────┘
      │                     │                      │
      │                     │                      │
   Upload                  API                 Predict
   Image              Request/Response        Disease Class
                                              + Confidence
                                              
                    Local Development
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   FastAPI    │─────▶│  CNN Model  │
│   (Local)   │      │ (localhost)  │      │(saved_model)│
└─────────────┘      └──────────────┘      └─────────────┘
```

---


## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Cloud account (for deployment)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/arunkumareswari/potato-disease-classification-ai.git
   cd potato-disease-classification-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r api/requirements.txt
   ```

3. **Run local API (FastAPI with saved_model)**
   ```bash
   cd api
   python main.py
   # API runs on http://localhost:8000
   ```

4. **Open frontend**
   ```bash
   cd frontend
   # Open index.html in browser or use live server
   ```

---

## 🌐 Deployment

### Frontend (Vercel)

1. Push `frontend` folder to GitHub
2. Connect repository to Vercel
3. Deploy with one click
4. Update API endpoint in `script.js` to point to GCP

### Backend (Google Cloud Functions)

```bash
cd gcp

gcloud functions deploy predict \
  --gen2 \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --memory 1GB \
  --timeout 300s \
  --region us-central1 \
  --project your-project-id \
  --entry-point predict
```

---

## 📡 API Usage

### Production Endpoint (GCP)
```
POST https://us-central1-nice-azimuth-477813-r1.cloudfunctions.net/predict
```

### Local Development Endpoint
```
POST http://localhost:8000/predict
```

### Response
```json
{
  "success": true,
  "class": "Late Blight",
  "confidence": 99.98,
}
```

---

## 🎓 How It Works

### Model Format Differences

The project uses **two model formats** for different purposes:

#### 1. **Local Development** (saved_model format)
- **Location**: `saved_model/1/`
- **Format**: TensorFlow SavedModel (`.pb` file)
- **Used in**: FastAPI local server (`api/main.py`)
- **Advantage**: Quick to load and ideal for fast local testing

#### 2. **Production Deployment** (h5 format)
- **Location**: `potatoes.h5` (uploaded to GCS)
- **Format**: Keras H5 format
- **Used in**: Google Cloud Functions (`gcp/main.py`)
- **Advantage**: Smaller file size, easier to deploy

### Prediction Pipeline

1. **Image Upload**: User uploads a potato leaf image via web interface
2. **Preprocessing**: Image is resized to 256x256 and converted to RGB
3. **API Request**: Image sent to backend (local FastAPI or GCP Function)
4. **Model Prediction**: CNN model analyzes the image
5. **Classification**: Model predicts one of three classes:
   - Early Blight
   - Late Blight
   - Healthy
6. **Result Display**: Shows disease class with confidence score

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">
  
### 🥔 Made with ❤️ for farmers and agricultural innovation

</div>