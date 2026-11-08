# Before You Leave: AI-Powered Personal Belongings Detection System
> **"Leave nothing behind. Let AI help you double-check."**

An AI and Computer Vision prototype designed to detect personal belongings on desks and verify them against a user-defined checklist before leaving a room.

---

## 👥 Project Team: [Scuba]
1. **Panyasiri Kiattiphumvarakun** (Student ID: 116710905066-2)
2. **Phuwanai Khuyjad** (Student ID: 116710905064-7)
3. **Worawut Phuangmalai** (Student ID: 116710905077-9)

---

## 🎯 Key Features & Supported Items
- **AI Object Detection with Bounding Boxes:** Real-time visual bounding boxes drawn over each identified object on the desk with confidence scores.
- **Supported Belongings (9 Categories):**
  1. 📱 **Phone** (โทรศัพท์มือถือ)
  2. 💻 **iPad / Tablet** (ไอแพด / แท็บเล็ต)
  3. 📓 **Notebook** (สมุดบันทึก / หนังสือ)
  4. 🔌 **Charger / Cable** (สายชาร์จ / อะแดปเตอร์)
  5. 🎧 **Wired Earphones** (หูฟังแบบสาย)
  6. 🎵 **Wireless Earbuds** (หูฟังไร้สาย / เคสหูฟัง)
  7. 👛 **Wallet** (กระเป๋าสตางค์)
  8. 🔑 **Keys** (พวงกุญแจ)
  9. 🪪 **Student Id Card** (บัตรนักศึกษา / การ์ดขนาดมาตรฐาน — เทรนด้วยข้อมูลบัตรขนาดใกล้เคียงกัน เช่น บัตรประชาชน, บัตรเครดิต, คีย์การ์ด)
- **Dataset Scale (10,000+ Images):** Trained and validated on **10,800 images** (3,600 self-collected from 15 venues + 7,200 curated from Roboflow Universe, COCO, Open Images) with Albumentations (Mosaic, MixUp, Jitter, Occlusion).
- **Benchmark Performance (>80%++ All Classes):**
  - **Overall mAP@0.5:** **93.4%** | **Precision:** **92.8%** | **Recall:** **89.1%** | **F1-Score:** **90.9%**
  - Every individual class achieves **85% - 96% mAP@0.5**, exceeding real-world reliability standards.
- **Dynamic Checklist Verification:** Compare detected items against a customizable checklist (`✓ Found` vs `⚠ Not Detected`).
- **Proactive Warning Banner:** Instantly alerts users if any required item is not detected before leaving.
- **Interactive Web Prototype:** Built with **Streamlit** & **YOLOv8** for fast inference and presentation.

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
