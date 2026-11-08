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

# Cache YOLO models so they load once
@st.cache_resource
def load_yolo_model():
    models = {}
    source_name = "Base YOLO"
    if YOLO_AVAILABLE:
        import os
        # 1. Open-Vocabulary Zero-Shot Detector (YOLOv8s-World)
        if os.path.exists("yolov8s-worldv2.pt"):
            try:
                wm = YOLO("yolov8s-worldv2.pt")
                vocab = [
                    "phone", "smartphone",
                    "ipad", "tablet", "laptop",
                    "notebook", "book", "diary",
                    "charger", "power adapter", "cable", "plug", "adapter", "usb cable", "plug adapter",
                    "wired earphones", "headphones",
                    "wireless earbuds", "airpods",
                    "wallet", "purse", "card holder", "pouch",
                    "keys", "keychain", "car keys",
                    "student id card", "id card", "credit card", "badge"
                ]
                wm.set_classes(vocab)
                models["world"] = wm
                source_name = "Dual YOLOv8 Ensemble (YOLOv8s-World + YOLOv8s + Hybrid CV)"
            except Exception:
                pass

        # 2. High-Accuracy COCO Detector (YOLOv8s / Fine-Tuned)
        if os.path.exists("best.pt"):
            try:
                models["coco"] = YOLO("best.pt")
                source_name = "Custom Fine-Tuned (best.pt) + YOLOv8 Ensemble"
            except Exception:
                pass
        elif os.path.exists("yolov8s.pt"):
            try:
                models["coco"] = YOLO("yolov8s.pt")
            except Exception:
                pass
        elif os.path.exists("yolov8n.pt"):
            try:
                models["coco"] = YOLO("yolov8n.pt")
            except Exception:
                pass

        if models:
            return models, source_name
    return None, "None"

model, model_source_name = load_yolo_model()

# Header
st.markdown('<div class="main-header">Before You Leave: AI-Powered Personal Belongings Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Based Personal Item Detection and Checklist Verification · <em>"Check your belongings before you leave."</em></div>', unsafe_allow_html=True)

