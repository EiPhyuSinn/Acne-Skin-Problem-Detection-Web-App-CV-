# 🧴 Acne & Skin Problem Detection Web App

This is a computer vision project that allows users to upload an image of a face and automatically detects various skin problems — such as acne, blackheads, whiteheads, cysts, and more — using a custom-trained YOLOv8 model.

The app is served using **FastAPI** and includes a simple, interactive front-end built with **HTML**, **CSS**, and **JavaScript**.

---

## 📸 Features

- 🔍 Detects 12 different types of skin conditions (e.g., blackheads, pustules, cysts)
- 🧠 Trained on custom Roboflow datasets using YOLOv8 for high accuracy
- 📊 Model achieves **0.80 mAP** after 100 epochs of training
- 🌐 Clean and responsive web UI for image upload and visualization
- 🧴 Recommends skincare products based on detected issues
- 💡 Fast inference with real-time annotated results

---

https://github.com/user-attachments/assets/be60fdab-a974-4cb4-bb5b-2cbbda0e9259

## 🖼️ Skin Conditions Detected

- Hidden acne  
- Cysts  
- Blackhead  
- Whitehead  
- Pustules  
- Nodular acne  
- Acne  
- Birthmark  
- Milium  
- Papular  
- Purulent  
- Scars  

---

## 🛠 Tech Stack

| Frontend  | Backend | Model        | Tools          |
|-----------|---------|--------------|----------------|
| HTML, CSS, JS | FastAPI | YOLOv8 (Ultralytics) | Roboflow, OpenCV, NumPy |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/acne-skin-detection.git
cd acne-skin-detection
