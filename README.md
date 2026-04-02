
---
title: HealthLens • Atlas Workspace
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.5.0
app_file: app.py
pinned: false
license: apache-2.0
---

# 🔳 HealthLens • Atlas AI Workspace

**HealthLens AI** is a production-style, multimodal AI health screening platform designed for the **Hugging Face Spaces** free tier. It features a professional **CodeAtlas Workspace** UI, integrated rules-based triage, and the **MedGemma** multimodal reasoning layer.

---

### **📊 System Architecture Flow**

```mermaid
graph TD
    A[User Workspace: Dashboard] --> B{Input Data}
    B -- Symptom Text --> C[Rules-Based Triage Engine]
    B -- Optical Dataset --> D[OpenCV Pre-processor]
    
    D -- Pass (Quality Check) --> E[Multimodal Inference Core]
    D -- Fail (Blur/Low-Light) --> F[System Error Console]
    
    C -- Red Flag Trigger --> G[Safety Alert Logic]
    E -- AI Reasoning Result --> H[Integrated Report Builder]
    G -- Safety Override --> H
    
    H -- Action Pipeline --> I[Analysis Logs (MongoDB)]
    H -- Action Pipeline --> J[Global Email (Gmail SMTP)]
    H -- Action Pipeline --> K[Atlas Workspace Console]
```

---

### **🛠️ Production Tech Stack**

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Workspace UI** | **Gradio (Blocks API)** | Next-gen dashboard with state-aware sidebar navigation. |
| **Design System** | **Emerald/Atlas CSS** | Pitch-black (#000000) nocturne theme with glassmorphism. |
| **Vision Core** | **OpenCV (Headless)** | Automated lighting and blur validation on medical images. |
| **AI Reasoning** | **Hugging Face API** | Multimodal analysis using `blip-image-captioning-base`. |
| **Persistence** | **MongoDB (Atlas)** | Integrated historical logs and screening archiving. |
| **Global Delivery**| **Gmail SMTP Relay** | Domain-free global email delivery for medical reports. |

---

### **🚀 Getting Started**

#### **1. Environment Configuration**
Configure your **`.env`** file with your credentials:
```bash
GMAIL_USER=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_16_digit_app_password
MONGODB_URI=your_mondodb_connection_string
HF_TOKEN=your_huggingface_read_token
```

#### **2. Local Development Launch**
Install the minimal requirements and launch the Atlas Node:
```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

---

### **📁 Unified Workspace Features**
- **Dashboard**: Professional side-by-side Clinical Intake and Optical Reasoning config.
- **Analysis Console**: Dedicated workspace for real-time reporting and export.
- **Safety Queue**: Integrated rules-based engine for high-priority red-flag detection (Chest pain, etc.).
- **Global Reports**: Markdown-to-HTML transformation delivered via secure SMTP.

---

### **🛡️ Clinical Disclaimer**
**HealthLens AI** is for **educational and screening use only**. It is **NOT** a certified medical diagnosis tool. In case of emergency, users are instructed to contact local emergency services immediately (911/112). 
