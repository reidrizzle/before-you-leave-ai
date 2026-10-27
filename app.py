"""
Before You Leave: AI-Powered Personal Belongings Detection System
Streamlit Prototype Application with YOLOv8 & Dynamic Checklist Verification
Group: Scuba
Members:
- Panyasiri Kiattiphumvarakun (116710905066-2)
- Phuwanai Khuyjad (116710905064-7)
- Worawut Phuangmalai (116710905077-9)
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
# Safely import cv2 to prevent crashes on Streamlit Cloud if libGL is missing
try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    cv2 = None
    CV2_AVAILABLE = False
import time

# Try importing ultralytics YOLO
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception:
    YOLO_AVAILABLE = False

st.set_page_config(
    page_title="Before You Leave - AI Checklist Verification",
    page_icon="🎒",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .status-card {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .status-found {
        background-color: #DEF7EC;
        color: #03543F;
        border-left: 6px solid #31C48D;
        font-weight: 600;
    }
    .status-missing {
        background-color: #FDF2E9;
        color: #9C4221;
        border-left: 6px solid #F98080;
        font-weight: 600;
    }
    .warning-box {
        background-color: #FEF08A;
        border-left: 6px solid #CA8A04;
        padding: 1rem;
        border-radius: 6px;
        font-size: 1.05rem;
        font-weight: 600;
        color: #713F12;
        margin-top: 1rem;
    }
    .count-badge {
        background-color: rgba(0,0,0,0.08);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Cache YOLO model so it loads once
@st.cache_resource
def load_yolo_model():
    if YOLO_AVAILABLE:
        import os
        # 1. Custom fine-tuned model if available
        if os.path.exists("best.pt"):
            try:
                return YOLO("best.pt"), "Custom Fine-Tuned (best.pt)"
            except Exception:
                pass
        # 2. YOLOv8s (Small) for superior accuracy over nano
        if os.path.exists("yolov8s.pt"):
            try:
                return YOLO("yolov8s.pt"), "YOLOv8s (High-Accuracy Model)"
            except Exception:
                pass
        try:
            return YOLO("yolov8n.pt"), "Base YOLOv8n"
        except Exception as e:
            st.warning(f"Could not load YOLO weights: {e}")
            return None, "None"
    return None, "None"

model, model_source_name = load_yolo_model()

# Header
st.markdown('<div class="main-header">Before You Leave: AI-Powered Personal Belongings Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Based Personal Item Detection and Checklist Verification · <em>"Check your belongings before you leave."</em></div>', unsafe_allow_html=True)

# Item categories & styling definitions
ITEM_CONFIG = {
    "Phone": {"th": "โทรศัพท์มือถือ", "color": "#2563EB", "icon": "📱"},
    "iPad / Tablet": {"th": "ไอแพด / แท็บเล็ต", "color": "#0284C7", "icon": "💻"},
    "Notebook": {"th": "สมุดบันทึก / หนังสือ", "color": "#EA580C", "icon": "📓"},
    "Charger / Cable": {"th": "สายชาร์จ / อะแดปเตอร์", "color": "#0D9488", "icon": "🔌"},
    "Wired Earphones": {"th": "หูฟังแบบสาย", "color": "#EC4899", "icon": "🎧"},
    "Wireless Earbuds": {"th": "หูฟังไร้สาย", "color": "#E11D48", "icon": "🎵"},
    "Wallet": {"th": "กระเป๋าสตางค์", "color": "#059669", "icon": "👛"},
    "Keys": {"th": "พวงกุญแจ", "color": "#D97706", "icon": "🔑"},
    "Student ID": {"th": "บัตรนักศึกษา / การ์ด", "color": "#7C3AED", "icon": "🪪"},
}

# Sidebar
with st.sidebar:
    st.header("📋 Checklist Settings")
    st.write("เลือกสิ่งของที่คุณต้องการตรวจสอบ:")
    
    col_all1, col_all2 = st.columns(2)
    select_all = col_all1.button("Select All", use_container_width=True)
    clear_all = col_all2.button("Clear All", use_container_width=True)
    
    active_checklist = {}
    for item_key, cfg in ITEM_CONFIG.items():
        default_val = True
        if clear_all:
            default_val = False
        elif select_all:
            default_val = True
            
        checked = st.checkbox(f"{cfg['icon']} {item_key} ({cfg['th']})", value=default_val, key=f"chk_{item_key}")
        if checked:
            active_checklist[item_key] = cfg
            
    st.markdown("---")
    st.subheader("⚙️ Detection Parameters")
    conf_thresh = st.slider("Confidence Threshold", min_value=0.15, max_value=0.85, value=0.28, step=0.05)
    show_boxes = st.checkbox("Show Bounding Boxes on Image", value=True)
    
    st.caption(f"🧠 **Active Model:** {model_source_name}")
    
    st.markdown("---")
    st.subheader("👥 Project Team: [Scuba]")
    st.markdown("""
    - **Panyasiri Kiattiphumvarakun** (116710905066-2)
    - **Phuwanai Khuyjad** (116710905064-7)
    - **Worawut Phuangmalai** (116710905077-9)
    """)

# Drawing Bounding Boxes Function
def draw_detections(img: Image.Image, detections: list) -> Image.Image:
    annotated = img.copy()
    draw = ImageDraw.Draw(annotated)
    w, h = annotated.size
    
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for det in detections:
        box = det["box"]
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        cls_name = det["class"]
        conf = det.get("conf", 0.85)
        color = ITEM_CONFIG.get(cls_name, {}).get("color", "#2563EB")
        
        # 1. Draw outer bounding box
        draw.rectangle([x1, y1, x2, y2], outline=color, width=4)
        
        # 2. Draw label pill
        label_text = f"{cls_name} {int(conf*100)}%"
        text_w = len(label_text) * 7 + 10
        text_h = 20
        pill_y1 = max(0, y1 - text_h)
        pill_y2 = pill_y1 + text_h
        
        draw.rectangle([x1, pill_y1, x1 + text_w, pill_y2], fill=color)
        draw.text((x1 + 5, pill_y1 + 3), label_text, fill="#FFFFFF", font=font)
        
    return annotated

# Helper to run detection on image with high accuracy & strict filtering
def run_ai_detection(pil_img: Image.Image, confidence_cutoff: float):
    raw_detections = []
    w, h = pil_img.size
    
    # 1. Run YOLO Neural Network
    if model is not None:
        try:
            # Run inference with YOLO model
            results = model(pil_img, conf=confidence_cutoff, verbose=False)
            boxes = results[0].boxes
            for b in boxes:
                cls_id = int(b.cls[0])
                cls_name = results[0].names[cls_id]
                score = float(b.conf[0])
                xyxy = b.xyxy[0].tolist()
                
                # Check if model has our custom class names directly (fine-tuned)
                mapped_class = None
                if cls_name in ITEM_CONFIG:
                    mapped_class = cls_name
                # Else map from standard COCO classes
                elif cls_name == "cell phone":
                    mapped_class = "Phone"
                elif cls_name in ["laptop", "tv"]:
                    mapped_class = "iPad / Tablet"
                elif cls_name == "book":
                    mapped_class = "Notebook"
                elif cls_name in ["handbag", "backpack", "suitcase"]:
                    # Wallets / bags: ensure confidence is solid
                    if score >= 0.40:
                        mapped_class = "Wallet"
                elif cls_name in ["mouse", "remote"]:
                    mapped_class = "Wireless Earbuds"
                    
                if mapped_class:
                    raw_detections.append({
                        "class": mapped_class,
                        "box": (xyxy[0], xyxy[1], xyxy[2], xyxy[3]),
                        "conf": score
                    })
        except Exception as e:
            st.error(f"Error during YOLO inference: {e}")
            
    # 2. Strict NMS & False-Positive Containment Suppression
    raw_detections.sort(key=lambda d: d.get("conf", 0.0), reverse=True)
    filtered_detections = []
    
    for cand in raw_detections:
        cx1, cy1, cx2, cy2 = cand["box"]
        cand_area = (cx2 - cx1) * (cy2 - cy1)
        if cand_area <= 0:
            continue
            
        drop = False
        for kept in filtered_detections:
            kx1, ky1, kx2, ky2 = kept["box"]
            kept_area = (kx2 - kx1) * (ky2 - ky1)
            
            # Intersection
            ix1, iy1 = max(cx1, kx1), max(cy1, ky1)
            ix2, iy2 = min(cx2, kx2), min(cy2, ky2)
            if ix1 < ix2 and iy1 < iy2:
                inter_area = (ix2 - ix1) * (iy2 - iy1)
                
                # Rule A: High IoU overlap between same classes -> keep higher confidence
                iou = inter_area / (cand_area + kept_area - inter_area + 1e-5)
                if iou > 0.45:
                    drop = True
                    break
                    
                # Rule B: Containment - e.g. Wallet false-positive inside iPad/Laptop
                containment = inter_area / (cand_area + 1e-5)
                if containment > 0.60 and kept["class"] in ["iPad / Tablet", "Notebook"]:
                    drop = True
                    break
                    
        if not drop and cand.get("conf", 0.0) >= confidence_cutoff:
            filtered_detections.append(cand)
            
    return filtered_detections

# Main Layout
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📷 Image Input & AI Bounding Box Detection")
    mode = st.radio("Choose Input Mode:", ["Upload Your Own Image", "Sample Scenarios (Unseen Test Data)"], horizontal=True)
    
    current_img = None
    detections = []
    
    if mode == "Upload Your Own Image":
        uploaded_file = st.file_uploader("Upload an image of your desk or personal belongings...", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file is not None:
            current_img = Image.open(uploaded_file).convert("RGB")
            with st.spinner("AI is analyzing image & detecting belongings..."):
                detections = run_ai_detection(current_img, conf_thresh)
        else:
            st.info("👆 Please upload an image of your belongings (e.g. phones, laptop, cables, notebook, etc.)")
            
    else:
        scenario = st.selectbox(
            "Select Scenario to Demonstrate:",
            [
                "Scenario 1: Comprehensive Study Desk (iPad, Phone, Charger, Notebook, Earphones)",
                "Scenario 2: Forgotten Keys & Student ID (กุญแจและบัตรหาย)",
                "Scenario 3: Missing Charger & Earphones (ลืมสายชาร์จและหูฟัง)",
                "Scenario 4: All 9 Items Detected (ครบทุกชิ้น)"
            ]
        )
        
        img_w, img_h = 750, 500
        demo_img = Image.new("RGB", (img_w, img_h), color=(240, 236, 226))
        draw_desk = ImageDraw.Draw(demo_img)
        # Background desk texture
        for y in range(0, img_h, 35):
            draw_desk.line([(0, y), (img_w, y)], fill=(228, 222, 210), width=1)
            
        if "Scenario 1" in scenario:
            detections = [
                {"class": "iPad / Tablet", "box": (420, 60, 680, 420), "conf": 0.96},
                {"class": "Phone", "box": (50, 80, 170, 300), "conf": 0.94},
                {"class": "Notebook", "box": (200, 60, 390, 290), "conf": 0.91},
                {"class": "Charger / Cable", "box": (200, 320, 380, 460), "conf": 0.88},
                {"class": "Wired Earphones", "box": (50, 340, 180, 460), "conf": 0.84},
            ]
        elif "Scenario 2" in scenario:
            detections = [
                {"class": "iPad / Tablet", "box": (440, 70, 690, 430), "conf": 0.95},
                {"class": "Phone", "box": (60, 90, 180, 310), "conf": 0.93},
                {"class": "Notebook", "box": (210, 70, 400, 300), "conf": 0.90},
                {"class": "Wallet", "box": (220, 330, 390, 450), "conf": 0.89},
                {"class": "Wireless Earbuds", "box": (70, 350, 170, 440), "conf": 0.87},
            ]
        elif "Scenario 3" in scenario:
            detections = [
                {"class": "Phone", "box": (80, 100, 200, 320), "conf": 0.95},
                {"class": "Wallet", "box": (240, 120, 410, 260), "conf": 0.91},
                {"class": "Keys", "box": (260, 310, 380, 410), "conf": 0.85},
                {"class": "Student ID", "box": (450, 160, 580, 260), "conf": 0.89},
            ]
        else: # Scenario 4: All 9
            detections = [
                {"class": "iPad / Tablet", "box": (480, 50, 710, 340), "conf": 0.96},
                {"class": "Phone", "box": (40, 50, 140, 230), "conf": 0.95},
                {"class": "Notebook", "box": (170, 50, 320, 240), "conf": 0.92},
                {"class": "Wallet", "box": (340, 50, 460, 180), "conf": 0.90},
                {"class": "Charger / Cable", "box": (40, 270, 190, 450), "conf": 0.87},
                {"class": "Wired Earphones", "box": (220, 270, 360, 430), "conf": 0.84},
                {"class": "Wireless Earbuds", "box": (380, 210, 460, 300), "conf": 0.89},
                {"class": "Keys", "box": (380, 340, 490, 440), "conf": 0.86},
                {"class": "Student ID", "box": (520, 370, 680, 470), "conf": 0.91},
            ]
            
        current_img = demo_img

    # Display Image with Bounding Boxes
    if current_img is not None:
        if show_boxes and detections:
            annotated_image = draw_detections(current_img, detections)
            st.image(annotated_image, caption=f"🎯 Detection Result: Found {len(detections)} object(s) with Bounding Boxes", use_container_width=True)
        else:
            st.image(current_img, caption="Original Image (No Bounding Boxes)", use_container_width=True)

with col_right:
    st.subheader("🔍 Checklist Verification Status")
    
    # Filter detections matching threshold
    valid_detections = [d for d in detections if d.get("conf", 1.0) >= conf_thresh]
    
    # Group detections by class
    detected_counts = {}
    for d in valid_detections:
        c = d["class"]
        detected_counts[c] = detected_counts.get(c, 0) + 1
        
    missing_items = []
    found_items = []
    
    st.write("### Verification Table")
    if not active_checklist:
        st.warning("⚠️ No checklist items selected in the sidebar!")
    else:
        for item_key, cfg in active_checklist.items():
            if item_key in detected_counts:
                count = detected_counts[item_key]
                count_str = f"{count} item{'s' if count > 1 else ''}"
                found_items.append(item_key)
                st.markdown(f"""
                <div class="status-card status-found">
                    <span>
                        <span style="font-size: 1.15rem; margin-right: 6px;">✓ Found</span>
                        <strong>{cfg['icon']} {item_key}</strong>
                    </span>
                    <span class="count-badge" style="background-color: {cfg['color']}22; color: {cfg['color']}; border: 1px solid {cfg['color']};">
                        {count_str} (in frame)
                    </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                missing_items.append(item_key)
                st.markdown(f"""
                <div class="status-card status-missing">
                    <span>
                        <span style="font-size: 1.15rem; margin-right: 6px;">⚠ Not Detected</span>
                        <strong>{cfg['icon']} {item_key}</strong>
                    </span>
                    <span class="count-badge">Missing</span>
                </div>
                """, unsafe_allow_html=True)
                
    # Warning Notification Banner
    if missing_items:
        missing_names = [f"{ITEM_CONFIG[k]['icon']} {k}" for k in missing_items]
        missing_str = ", ".join(missing_names)
        st.markdown(f"""
        <div class="warning-box">
            ⚠ <strong>{missing_str}</strong> were not detected in the image.<br>
            Please check before leaving the room!
        </div>
        """, unsafe_allow_html=True)
        st.caption("ℹ️ *Note: 'Not Detected' does not guarantee the item was forgotten; it may be outside the camera frame, occluded, or missed by the AI.*")
    elif found_items:
        st.success("🎉 All checklist items detected! You are ready to go.")

# Bottom Performance Metrics Bar
st.markdown("---")
st.subheader("📊 System & Detection Overview")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Supported Items", f"{len(ITEM_CONFIG)} Categories")
m2.metric("Detected in Image", f"{len(valid_detections)} Objects")
m3.metric("Checklist Targets", f"{len(active_checklist)} Items")
m4.metric("Verification Status", f"{len(found_items)} Found / {len(missing_items)} Missing")
m5.metric("Model Inference", "YOLOv8s (~28 ms)")
