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
  9. 🪪 **Student ID** (บัตรนักศึกษา / คีย์การ์ด)
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
