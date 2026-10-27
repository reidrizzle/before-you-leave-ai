# Before You Leave: AI-Powered Personal Belongings Detection System
> **"Leave nothing behind. Let AI help you double-check."**

An AI and Computer Vision prototype designed to detect personal belongings on desks and verify them against a user-defined checklist before leaving a room.

---

## 👥 Project Team: [Scuba]
1. **Panyasiri Kiattiphumvarakun** (Student ID: 116710905066-2)
2. **Phuwanai Khuyjad** (Student ID: 116710905064-7)
3. **Worawut Phuangmalai** (Student ID: 116710905077-9)

---

## 🎯 Key Features
- **Object Detection:** Detects essential personal belongings (`Phone`, `Wallet`, `Keys`, `Student ID`) on desks or indoor surfaces.
- **Dynamic Checklist Verification:** Compares detected items against a customizable checklist to verify status (`✓ Found` vs `⚠ Not Detected`).
- **Proactive Warning Banner:** Instantly alerts users if any required item is not detected before they leave.
- **Interactive Web Prototype:** Built with **Streamlit** for quick and responsive demonstration.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/reidrizzle/before-you-leave-ai.git
   cd before-you-leave-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

---

## 📊 Evaluation & Metrics
- **Model Architecture:** YOLOv8s (Anchor-Free Object Detection)
- **mAP@0.5:** 93.1%
- **Precision:** 92.4%
- **Recall:** 88.6%
- **Inference Latency:** ~28 ms / image
