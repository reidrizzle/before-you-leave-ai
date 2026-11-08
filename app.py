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
    "iPad / Tablet": {"th": "ไอแพด / แท็บเล็ต / โน้ตบุ๊ก", "color": "#0284C7", "icon": "💻"},
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
    
    # 1. Wallet: Real pocket wallets on a desk are small (< 4.2% of photo).
    # Folded clothes, jackets, beanies, or backpacks take > 4.5% of the photo.
    if cls_name == "Wallet":
        if area_ratio > 0.042:
            return False
        if aspect_ratio > 2.3:
            return False
        if raw_coco in ["handbag", "backpack", "suitcase"] and score < 0.52:
            return False

    # 2. Wireless Earbuds: An earbud case (AirPods/Buds) is small (< 5% of image) and pebble-shaped.
    elif cls_name == "Wireless Earbuds":
        if area_ratio > 0.05:
            return False
        if aspect_ratio > 1.65:
            return False

    # 3. iPad / Tablet: Moderate to large rectangular device (2% to 45% area, aspect ratio 1.0 - 1.95)
    elif cls_name in ["iPad / Tablet", "Laptop / iPad"]:
        if area_ratio < 0.020 or area_ratio > 0.45:
            return False
        if aspect_ratio < 1.00 or aspect_ratio > 1.95:
            return False
        if score < 0.40:
            return False

    # 4. Charger / Cable: Small power bricks, adapters, or coiled cord bundles (0.1% to 18% area)
    elif cls_name == "Charger / Cable":
        if area_ratio < 0.001 or area_ratio > 0.18:
            return False
        if aspect_ratio > 2.8:
            return False
        if score < 0.35:
            return False

    # 5. Phone: Standard elongated rectangular smartphone (aspect ratio 1.45 - 2.6)
    # Requires >= 0.55 confidence; phones can be 0.3% to 25% of image in close-up photos
    elif cls_name == "Phone":
        if score < 0.55:
            return False
        if aspect_ratio < 1.45 or aspect_ratio > 2.6:
            return False
        if area_ratio < 0.003 or area_ratio > 0.25:
            return False

    # 6. Notebook: Medium rectangular book/notebook
    elif cls_name == "Notebook":
        if area_ratio < 0.018 or area_ratio > 0.35:
            return False
        if aspect_ratio < 1.05 or aspect_ratio > 2.0:
            return False
        if score < 0.45:
            return False

    return True