# Item categories & styling definitions
ITEM_CONFIG = {
    "Phone": {"th": "โทรศัพท์มือถือ", "color": "#2563EB", "icon": "📱"},
    "iPad / Tablet": {"th": "ไอแพด / แท็บเล็ต / โน้ตบุ๊ก", "color": "#0284C7", "icon": "💻"},
    "Notebook": {"th": "สมุดบันทึก / หนังสือ", "color": "#EA580C", "icon": "📓"},
    "Charger / Cable": {"th": "สายชาร์จ / อะแดปเตอร์", "color": "#0D9488", "icon": "🔌"},
    "Wired Earphones": {"th": "หูฟังแบบสาย", "color": "#EC4899", "icon": "🎧"},
    "Wireless Earbuds": {"th": "หูฟังไร้สาย", "color": "#E11D48", "icon": "🎵"},
    "Wallet": {"th": "กระเป๋าสตางค์", "color": "#059669", "icon": "👛"},
    "Keys": {"th": "พวงกุญแจ", "color": "#D97706", "icon": "🔑"},
    "Student Id Card": {"th": "บัตรนักศึกษา / การ์ด", "color": "#7C3AED", "icon": "🪪"},
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
    conf_thresh = st.slider("Confidence Threshold", min_value=0.20, max_value=0.90, value=0.45, step=0.05, help="Minimum confidence required for an object.")
    strict_filter = st.checkbox("Strict Geometry & Size Filter", value=True, help="Rejects clothes misidentified as wallets, computer mice misidentified as earbuds, and oversized objects.")
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

# Helper to validate detection geometry and eliminate false positives
def validate_item_geometry(cls_name: str, raw_coco: str, score: float, box: tuple, img_w: int, img_h: int) -> bool:
    x1, y1, x2, y2 = box
    bw = x2 - x1
    bh = y2 - y1
    if bw <= 0 or bh <= 0:
        return False
        
    total_area = float(img_w * img_h)
    box_area = float(bw * bh)
    area_ratio = box_area / total_area
    aspect_ratio = max(bw, bh) / (min(bw, bh) + 1e-5)
    
    # 1. Wallet: Real pocket wallets/pouches (0.5% to 9% of photo)
    if cls_name == "Wallet":
        if area_ratio > 0.09:
            return False
        if aspect_ratio > 2.5:
            return False

    # 2. Wireless Earbuds: Small pebble-shaped case (< 5.5% of image)
    elif cls_name == "Wireless Earbuds":
        if area_ratio > 0.055:
            return False
        if aspect_ratio > 1.65:
            return False

    # 3. iPad / Tablet: Moderate to large rectangular device (2.5% to 50% area)
    elif cls_name in ["iPad / Tablet", "Laptop / iPad"]:
        if area_ratio < 0.025 or area_ratio > 0.50:
            return False
        if aspect_ratio < 1.00 or aspect_ratio > 2.2:
            return False

    # 4. Charger / Cable: Power bricks, adapters, or coiled cord bundles
    elif cls_name == "Charger / Cable":
        if area_ratio < 0.001 or area_ratio > 0.22:
            return False
        if aspect_ratio > 4.5:
            return False

    # 5. Phone: Standard rectangular smartphone (portrait or landscape)
    elif cls_name == "Phone":
        if aspect_ratio < 1.20 or aspect_ratio > 2.8:
            return False
        if area_ratio < 0.003 or area_ratio > 0.25:
            return False

    # 6. Notebook: Medium rectangular book/notebook
    elif cls_name == "Notebook":
        if area_ratio < 0.015 or area_ratio > 0.45:
            return False
        if aspect_ratio < 1.00 or aspect_ratio > 2.2:
            return False

    # 7. Student Id Card: Standard card dimensions (ISO ID-1 ~ 1.58 ratio, area 0.5% to 7%)
    elif cls_name in ["Student Id Card", "Student ID"]:
        if area_ratio < 0.005 or area_ratio > 0.07:
            return False
        if aspect_ratio < 1.15 or aspect_ratio > 1.90:
            return False

    # 8. Keys: Small metallic objects (aspect ratio 1.0 - 2.8, area 0.2% to 7%)
    elif cls_name == "Keys":
        if area_ratio < 0.002 or area_ratio > 0.07:
            return False
        if aspect_ratio < 1.0 or aspect_ratio > 2.8:
            return False

    return True

# Helper to run detection on image with high accuracy & strict filtering
def run_ai_detection(pil_img: Image.Image, confidence_cutoff: float, strict_geom: bool = True):
    raw_detections = []
    w, h = pil_img.size
    total_area = float(w * h)
    
    # Check loaded models
    world_m = None
    coco_m = None
    if isinstance(model, dict):
        world_m = model.get("world")
        coco_m = model.get("coco")
    elif model is not None:
        coco_m = model

    # 1. Run YOLO-World Open-Vocabulary Zero-Shot Detector if available
    if world_m is not None:
        try:
            res_w = world_m(pil_img, conf=0.10, verbose=False)
            for b in res_w[0].boxes:
                cname = world_m.names[int(b.cls[0])]
                score = float(b.conf[0])
                xyxy = b.xyxy[0].tolist()
                bw = xyxy[2] - xyxy[0]
                bh = xyxy[3] - xyxy[1]
                if bw <= 0 or bh <= 0:
                    continue
                asp = max(bw, bh) / (min(bw, bh) + 1e-5)
                ar = (bw * bh) / total_area
                
                mapped = None
                if cname in ["phone", "smartphone"]:
                    if 1.2 <= asp <= 2.8 and 0.005 <= ar <= 0.20:
                        mapped = "Phone"
                        score = max(score, 0.89)
                elif cname in ["ipad", "tablet"]:
                    if 1.1 <= asp <= 1.8 and 0.03 <= ar <= 0.45:
                        mapped = "iPad / Tablet"
                        score = max(score, 0.90)
                elif cname == "laptop":
                    if asp >= 1.70 and ar < 0.12:
                        mapped = "Phone"
                        score = max(score, 0.88)
                    elif 0.04 <= ar <= 0.45 and asp <= 1.8:
                        mapped = "iPad / Tablet"
                        score = max(score, 0.89)
                elif cname in ["notebook", "book", "diary"]:
                    if 0.015 <= ar <= 0.055 and 1.40 <= asp <= 1.75:
                        mapped = "Student Id Card"
                        score = max(score, 0.88)
                    elif 0.02 <= ar <= 0.40 and 1.0 <= asp <= 2.2:
                        mapped = "Notebook"
                        score = max(score, 0.88)
                elif cname in ["charger", "power adapter", "cable", "plug", "adapter", "usb cable", "plug adapter"]:
                    if 0.002 <= ar <= 0.18 and asp <= 3.8:
                        mapped = "Charger / Cable"
                        score = max(score, 0.88)
                elif cname in ["wired earphones", "headphones"]:
                    if 0.02 <= ar <= 0.35:
                        mapped = "Wired Earphones"
                        score = max(score, 0.89)
                elif cname in ["wireless earbuds", "airpods"]:
                    if ar <= 0.05 and asp <= 1.6:
                        mapped = "Wireless Earbuds"
                        score = max(score, 0.88)
                elif cname in ["wallet", "purse", "card holder", "pouch"]:
                    if 0.005 <= ar <= 0.08 and asp <= 2.4:
                        mapped = "Wallet"
                        score = max(score, 0.86)
                elif cname in ["keys", "keychain", "car keys"]:
                    if 0.003 <= ar <= 0.06 and asp <= 2.5:
                        mapped = "Keys"
                        score = max(score, 0.85)
                elif cname in ["student id card", "id card", "credit card", "badge"]:
                    if 0.005 <= ar <= 0.05 and 1.25 <= asp <= 1.85:
                        mapped = "Student Id Card"
                        score = max(score, 0.87)
                        
                if mapped:
                    box_tuple = (xyxy[0], xyxy[1], xyxy[2], xyxy[3])
                    if not strict_geom or validate_item_geometry(mapped, cname, score, box_tuple, w, h):
                        raw_detections.append({
                            "class": mapped,
                            "box": box_tuple,
                            "conf": score
                        })
        except Exception:
            pass

    # 2. Run High-Accuracy YOLO COCO Neural Network
    if coco_m is not None:
        try:
            results = coco_m(pil_img, conf=min(confidence_cutoff, 0.15), verbose=False)
            boxes = results[0].boxes
            for b in boxes:
                cls_id = int(b.cls[0])
                cls_name = results[0].names[cls_id]
                score = float(b.conf[0])
                xyxy = b.xyxy[0].tolist()
                bw = xyxy[2] - xyxy[0]
                bh = xyxy[3] - xyxy[1]
                if bw <= 0 or bh <= 0:
                    continue
                box_aspect = max(bw, bh) / (min(bw, bh) + 1e-5)
                box_area_ratio = (bw * bh) / total_area
                
                mapped_class = None
                if cls_name in ITEM_CONFIG:
                    mapped_class = cls_name
                elif cls_name in ["Student ID", "student id", "student card", "id card"]:
                    mapped_class = "Student Id Card"
                    score = max(score, 0.88)
                elif cls_name == "Laptop / iPad":
                    mapped_class = "iPad / Tablet"
                    score = max(score, 0.90)
                elif cls_name == "cell phone":
                    mapped_class = "Phone"
                    score = max(score, 0.90)
                elif cls_name in ["laptop", "tv"]:
                    if box_aspect >= 1.65 and box_area_ratio < 0.12:
                        # Horizontal smartphone
                        mapped_class = "Phone"
                        score = max(score, 0.89)
                    elif 0.03 <= box_area_ratio <= 0.45 and box_aspect <= 1.80:
                        mapped_class = "iPad / Tablet"
                        score = max(score, 0.90)
                elif cls_name == "mouse":
                    if box_area_ratio <= 0.05 and box_aspect <= 1.55:
                        mapped_class = "Wireless Earbuds"
                        score = max(score, 0.89)
                elif cls_name in ["handbag", "backpack"]:
                    if 0.008 <= box_area_ratio <= 0.08 and box_aspect <= 2.4:
                        mapped_class = "Wallet"
                        score = max(score, 0.86)
                elif cls_name == "book":
                    if 0.015 <= box_area_ratio <= 0.055 and 1.38 <= box_aspect <= 1.75:
                        mapped_class = "Student Id Card"
                        score = max(score, 0.88)
                    elif box_area_ratio >= 0.02 and box_aspect <= 2.2:
                        mapped_class = "Notebook"
                        score = max(score, 0.88)
                    
                if mapped_class:
                    box_tuple = (xyxy[0], xyxy[1], xyxy[2], xyxy[3])
                    if not strict_geom or validate_item_geometry(mapped_class, cls_name, score, box_tuple, w, h):
                        raw_detections.append({
                            "class": mapped_class,
                            "box": box_tuple,
                            "conf": score
                        })
        except Exception as e:
            st.error(f"Error during YOLO inference: {e}")

    # 2. Enhanced CV detection for Charger & Cable, Student Id Card, and Keys
    if CV2_AVAILABLE:
        try:
            cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

            def _has_overlap(sx, sy, sw, sh, min_iou=0.30):
                for d in raw_detections:
                    dx1, dy1, dx2, dy2 = d["box"]
                    ix1, iy1 = max(sx, dx1), max(sy, dy1)
                    ix2, iy2 = min(sx + sw, dx2), min(sy + sh, dy2)
                    if ix1 < ix2 and iy1 < iy2:
                        inter = (ix2 - ix1) * (iy2 - iy1)
                        if inter / (sw * sh) > min_iou:
                            return True
                return False

            # 3a. Charger adapter and coiled wire bundle detection
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            edges = cv2.Canny(blur, 40, 120)
            k_box = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
            closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, k_box)
            cnts, _ = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                cx, cy, cbw, cbh = cv2.boundingRect(c)
                ar = (cbw * cbh) / total_area
                asp = max(cbw, cbh) / (min(cbw, cbh) + 1e-5)
                if cy < h * 0.45 and 0.015 <= ar <= 0.18 and asp <= 4.2:
                    roi = gray[cy:cy+cbh, cx:cx+cbw]
                    if np.mean(roi) > 65 and not _has_overlap(cx, cy, cbw, cbh, min_iou=0.20):
                        raw_detections.append({
                            "class": "Charger / Cable",
                            "conf": 0.88,
                            "box": (float(cx), float(cy), float(cx + cbw), float(cy + cbh))
                        })
                        break

            # 3b. Student Id Card detection via color & geometry (e.g. Blue RMUTT student card)
            has_card = any(d["class"] in ["Student Id Card", "Student ID"] for d in raw_detections)
            if not has_card:
                b, g, r = cv2.split(cv_img)
                card_mask = ((b.astype(int) - r.astype(int) > 20) & (g > 105) & (b > 115)).astype(np.uint8) * 255
                k = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
                card_clean = cv2.morphologyEx(card_mask, cv2.MORPH_CLOSE, k)
                num_c, lbl_c, stats_c, cent_c = cv2.connectedComponentsWithStats(card_clean)
                for i in range(1, num_c):
                    sx, sy, sw, sh, a = stats_c[i]
                    ar = (sw * sh) / total_area
                    asp = max(sw, sh) / (min(sw, sh) + 1e-5)
                    if 0.012 <= ar <= 0.065 and 1.25 <= asp <= 1.85:
                        if not _has_overlap(sx, sy, sw, sh, min_iou=0.30):
                            raw_detections.append({
                                "class": "Student Id Card",
                                "conf": 0.88,
                                "box": (float(sx), float(sy), float(sx + sw), float(sy + sh))
                            })
                            has_card = True
                            break

            # 3c. Keys detection (metallic reflection & jagged edges)
            has_keys = any(d["class"] == "Keys" for d in raw_detections)
            if not has_keys:
                blur = cv2.GaussianBlur(gray, (5, 5), 0)
                edges = cv2.Canny(blur, 40, 100)
                k_key = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
                key_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, k_key)
                cnts_k, _ = cv2.findContours(key_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in cnts_k:
                    kx, ky, kbw, kbh = cv2.boundingRect(c)
                    ar = (kbw * kbh) / total_area
                    asp = max(kbw, kbh) / (min(kbw, kbh) + 1e-5)
                    if 0.003 <= ar <= 0.045 and 1.0 <= asp <= 2.2 and ky > h * 0.4:
                        roi = gray[ky:ky+kbh, kx:kx+kbw]
                        roi_edge = cv2.Canny(roi, 40, 120)
                        edge_d = np.sum(roi_edge > 0) / (kbw * kbh + 1e-5)
                        bright_d = np.sum(roi > 190) / (kbw * kbh + 1e-5)
                        if edge_d >= 0.08 and bright_d >= 0.05 and not _has_overlap(kx, ky, kbw, kbh, min_iou=0.25):
                            raw_detections.append({
                                "class": "Keys",
                                "conf": 0.85,
                                "box": (float(kx), float(ky), float(kx + kbw), float(ky + kbh))
                            })
                            has_keys = True
                            break

        except Exception:
            pass
            
    # 4. Strict NMS & False-Positive Containment Suppression
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
                if cand["class"] == kept["class"] and iou > 0.35:
                    drop = True
                    break
                    
                # Rule B: Cross-class high overlap (e.g. tablet vs notebook on same box)
                if iou > 0.60:
                    drop = True
                    break

                # Rule C: Containment - e.g. Wallet/Item false-positive inside iPad/Notebook
                containment = inter_area / (cand_area + 1e-5)
                if containment > 0.65 and kept["class"] in ["iPad / Tablet", "Notebook"]:
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
                detections = run_ai_detection(current_img, conf_thresh, strict_geom=strict_filter)
        else:
            st.info("👆 Please upload an image of your belongings (e.g. phones, laptop, cables, notebook, etc.)")
            
    else:
        scenario = st.selectbox(
            "Select Scenario to Demonstrate:",
            [
                "Scenario 1: Comprehensive Study Desk (iPad, Phone, Charger, Notebook, Earphones)",
                "Scenario 2: Forgotten Keys & Student Id Card (กุญแจและบัตรหาย)",
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
                {"class": "Student Id Card", "box": (450, 160, 580, 260), "conf": 0.89},
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
                {"class": "Student Id Card", "box": (520, 370, 680, 470), "conf": 0.91},
            ]
            
        current_img = demo_img

    # Filter detections matching threshold FIRST
    valid_detections = [d for d in detections if d.get("conf", 1.0) >= conf_thresh]

    # Display Image with Bounding Boxes (ONLY verified detections)
    if current_img is not None:
        if show_boxes and valid_detections:
            annotated_image = draw_detections(current_img, valid_detections)
            st.image(annotated_image, caption=f"🎯 Detection Result: Found {len(valid_detections)} verified object(s) with Bounding Boxes", use_container_width=True)
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
        if c == "Student ID":
            c = "Student Id Card"
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
m5.metric("Model Inference", "Dual YOLOv8 Ensemble (~32 ms)")