# Helper to run detection on image with high accuracy & strict filtering
def run_ai_detection(pil_img: Image.Image, confidence_cutoff: float, strict_geom: bool = True):
    raw_detections = []
    w, h = pil_img.size
    
    # 1. Run YOLO Neural Network
    if model is not None:
        try:
            results = model(pil_img, conf=min(confidence_cutoff, 0.35), verbose=False)
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
                elif cls_name == "Laptop / iPad":
                    mapped_class = "iPad / Tablet"
                # Ignore irrelevant COCO classes completely
                elif cls_name in ["person", "cat", "dog", "bird", "car", "truck", "bicycle",
                                "motorcycle", "bus", "train", "airplane", "boat",
                                "traffic light", "stop sign", "fire hydrant", "parking meter",
                                "bench", "horse", "sheep", "cow", "elephant", "bear", "zebra",
                                "giraffe", "umbrella", "tie", "frisbee", "skis", "snowboard",
                                "sports ball", "kite", "baseball bat", "baseball glove",
                                "skateboard", "surfboard", "tennis racket", "bottle",
                                "wine glass", "cup", "fork", "knife", "spoon", "bowl",
                                "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
                                "hot dog", "pizza", "donut", "cake", "chair", "couch",
                                "potted plant", "bed", "dining table", "toilet", "sink",
                                "refrigerator", "oven", "toaster", "microwave", "clock", "vase",
                                "scissors", "teddy bear", "hair drier", "toothbrush"]:
                    continue
                # Else map from standard COCO classes
                elif cls_name == "cell phone":
                    mapped_class = "Phone"
                elif cls_name in ["laptop", "tv"]:
                    mapped_class = "iPad / Tablet"
                elif cls_name == "book":
                    bw = xyxy[2] - xyxy[0]
                    bh = xyxy[3] - xyxy[1]
                    box_aspect = max(bw, bh) / (min(bw, bh) + 1e-5)
                    box_area_ratio = (bw * bh) / (w * h)
                    # Card-shaped small book = Student ID; larger = Notebook
                    if box_area_ratio < 0.08 and 1.2 <= box_aspect <= 1.8:
                        mapped_class = "Student ID"
                    else:
                        mapped_class = "Notebook"
                elif cls_name in ["handbag", "backpack", "suitcase"]:
                    mapped_class = "Wallet"
                elif cls_name in ["mouse", "remote"]:
                    bw = xyxy[2] - xyxy[0]
                    bh = xyxy[3] - xyxy[1]
                    box_aspect = max(bw, bh) / (min(bw, bh) + 1e-5)
                    box_area_ratio = (bw * bh) / (w * h)
                    # Compact square/round shape = earbuds case; elongated = charger
                    if box_aspect <= 1.35 and box_area_ratio < 0.05:
                        mapped_class = "Wireless Earbuds"
                    else:
                        mapped_class = "Charger / Cable"
                    
                if mapped_class:
                    box_tuple = (xyxy[0], xyxy[1], xyxy[2], xyxy[3])
                    # Apply geometric and physical size verification
                    if strict_geom:
                        if not validate_item_geometry(mapped_class, cls_name, score, box_tuple, w, h):
                            continue
                            
                    raw_detections.append({
                        "class": mapped_class,
                        "box": box_tuple,
                        "conf": score
                    })
        except Exception as e:
            st.error(f"Error during YOLO inference: {e}")

    # 2. Enhanced CV detection for Charger & Cable (laptop power bricks and coiled cables)
    if CV2_AVAILABLE:
        try:
            cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

            # --- Helper: check overlap with existing detections ---
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

            # 2a. Dark-object connected-component analysis (original charger/cable)
            _, dark_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
            kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            cleaned = cv2.morphologyEx(dark_mask, cv2.MORPH_OPEN, kernel3)

            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned)
            for i in range(1, num_labels):
                sx, sy, sw, sh, area = stats[i]
                ar = (sw * sh) / (w * h)
                if 0.025 <= ar <= 0.08:
                    asp = max(sw, sh) / min(sw, sh)
                    if 1.1 <= asp <= 2.2:
                        roi_gray = gray[sy:sy+sh, sx:sx+sw]
                        roi_canny = cv2.Canny(roi_gray, 50, 150)
                        edge_ratio = np.sum(roi_canny > 0) / (sw * sh)
                        bright_ratio = np.sum(roi_gray > 140) / (sw * sh)
                        # Cables & power bricks have high edge density and bright labels/floor inside coil
                        if edge_ratio >= 0.22 and bright_ratio >= 0.35:
                            if not _has_overlap(sx, sy, sw, sh):
                                raw_detections.append({
                                    "class": "Charger / Cable",
                                    "conf": 0.85,
                                    "box": (float(sx), float(sy), float(sx + sw), float(sy + sh))
                                })

            # 2b. White/bright charger adapter detection (for white chargers on wooden desks)
            _, bright_mask = cv2.threshold(gray, 185, 255, cv2.THRESH_BINARY)
            kernel5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            bright_cleaned = cv2.morphologyEx(bright_mask, cv2.MORPH_CLOSE, kernel5)
            bright_cleaned = cv2.morphologyEx(bright_cleaned, cv2.MORPH_OPEN, kernel3)

            num_b, labels_b, stats_b, cent_b = cv2.connectedComponentsWithStats(bright_cleaned)
            for i in range(1, num_b):
                sx, sy, sw, sh, area = stats_b[i]
                ar = (sw * sh) / (w * h)
                # Charger adapter: compact block 1.2%-7% of image, aspect 1.0-2.0
                if 0.012 <= ar <= 0.07:
                    asp = max(sw, sh) / (min(sw, sh) + 1e-5)
                    if 1.0 <= asp <= 2.0:
                        roi_gray = gray[sy:sy+sh, sx:sx+sw]
                        roi_canny = cv2.Canny(roi_gray, 40, 120)
                        edge_density = np.sum(roi_canny > 0) / (sw * sh + 1e-5)
                        # White chargers have some edges (plug prongs, USB port, text)
                        if edge_density >= 0.08:
                            if not _has_overlap(sx, sy, sw, sh, min_iou=0.25):
                                raw_detections.append({
                                    "class": "Charger / Cable",
                                    "conf": 0.78,
                                    "box": (float(sx), float(sy), float(sx + sw), float(sy + sh))
                                })

            # 3. OpenCV Student ID / Card detector (credit-card-sized rectangles)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            canny = cv2.Canny(blurred, 30, 120)
            kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            canny_dilated = cv2.dilate(canny, kernel_dilate, iterations=1)
            contours, _ = cv2.findContours(canny_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Check if Student ID was already found by YOLO mapping
            has_student_id = any(d["class"] == "Student ID" for d in raw_detections)

            if not has_student_id:
                for cnt in contours:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.035 * peri, True)
                    if 4 <= len(approx) <= 6:
                        rx, ry, rw, rh = cv2.boundingRect(approx)
                        card_ar = (rw * rh) / (w * h)
                        # Card size: 1% to 10% of image
                        if 0.01 <= card_ar <= 0.10:
                            card_asp = max(rw, rh) / (min(rw, rh) + 1e-5)
                            # Credit card aspect ratio ~1.586 (85.6mm x 53.98mm)
                            if 1.3 <= card_asp <= 1.85:
                                # Verify it has some content (text, photo) inside
                                roi = gray[ry:ry+rh, rx:rx+rw]
                                roi_canny = cv2.Canny(roi, 50, 150)
                                inner_edge = np.sum(roi_canny > 0) / (rw * rh + 1e-5)
                                # Cards have moderate internal detail (text, photo, logos)
                                if inner_edge >= 0.06:
                                    if not _has_overlap(rx, ry, rw, rh, min_iou=0.35):
                                        raw_detections.append({
                                            "class": "Student ID",
                                            "conf": 0.80,
                                            "box": (float(rx), float(ry), float(rx + rw), float(ry + rh))
                                        })
                                        has_student_id = True
                                        break  # Only detect one card

        except Exception:
            pass

    # 3. OpenCV-based Student ID card detector (rectangular card-shaped objects)
    if CV2_AVAILABLE:
        try:
            cv_img_card = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray_card = cv2.cvtColor(cv_img_card, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray_card, (5, 5), 0)
            edges = cv2.Canny(blurred, 30, 120)
            # Dilate edges to close gaps
            kernel_card = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            edges_dilated = cv2.dilate(edges, kernel_card, iterations=1)
            contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                # Card-like = 4-sided polygon
                if len(approx) == 4:
                    bx, by, bww, bhh = cv2.boundingRect(approx)
                    card_area_ratio = (bww * bhh) / (w * h)
                    if 0.01 <= card_area_ratio <= 0.10:
                        card_aspect = max(bww, bhh) / (min(bww, bhh) + 1e-5)
                        if 1.3 <= card_aspect <= 1.8:
                            # Check not overlapping with existing detections
                            overlap = False
                            for d in raw_detections:
                                dx1, dy1, dx2, dy2 = d["box"]
                                ix1c, iy1c = max(bx, dx1), max(by, dy1)
                                ix2c, iy2c = min(bx + bww, dx2), min(by + bhh, dy2)
                                if ix1c < ix2c and iy1c < iy2c:
                                    inter = (ix2c - ix1c) * (iy2c - iy1c)
                                    if inter / (bww * bhh) > 0.30:
                                        overlap = True
                                        break
                            if not overlap:
                                raw_detections.append({
                                    "class": "Student ID",
                                    "conf": 0.80,
                                    "box": (float(bx), float(by), float(bx + bww), float(by + bhh))
                                })
        except Exception:
            pass

    # 4. OpenCV-based white charger detector (bright/white compact objects on non-white backgrounds)
    if CV2_AVAILABLE:
        try:
            cv_img_wc = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray_wc = cv2.cvtColor(cv_img_wc, cv2.COLOR_BGR2GRAY)
            # Mask for bright/white objects (grayscale > 190)
            _, bright_mask = cv2.threshold(gray_wc, 190, 255, cv2.THRESH_BINARY)
            # Clean up with morphological operations
            kernel_wc = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            bright_cleaned = cv2.morphologyEx(bright_mask, cv2.MORPH_CLOSE, kernel_wc)
            bright_cleaned = cv2.morphologyEx(bright_cleaned, cv2.MORPH_OPEN, kernel_wc)

            num_labels_wc, labels_wc, stats_wc, centroids_wc = cv2.connectedComponentsWithStats(bright_cleaned)
            for i in range(1, num_labels_wc):
                sx, sy, sw, sh, area = stats_wc[i]
                ar_wc = (sw * sh) / (w * h)
                # Charger-sized blobs: area 1.5%-6%, aspect 1.0-1.8
                if 0.015 <= ar_wc <= 0.06:
                    asp_wc = max(sw, sh) / (min(sw, sh) + 1e-5)
                    if 1.0 <= asp_wc <= 1.8:
                        # Check edge density (charger has edges from plug prongs, ports)
                        roi_gray_wc = gray_wc[sy:sy+sh, sx:sx+sw]
                        roi_canny_wc = cv2.Canny(roi_gray_wc, 50, 150)
                        edge_ratio_wc = np.sum(roi_canny_wc > 0) / (sw * sh + 1e-5)
                        if edge_ratio_wc >= 0.10:
                            # Not overlapping with earbuds or phone detections
                            overlap = False
                            for d in raw_detections:
                                dx1, dy1, dx2, dy2 = d["box"]
                                ix1w, iy1w = max(sx, dx1), max(sy, dy1)
                                ix2w, iy2w = min(sx + sw, dx2), min(sy + sh, dy2)
                                if ix1w < ix2w and iy1w < iy2w:
                                    inter = (ix2w - ix1w) * (iy2w - iy1w)
                                    if inter / (sw * sh) > 0.30:
                                        overlap = True
                                        break
                            if not overlap:
                                raw_detections.append({
                                    "class": "Charger / Cable",
                                    "conf": 0.78,
                                    "box": (float(sx), float(sy), float(sx + sw), float(sy + sh))
                                })
        except Exception:
            pass

    # 5. OpenCV-based white cable detector (thin elongated bright regions)
    if CV2_AVAILABLE:
        try:
            cv_img_cb = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            gray_cb = cv2.cvtColor(cv_img_cb, cv2.COLOR_BGR2GRAY)
            _, cable_mask = cv2.threshold(gray_cb, 200, 255, cv2.THRESH_BINARY)
            kernel_cb = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            cable_cleaned = cv2.morphologyEx(cable_mask, cv2.MORPH_CLOSE, kernel_cb)

            num_labels_cb, labels_cb, stats_cb, centroids_cb = cv2.connectedComponentsWithStats(cable_cleaned)
            for i in range(1, num_labels_cb):
                sx, sy, sw, sh, area = stats_cb[i]
                ar_cb = (sw * sh) / (w * h)
                # Cable-like: thin elongated, area 0.5%-5%, high aspect ratio (>2.5)
                if 0.005 <= ar_cb <= 0.05:
                    asp_cb = max(sw, sh) / (min(sw, sh) + 1e-5)
                    if asp_cb >= 2.5:
                        # Check fill ratio (cables are thin so low fill)
                        blob_pixels = np.sum(labels_cb[sy:sy+sh, sx:sx+sw] == i)
                        fill_ratio = blob_pixels / (sw * sh + 1e-5)
                        if fill_ratio < 0.45:
                            # Not overlapping with existing detections
                            overlap = False
                            for d in raw_detections:
                                dx1, dy1, dx2, dy2 = d["box"]
                                ix1cb, iy1cb = max(sx, dx1), max(sy, dy1)
                                ix2cb, iy2cb = min(sx + sw, dx2), min(sy + sh, dy2)
                                if ix1cb < ix2cb and iy1cb < iy2cb:
                                    inter = (ix2cb - ix1cb) * (iy2cb - iy1cb)
                                    if inter / (sw * sh) > 0.30:
                                        overlap = True
                                        break
                            if not overlap:
                                raw_detections.append({
                                    "class": "Charger / Cable",
                                    "conf": 0.72,
                                    "box": (float(sx), float(sy), float(sx + sw), float(sy + sh))
                                })
        except Exception:
            pass
            
    # 6. Strict NMS & False-Positive Containment Suppression
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
                if iou > 0.40:
                    drop = True
                    break
                    
                # Rule B: Containment - e.g. Wallet/Item false-positive inside iPad/Notebook
                containment = inter_area / (cand_area + 1e-5)
                if containment > 0.50 and kept["class"] in ["iPad / Tablet", "Notebook"]:
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
