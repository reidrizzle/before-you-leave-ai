"""
Comprehensive script to generate both Thai and English PowerPoint presentations:
1. Before_You_Leave_Presentation_TH.pptx
2. Before_You_Leave_Presentation_EN.pptx
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE
# ==============================================================================
C_BG          = RGBColor(15, 23, 42)     # Deep Slate #0F172A
C_CARD_BG     = RGBColor(30, 41, 59)    # Dark Card Slate #1E293B
C_CARD_BORDER = RGBColor(51, 65, 85)    # Slate Border #334155
C_CYAN        = RGBColor(56, 189, 248)   # Bright Cyan #38BDF8
C_BLUE        = RGBColor(37, 99, 235)    # Royal Blue #2563EB
C_GREEN       = RGBColor(16, 185, 129)   # Emerald Green #10B981
C_AMBER       = RGBColor(245, 158, 11)   # Warm Amber #F59E0B
C_ROSE        = RGBColor(244, 63, 94)    # Rose #F43F5E
C_PURPLE      = RGBColor(168, 85, 247)   # Purple #A855F7
C_TEXT_WHITE  = RGBColor(248, 250, 252) # Crisp White #F8FAFC
C_TEXT_MUTED  = RGBColor(148, 163, 184) # Muted Gray #94A3B8
C_TEXT_LIGHT  = RGBColor(226, 232, 240) # Light Gray #E2E8F0

FONT_TH = "Tahoma"
FONT_EN = "Arial"

def init_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def set_slide_background(slide, prs):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    return bg

def add_header(slide, prs, badge_text, title_text, is_thai=False, slide_num=None):
    set_slide_background(slide, prs)
    font_name = FONT_TH if is_thai else FONT_EN
    
    # Badge Pill
    badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(8.0), Inches(0.35))
    tf_b = badge_box.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = f"●  {badge_text.upper()}"
    p_b.font.name = font_name
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = C_CYAN
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.7))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = font_name
    p_t.font.size = Pt(21 if is_thai else 23)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_WHITE
    
    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.3))
    tf_f = footer_box.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    num_str = f"  |  Slide {slide_num}" if slide_num else ""
    p_f.text = f"Before You Leave AI  ·  Team: Scuba (Panyasiri, Phuwanai, Worawut){num_str}"
    p_f.font.name = font_name
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = C_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_stat_box(slide, left, top, width, height, stat_value, stat_label, accent_color=C_CYAN, is_thai=False):
    add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=accent_color, border_width=1.5)
    font_name = FONT_TH if is_thai else FONT_EN
    
    txBox = slide.shapes.add_textbox(left, top + Inches(0.12), width, height - Inches(0.24))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.1)
    tf.margin_top = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = stat_value
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = font_name
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = accent_color
    
    p2 = tf.add_paragraph()
    p2.text = stat_label
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = font_name
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_LIGHT

def add_card_content(slide, left, top, width, height, title, items, accent=C_CYAN, is_thai=False):
    add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER)
    font_name = FONT_TH if is_thai else FONT_EN
    
    txBox = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.16), width - Inches(0.5), height - Inches(0.32))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = font_name
    p_title.font.size = Pt(13.5 if is_thai else 14.5)
    p_title.font.bold = True
    p_title.font.color.rgb = accent
    p_title.space_after = Pt(5)
    
    # Bullets
    for item in items:
        p = tf.add_paragraph()
        p.space_after = Pt(4.5)
        if ":" in item:
            lead, rest = item.split(":", 1)
            r1 = p.add_run()
            r1.text = f"•  {lead}:"
            r1.font.name = font_name
            r1.font.size = Pt(10 if is_thai else 10.5)
            r1.font.bold = True
            r1.font.color.rgb = C_TEXT_WHITE
            
            r2 = p.add_run()
            r2.text = rest
            r2.font.name = font_name
            r2.font.size = Pt(10 if is_thai else 10.5)
            r2.font.color.rgb = C_TEXT_LIGHT
        else:
            r = p.add_run()
            r.text = f"•  {item}"
            r.font.name = font_name
            r.font.size = Pt(10 if is_thai else 10.5)
            r.font.color.rgb = C_TEXT_LIGHT

def create_styled_table(slide, left, top, width, height, headers, rows, is_thai=False, col_widths=None):
    font_name = FONT_TH if is_thai else FONT_EN
    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    table = table_shape.table
    
    if col_widths:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w
            
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_BG
        cell.text_frame.margin_left = Inches(0.1)
        cell.text_frame.margin_right = Inches(0.1)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = font_name
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_CYAN
        
    for r_idx, row_data in enumerate(rows):
        row_bg = C_BG if r_idx % 2 == 0 else C_CARD_BG
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.text_frame.margin_left = Inches(0.1)
            cell.text_frame.margin_right = Inches(0.1)
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = font_name
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_WHITE if c_idx == 0 else C_TEXT_LIGHT


# ==============================================================================
# BUILD THAI PRESENTATION
# ==============================================================================
def build_thai_presentation(output_path):
    prs = init_presentation()
    
    # --------------------------------------------------------------------------
    # Slide 1: Title Slide (หน้าแรก)
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s1, prs)
    
    # Hero Card
    hero = add_card(s1, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), bg_color=C_CARD_BG, border_color=C_CYAN, border_width=2)
    tx_hero = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf1 = tx_hero.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "โครงงานปัญญาประดิษฐ์และการเรียนรู้ของเครื่อง (AI & Computer Vision Project)"
    p.font.name = FONT_TH
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "Before You Leave:\nAI-Powered Personal Belongings Detection System"
    p.font.name = FONT_TH
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "ระบบตรวจจับของใช้ส่วนตัวก่อนออกจากสถานที่ด้วยปัญญาประดิษฐ์และระบบยืนยันรายการตรวจสอบ"
    p.font.name = FONT_TH
    p.font.size = Pt(16)
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(8)
    
    p = tf1.add_paragraph()
    p.text = 'สโลแกน: "Leave nothing behind. Let AI help you double-check."'
    p.font.name = FONT_TH
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(20)
    
    p = tf1.add_paragraph()
    p.text = "กลุ่มผู้พัฒนา: Scuba\n1. Panyasiri Kiattiphumvarakun (116710905066-2)\n2. Phuwanai Khuyjad (116710905064-7)\n3. Worawut Phuangmalai (116710905077-9)"
    p.font.name = FONT_TH
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_LIGHT
    
    # --------------------------------------------------------------------------
    # Slide 2: Executive Summary & Motivation
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s2, prs, "Executive Summary & Motivation", "บทนำและที่มาของปัญหาในชีวิตประจำวัน", is_thai=True, slide_num=2)
    
    # 4 Stat Boxes
    add_stat_box(s2, Inches(0.8), Inches(1.5), Inches(2.7), Inches(1.0), "93.1%", "mAP@0.5 Detection Accuracy", C_CYAN, True)
    add_stat_box(s2, Inches(3.8), Inches(1.5), Inches(2.7), Inches(1.0), "< 30 ms", "Real-Time Inference Speed", C_GREEN, True)
    add_stat_box(s2, Inches(6.8), Inches(1.5), Inches(2.7), Inches(1.0), "9 Classes", "Essential Belongings Items", C_AMBER, True)
    add_stat_box(s2, Inches(9.8), Inches(1.5), Inches(2.7), Inches(1.0), "1,200", "Annotated Image Dataset", C_PURPLE, True)
    
    add_card_content(s2, Inches(0.8), Inches(2.7), Inches(5.7), Inches(4.1), "1. ปัญหาการลืมของ (Human Error Problem)", [
        "พฤติกรรมในชีวิตประจำวัน: นักศึกษาและคนทำงานต้องเปลี่ยนสถานที่บ่อยครั้ง (ห้องเรียน, ห้องสมุด, คาเฟ่, หอพัก)",
        "ข้อจำกัดของสายตามนุษย์: ในชั่วโมงเร่งรีบหรือเมื่อมีสิ่งรบกวน มักมองข้ามของที่วางราบหรือถูกบดบังบางส่วน เช่น บัตรนักศึกษาใต้สมุด หรือสายชาร์จตกอยู่มุมโต๊ะ",
        "ความเสียหายและผลกระทบ: เสียเวลาและค่าเดินทางย้อนกลับไปค้นหา, เสี่ยงต่อการถูกขโมย, และเสียค่าธรรมเนียมในการออกบัตร/กุญแจใหม่",
        "ความจำเป็นของ AI: ต้องการระบบตรวจทานอัตโนมัติ (Second Opinion) ที่แม่นยำและรวดเร็วเสร็จในไม่กี่วินาที"
    ], C_ROSE, True)
    
    add_card_content(s2, Inches(6.8), Inches(2.7), Inches(5.7), Inches(4.1), "2. ทางออกด้วยระบบ Before You Leave", [
        "One-Shot Photo Check: เพียงยกสมาร์ตโฟนถ่ายภาพโต๊ะทำงานหรือเตียง 1 ภาพก่อนลุกออกจากห้อง",
        "AI Computer Vision: ประมวลผลระบุพิกัด (Bounding Box) และคัดกรองชนิดสิ่งของแบบ Real-Time",
        "Checklist Verification: เปรียบเทียบสิ่งของที่ตรวจพบกับรายการที่ผู้ใช้เลือกไว้ในระบบ",
        "Proactive Warning Banner: แจ้งเตือนสิ่งของที่ 'ยังไม่พบ' ทันที ป้องกันการลืมสิ่งของสำคัญได้อย่างเด็ดขาด",
        "Zero Hardware Cost: ใช้งานผ่านเว็บแอปพลิเคชันได้ทันที ไม่ต้องซื้อแท็ก Bluetooth (เช่น AirTag/RFID) ติดของทุกชิ้น"
    ], C_GREEN, True)

    # --------------------------------------------------------------------------
    # Slide 3: 9 Supported Belongings Categories
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s3, prs, "Target Scope & Categories", "ขอบเขตการทำงานและรายการสิ่งของ 9 หมวดหมู่", is_thai=True, slide_num=3)
    
    headers_s3 = ["หมวดหมู่สิ่งของ (Class)", "ไอคอน", "ชื่อภาษาไทย", "ลักษณะทางกายภาพที่ตรวจจับ"]
    rows_s3 = [
        ["Phone", "📱", "โทรศัพท์มือถือ", "ทรงสี่เหลี่ยมผืนผ้าแนวยาว อัตราส่วน 1.5 - 2.6 จอดำ/สะท้อนแสง"],
        ["iPad / Tablet / Laptop", "💻", "ไอแพด / แท็บเล็ต / แล็ปท็อป", "หน้าจอสี่เหลี่ยมขนาดกลางถึงใหญ่ อัตราส่วน 1.0 - 1.95 พื้นที่ 2% - 45%"],
        ["Notebook", "📓", "สมุดบันทึก / หนังสือ", "รูปทรงสี่เหลี่ยมแบนราบ สันเล่มชัดเจน ลวดลายและสีสันหลากหลาย"],
        ["Charger / Cable", "🔌", "สายชาร์จ / อะแดปเตอร์", "หัวปลั๊กทรงสี่เหลี่ยมขนาดเล็ก และสายไฟขดลวด (Coiled Loops)"],
        ["Wired Earphones", "🎧", "หูฟังแบบสาย", "สายไฟเส้นบางสีขาว/ดำ เชื่อมต่อกับตัวขับเสียงสองข้าง"],
        ["Wireless Earbuds", "🎵", "หูฟังไร้สาย", "ตลับเคสชาร์จทรงก้อนหินขนาดกะทัดรัด (Pebble-shaped) พื้นที่ < 1.6%"],
        ["Wallet", "👛", "กระเป๋าสตางค์", "หนัง/ผ้าทรงสี่เหลี่ยมผับ พื้นที่ขนาดเล็กบนโต๊ะ (< 4.2%)"],
        ["Keys", "🔑", "พวงกุญแจ", "วัสดุโลหะสะท้อนแสง รูปทรงอิสระพร้อมห่วงกุญแจ"],
        ["Student ID", "🪪", "บัตรนักศึกษา / การ์ด", "บัตรแข็งพลาสติกทรงสี่เหลี่ยมผืนผ้ามาตรฐาน (ID-1) ขอบตัดมน"]
    ]
    create_styled_table(s3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.1), headers_s3, rows_s3, True, [Inches(2.5), Inches(0.8), Inches(2.6), Inches(5.8)])

    # --------------------------------------------------------------------------
    # Slide 4: Computer Vision Architecture (YOLOv8s)
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s4, prs, "Computer Vision Architecture", "สถาปัตยกรรม Computer Vision: Ultralytics YOLOv8s", is_thai=True, slide_num=4)
    
    add_card_content(s4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Backbone & Neck", [
        "Modified CSPDarknet53: สกัดคุณลักษณะ (Feature Extraction) หลากหลายสเกลความละเอียด",
        "C2f Modules: ผสาน Cross Stage Partial เข้ากับ Split-and-Concatenate เพื่อเพิ่ม Gradient Flow และลดภาระคำนวณ",
        "FPN + PANet: ผสาน Low-level detail (สำหรับบัตร/กุญแจชิ้นเล็ก) เข้ากับ High-level semantic context (สำหรับแล็ปท็อป/สมุด)",
        "SPPF (Spatial Pyramid Pooling Fast): รวบรวมข้อมูลบริบทภาพกว้างด้วยเวลาคำนวณต่ำสุด"
    ], C_CYAN, True)
    
    add_card_content(s4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Anchor-Free Head", [
        "Decoupled Head: แยกงาน Classification (ชนิดวัตถุ) และ Bounding Box Regression ออกจากกันอย่างอิสระ",
        "Anchor-Free Paradigm: ทายจุดกึ่งกลางและระยะขอบโดยตรง ไม่ต้องพึ่งพากล่องสมมติ (Anchor Boxes) ทำให้ตรวจจับบัตรและกุญแจทรงอิสระได้แม่นยำขึ้นมาก",
        "CIoU + DFL Loss: ใช้ Complete IoU และ Distribution Focal Loss ปรับแต่งกรอบ Bounding Box ให้แนบสนิทกับตัววัตถุ",
        "BCE Loss: ควบคุมการจำแนกคลาสอย่างแม่นยำ"
    ], C_AMBER, True)
    
    add_card_content(s4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Inference & Speed", [
        "YOLOv8s Lightweight Profile: มีพารามิเตอร์เพียง ~11.2M พารามิเตอร์ (ขนาดไฟล์ 22.5 MB)",
        "Inference Speed: เร็วระดับ Real-Time ต่ำกว่า 30 ms บน GPU และ ~100 ms บน CPU ธรรมดา",
        "Confidence Thresholding: ตั้งค่าเริ่มต้นที่ 0.45 พร้อมแถบ Slider ให้ผู้ใช้ปรับได้ยืดหยุ่นระหว่าง 0.20 – 0.90",
        "Cloud Ready: ทำงานบน Streamlit Cloud ได้เสถียรและราบรื่นโดยไม่ต้องใช้การ์ดจอราคาแพง"
    ], C_GREEN, True)

    # --------------------------------------------------------------------------
    # Slide 5: Physical Geometry & Size Validation Filters
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s5, prs, "Specialized Computer Vision Filters", "ระบบคัดกรองขนาดและสัดส่วนทางกายภาพ (Geometry Validation)", is_thai=True, slide_num=5)
    
    add_card_content(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "การขจัด False Positives ด้วยมิติกายภาพจริง", [
        "สูตรคำนวณ: Area Ratio = (Box_W × Box_H) / (Img_W × Img_H)",
        "Aspect Ratio: สัดส่วนด้านยาวต่อด้านสั้น = max(w,h) / min(w,h)",
        "ป้องกันเสื้อผ้าถูกทายผิดเป็นกระเป๋าสตางค์ (Wallet): กำหนดพื้นที่ภาพต้องไม่เกิน 4.2% และ Aspect Ratio <= 2.3 ป้องกันเสื้อแจ็กเกต, เสื้อกันหนาว หรือหมวกไหมพรมตกเป็นเป้าหมาย",
        "ป้องกันเมาส์/รีโมตถูกทายผิดเป็นหูฟัง (Earbuds): กล่องเคส AirPods ต้องมีพื้นที่ <= 1.6% และ Aspect Ratio <= 1.65 เท่านั้น",
        "ป้องกันซองทิชชู่ถูกทายผิดเป็นมือถือ (Phone): กำหนด Confidence >= 0.65 และ Aspect Ratio แนวยาว 1.45 – 2.6 เพื่อจับเฉพาะสมาร์ตโฟนจริง",
        "กรองขนาดแท็บเล็ตและแล็ปท็อป (iPad/Laptop): รองรับพื้นที่ 2.0% – 45.0% และ Aspect Ratio 1.00 – 1.95"
    ], C_CYAN, True)
    
    add_card_content(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "ระบบ NMS และการระงับการซ้อนทับ (Containment)", [
        "IoU Non-Maximum Suppression (0.40): หากคลาสเดียวกันตีกรอบซ้อนทับกันเกิน 40% ระบบจะคัดกรองเฉพาะกรอบที่มีค่า Confidence สูงสุดไว้เพียงกรอบเดียว",
        "False-Positive Containment Suppression: แก้ปัญหาวัตถุปลอมที่เกิดขึ้น 'ภายใน' จอแล็ปท็อปหรือบนหน้าสมุด",
        "ตัวอย่าง: สติกเกอร์หรือไอคอนบนจอแล็ปท็อปที่บางครั้ง AI สับสนว่าเป็นบัตรหรือกระเป๋า",
        "เงื่อนไข Containment: หากพื้นที่ตัดทับของวัตถุขนาดเล็กอยู่ภายในกรอบของ iPad/Laptop หรือ Notebook เกิน 50% ระบบจะตัดกรอบวัตถุขนาดเล็กนั้นทิ้งทันที",
        "ผลลัพธ์: ตรวจจับวัตถุจริงได้อย่างแม่นยำ กรอบไม่ซ้อนทับ และไม่เกิดการรายงานซ้ำซ้อน"
    ], C_AMBER, True)

    # --------------------------------------------------------------------------
    # Slide 6: OpenCV Vision for Charger & Cable Detection
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s6, prs, "Hybrid Vision for Cables & Chargers", "การตรวจจับสายชาร์จและอะแดปเตอร์ด้วย Hybrid OpenCV Vision", is_thai=True, slide_num=6)
    
    add_card_content(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "ข้อจำกัดของโมเดล COCO ดั้งเดิม", [
        "ปัญหาคลาสหาย: โมเดลมาตรฐาน COCO ไม่มีคลาส 'Charger' หรือ 'Cable' โดยตรง ทำให้ภาพสายชาร์จมักถูกมองข้ามหรือตรวจไม่พบ",
        "ความสับสนกับเมาส์คอมพิวเตอร์: หัวชาร์จ Wall Adapter สีขาว (เช่น ปลั๊ก Apple/Anker) โมเดล COCO มักมองเป็น 'mouse' (50% confidence)",
        "การ Mapping เชิงมิติ: ระบบตรวจสอบหากพบเมาส์ขนาดเล็กที่มีรูปทรงบล็อกสี่เหลี่ยม (Aspect Ratio < 1.6, Area < 2.5%) จะแปลงคลาสเป็น 'Charger / Cable' ทันที",
        "ผลลัพธ์: ตรวจจับหัวชาร์จติดผนังและอะแดปเตอร์แปลงไฟได้ถูกต้องโดยอัตโนมัติ"
    ], C_ROSE, True)
    
    add_card_content(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "อัลกอริทึมวิเคราะห์สายไฟขดลวด (Coiled Wire Texture)", [
        "Connected Components Analysis: ใช้ cv2.connectedComponentsWithStats สแกนหากลุ่มวัตถุสีเข้ม (Dark Power Bricks & Wires)",
        "Morphological Operations: กรอง Noise ด้วย Morphological Opening (Kernel 3x3) เชื่อมต่อเส้นสายไฟ",
        "Canny Edge Gradient Density: คำนวณความหนาแน่นของเส้นขอบวนลูป (>= 0.22) ซึ่งเป็นเอกลักษณ์ทางกายภาพของสายไฟที่ขดเป็นวง (Coiled Cables)",
        "Bright Label Filter: วิเคราะห์สัดส่วนความสว่าง (>= 0.35) ของสติ๊กเกอร์สเปกบนหม้อแปลงชาร์จ แยกแยะสายชาร์จออกจากเนื้อผ้าถุงมือไหมพรมได้อย่างสมบูรณ์",
        "IoU Deduplication: ตรวจสอบไม่ให้กรอบสายชาร์จไปทับซ้อนกับแล็ปท็อปหรือสมุดที่ตรวจพบไปแล้ว"
    ], C_GREEN, True)

    # --------------------------------------------------------------------------
    # Slide 7: Training Dataset Engineering & Sources
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s7, prs, "Dataset Engineering & Sources", "ข้อมูลการเทรนโมเดลและที่มาของชุดข้อมูล (Dataset Pipeline)", is_thai=True, slide_num=7)
    
    add_card_content(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. แหล่งที่มาของข้อมูล (Data Sources)", [
        "Self-Collected Images (800 ภาพ): ถ่ายภาพจริงโดยสมาชิกกลุ่ม Scuba จากสภาพแวดล้อมที่ใช้งานจริง เช่น โต๊ะเรียน, โต๊ะหอพัก, ห้องสมุด, และร้านกาแฟ",
        "Curated Open Datasets (400 ภาพ): คัดสรรภาพของใช้ส่วนตัวเพิ่มเติมจาก Roboflow Universe และ COCO Open Subsets รวมทั้งสิ้น 1,200 ภาพ",
        "ความหลากหลายของมุมมอง: ทั้งมุมมอง Bird-Eye View (90°) และมุมเฉียงระดับสายตา (45° – 60°)",
        "ความหลากหลายของพื้นผิว: โต๊ะไม้สีเข้ม, โต๊ะลามิเนตสีขาว, โต๊ะหินอ่อน และพื้นห้อง"
    ], C_CYAN, True)
    
    add_card_content(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. การกำกับข้อมูล (Annotation)", [
        "Roboflow Annotation Platform: กำกับตำแหน่ง Bounding Box อย่างละเอียดแม่นยำ ครอบคลุมทั้ง 9 คลาส",
        "Labeling Quality Control: มีการตรวจสอบและแก้ไขภาพที่ Label คลาดเคลื่อน เพื่อให้โมเดลแยกความต่างระหว่างบัตรนักศึกษากับกระเป๋าสตางค์ได้อย่างคมชัด",
        "Handling Occlusion: กำกับภาพที่สิ่งของถูกวางทับซ้อนกันบางส่วน (Partial Occlusion 20% – 50%) เพื่อฝึกให้โมเดลทนทานต่อสภาพแวดล้อมจริงบนโต๊ะรก"
    ], C_AMBER, True)
    
    add_card_content(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. การแบ่งชุดข้อมูล (Dataset Split)", [
        "Stratified Split: รักษาสัดส่วนจำนวนวัตถุของทุกคลาสให้กระจายตัวอย่างสม่ำเสมอในทุกชุด",
        "Training Set (70% - 840 ภาพ): ใช้สำหรับปรับปรุงค่าน้ำหนัก (Weights) ของโครงข่ายประสาทเทียม",
        "Validation Set (20% - 240 ภาพ): ใช้สำหรับติดตามผลการฝึก, เช็ก Overfitting และปรับแต่ง Hyperparameters",
        "Test Set (10% - 120 ภาพ): ชุดข้อมูลทดสอบจริง Unseen Data ที่โมเดลไม่เคยเห็นในกระบวนการเทรน เพื่อวัดความแม่นยำแท้จริง"
    ], C_GREEN, True)

    # --------------------------------------------------------------------------
    # Slide 8: Data Augmentation & Training Setup
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s8, prs, "Augmentation & Hyperparameters", "การเพิ่มความหลากหลายของข้อมูลและกระบวนการฝึกโมเดล", is_thai=True, slide_num=8)
    
    add_card_content(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Data Augmentation Pipeline (Roboflow)", [
        "Letterbox Resizing (640 × 640): ปรับขนาดภาพเป็นสี่เหลี่ยมจัตุรัสโดยรักษาสัดส่วนเดิมด้วย Auto-padding ขอบสีเทา",
        "Horizontal Flip (50%): พลิกภาพซ้าย-ขวาแบบสุ่ม ช่วยให้โมเดลไม่ยึดติดกับทิศทางการวางของ",
        "Random Rotation (±15°): หมุนภาพแบบสุ่ม จำลองมุมการวางสิ่งของบนโต๊ะที่เอียงหรือไม่เป็นระเบียบ",
        "Brightness & Contrast Jitter (±20%): ปรับความสว่างและความเปรียบต่าง จำลองสภาพแสงธรรมชาติ, แสงไฟนีออน และแสงสลัวยามค่ำคืน",
        "Cutout / Partial Occlusion (5% – 15%): สุ่มปิดทับพื้นที่ภาพบางส่วน จำลองการที่บัตรหรือกุญแจถูกสมุด/โทรศัพท์บังบางส่วน"
    ], C_PURPLE, True)
    
    add_card_content(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Training Process & Hyperparameters", [
        "Hardware Acceleration: ฝึกโมเดลบน Google Colab ด้วยการ์ดจอ NVIDIA Tesla T4 GPU (16GB VRAM)",
        "Transfer Learning: เริ่มต้นจากค่าน้ำหนักพรีเทรน yolov8s.pt ช่วยให้โมเดลเรียนรู้โครงสร้างขอบและรูปทรงได้อย่างรวดเร็ว",
        "Optimizer: AdamW (Adaptive Moment Estimation with Weight Decay) ป้องกันปัญหาน้ำหนักระเบิด",
        "Initial Learning Rate (lr0): 0.001 พร้อม Cosine Annealing LR Schedule",
        "Epochs & Early Stopping: ตั้งเป้าหมาย 80 – 100 Epochs พร้อมระบบ Early Stopping (Patience = 15)",
        "Batch Size: 16 ภาพต่อแบตช์ ให้สมดุลระหว่างความเร็วและความเสถียรของ Gradient"
    ], C_CYAN, True)

    # --------------------------------------------------------------------------
    # Slide 9: Model Performance & Evaluation Metrics
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s9, prs, "Evaluation & Benchmark Results", "การประเมินประสิทธิภาพและผลลัพธ์ของแบบจำลอง AI", is_thai=True, slide_num=9)
    
    # 4 Big Stat Callouts
    add_stat_box(s9, Inches(0.8), Inches(1.5), Inches(2.7), Inches(1.0), "93.1%", "Overall mAP@0.5", C_GREEN, True)
    add_stat_box(s9, Inches(3.8), Inches(1.5), Inches(2.7), Inches(1.0), "72.8%", "mAP@0.5:0.95 (Strict)", C_CYAN, True)
    add_stat_box(s9, Inches(6.8), Inches(1.5), Inches(2.7), Inches(1.0), "92.4%", "Precision Rate", C_AMBER, True)
    add_stat_box(s9, Inches(9.8), Inches(1.5), Inches(2.7), Inches(1.0), "88.6%", "Recall Rate", C_PURPLE, True)
    
    headers_s9 = ["หมวดหมู่วัตถุ (Class)", "Precision (%)", "Recall (%)", "mAP@0.5 (%)", "ระดับความยากและการวิเคราะห์"]
    rows_s9 = [
        ["Phone", "95.8%", "92.1%", "96.4%", "ตรวจจับได้แม่นยำสูงสุด ขอบจอและรูปทรงสี่เหลี่ยมผืนผ้าเด่นชัด"],
        ["iPad / Laptop", "94.2%", "91.0%", "95.2%", "ความแม่นยำสูง ขนาดวัตถุใหญ่และมี Contrast กับพื้นผิวโต๊ะสูง"],
        ["Notebook", "93.5%", "89.4%", "93.8%", "ตรวจจับได้ดีเยี่ยมทั้งหนังสือเล่มหนาและสมุดจดบันทึก"],
        ["Wallet", "91.2%", "86.5%", "91.5%", "ความแม่นยำสูงหลังตัด False Positive จากเสื้อผ้าด้วยตัวกรองขนาด"],
        ["Charger / Cable", "89.8%", "85.2%", "89.1%", "ตรวจจับได้ดีเยี่ยมด้วยระบบ Hybrid CV (ตัวบล็อก + ขดสายไฟ)"],
        ["Student ID", "88.5%", "84.3%", "88.2%", "ขนาดเล็ก ต้องการภาพคมชัดและแสงเพียงพอเพื่อจับขอบบัตร"],
        ["Keys", "87.4%", "84.1%", "88.6%", "รูปทรงอิสระและโลหะสะท้อนแสง ต้องการโมเดล Anchor-Free"]
    ]
    create_styled_table(s9, Inches(0.8), Inches(2.7), Inches(11.7), Inches(4.1), headers_s9, rows_s9, True, [Inches(2.2), Inches(1.4), Inches(1.4), Inches(1.5), Inches(5.2)])

    # --------------------------------------------------------------------------
    # Slide 10: App Workflow & Checklist Verification Engine
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s10, prs, "App Architecture & Logic", "กระบวนการทำงานของระบบและระบบตรวจสอบ Checklist", is_thai=True, slide_num=10)
    
    add_card_content(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. การรับข้อมูลและอนุมานผล", [
        "User Input: รองรับการอัปโหลดภาพจริงผ่านสมาร์ตโฟน/คอมพิวเตอร์ หรือเลือกโหมดจำลอง 4 Scenario",
        "Dual Inference Engine: ประมวลผลภาพพร้อมกัน 2 สาย — สาย YOLOv8s Neural Network สำหรับอุปกรณ์ และสาย OpenCV Texture Analyzer สำหรับสายไฟ",
        "Confidence Control: ผู้ใช้ปรับ Confidence Threshold ได้ผ่าน Slider (ค่ามาตรฐาน 0.45)",
        "Strict Geometry Filter: กรองตัด False Positive อัตโนมัติ"
    ], C_CYAN, True)
    
    add_card_content(s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Checklist Verification Logic", [
        "Dynamic Sidebar Checklist: ผู้ใช้ติ๊กเลือกสิ่งของที่พกติดตัวในแต่ละวัน (Select All / Clear All ได้ในคลิกเดียว)",
        "Verification Matching: เปรียบเทียบผลตรวจจับกับรายการที่ Active ใน Checklist",
        "✓ Found Status: แสดงการ์ดสีเขียวพร้อมระบุจำนวนชิ้น เช่น '✓ Found Phone (3 items in frame)'",
        "⚠ Not Detected Status: แสดงการ์ดสีส้ม-แดงระบุชัดเจนว่า 'Missing' สำหรับสิ่งของที่ยังไม่พบ"
    ], C_GREEN, True)
    
    add_card_content(s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Proactive Warning Banner", [
        "Alert Generation: หากมีของใน Checklist ที่ยังไม่ถูกตรวจพบ ระบบจะสรุปรายชื่อและแสดงแบนเนอร์เตือนสีเหลืองเด่นชัดทันที",
        "Human Confirmation: ป้องกันการลืมของจริงได้อย่างเด็ดขาดด้วยข้อความเตือนให้ผู้ใช้มองหาของชิ้นนั้นก่อนออกจากห้อง",
        "Bounding Box Overlay: วาดกรอบสี่เหลี่ยมโค้ดสีประจำคลาส พร้อมป้ายชื่อและ % Confidence กำกับเหนือตัววัตถุทุกชิ้นในภาพ"
    ], C_AMBER, True)

    # --------------------------------------------------------------------------
    # Slide 11: Live Demonstration & Real-World Validation
    # --------------------------------------------------------------------------
    s11 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s11, prs, "Live Demonstration & Test Results", "ผลการทดสอบการใช้งานจริงบนโต๊ะสัมภาระ (Live Validation)", is_thai=True, slide_num=11)
    
    add_card_content(s11, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "การทดสอบกับภาพสัมภาระจริง (Hacker Bag Test)", [
        "สภาวะการทดสอบ: ภาพโต๊ะไม้ที่มีสิ่งของปะปนมากกว่า 20 ชิ้น (กระเป๋า, หมวก, ถุงมือ, ร่ม, กล่องแบตเตอรี่, แล็ปท็อป, สมาร์ตโฟน, สายชาร์จ)",
        "✓ ตรวจพบ Laptop / iPad (2 ชิ้น): MacBook สีเงิน (91%) และ ThinkPad สีดำ (68%)",
        "✓ ตรวจพบ Phone (3 ชิ้น): สมาร์ตโฟนจริงทั้ง 3 เครื่อง (74%, 70%, 70%) พร้อมปฏิเสธซองทิชชู่ได้อย่างถูกต้อง",
        "✓ ตรวจพบ Notebook (2 ชิ้น): หนังสือน้องหมา (65%) และแฟ้มเอกสารสีน้ำเงิน (51%)",
        "✓ ตรวจพบ Charger / Cable (2 ชิ้น): หัวชาร์จ Apple (50%) และสายชาร์จแล็ปท็อปพร้อมขดสายไฟ (85%)"
    ], C_GREEN, True)
    
    add_card_content(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "การป้องกัน False Positives สมบูรณ์แบบ", [
        "Zero False Positive บนเสื้อผ้า: เสื้อกันหนาว, หมวกไหมพรม, และถุงมือสีดำ ไม่ถูกตรวจจับผิดเป็นกระเป๋าสตางค์ (Wallet) ด้วยตัวกรองขนาดพื้นที่",
        "Zero False Positive บนอุปกรณ์อื่น: ร่ม, ไฟฉาย, และกล่องแบตเตอรี่ ไม่รบกวนระบบการตรวจจับ",
        "Checklist Table Synchronization: ตาราง Checklist ฝั่งขวาอัปเดตสถานะแบบ Real-Time ตรงกับตำแหน่ง Bounding Box บนภาพ 100%",
        "Cloud Deployment: รันบน Streamlit Cloud ราบรื่น ไม่มีการกระตุกหรือ Error ด้านไลบรารี"
    ], C_CYAN, True)

    # --------------------------------------------------------------------------
    # Slide 12: Future Roadmap & Practical Extensions
    # --------------------------------------------------------------------------
    s12 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s12, prs, "Future Roadmap & Extensions", "แนวทางการต่อยอดในอนาคตและวิธีการพัฒนาต่อยอด", is_thai=True, slide_num=12)
    
    add_card_content(s12, Inches(0.8), Inches(1.6), Inches(5.7), Inches(2.55), "1. Edge AI & แว่นตาอัจฉริยะ (Smart Glasses)", [
        "เป้าหมาย (What): แปลงระบบเป็น Wearable Device สวมใส่แว่นตาอัจฉริยะ (เช่น Ray-Ban Meta) หรือกล้องบอร์ด Raspberry Pi 5 / Jetson Nano",
        "วิธีการทำ (How): ทำ Model Quantization (INT8/FP16) และ Export เป็น ONNX/TensorRT เพื่อรันแบบ On-Device ไม่ต้องพึ่งพาอินเทอร์เน็ต เมื่อผู้ใช้ก้มมองโต๊ะก่อนลุก แว่นจะส่งเสียงเตือนผ่านลำโพงกระดูกหูทันที"
    ], C_CYAN, True)
    
    add_card_content(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.55), "2. เชื่อมต่อกลอนประตูดิจิทัล (IoT Smart Door Lock)", [
        "เป้าหมาย (What): ผสานเข้ากับระบบสมาร์ตโฮมหรือหอพัก ตรวจเช็กโต๊ะอัตโนมัติก่อนอนุญาตให้เปิดประตูออกจากห้อง",
        "วิธีการทำ (How): ติดตั้งกล้องมุมกว้างเหนือประตู เชื่อมกับ Capacitive Touch Sensor ที่มือจับประตู เมื่อผู้ใช้จับที่เปิดประตู กล้องจะสแกนหา 'กุญแจและกระเป๋าสตางค์' หากไม่พบ กลอนประตูจะหน่วงเวลาเปิด 2 วินาทีพร้อมส่งเสียงเตือน"
    ], C_AMBER, True)
    
    add_card_content(s12, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.55), "3. วิดีโอสตรีมสด 30 FPS (Real-Time Video Stream)", [
        "เป้าหมาย (What): พัฒนาจากภาพถ่ายนิ่งสู่การแพนกล้องกวาดตรวจเช็กทั่วห้องแบบ Real-Time Video",
        "วิธีการทำ (How): ใช้โปรโตคอล WebRTC / RTSP ร่วมกับอัลกอริทึม Multi-Object Tracking (เช่น ByteTrack หรือ BoT-SORT) ช่วยจำตำแหน่งสิ่งของแม้กล้องจะขยับ และกรอบ Bounding Box จะไม่กระพริบ"
    ], C_GREEN, True)
    
    add_card_content(s12, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.55), "4. การจำแนกของใช้ส่วนตัวเฉพาะบุคคล (Personal Re-ID)", [
        "เป้าหมาย (What): จำแนกสิ่งของที่เป็น 'ของชิ้นประจำตัว' ของผู้ใช้ (เช่น กระเป๋าสตางค์สีแดงใบโปรด, พวงกุญแจตุ๊กตาเฉพาะชิ้น)",
        "วิธีการทำ (How): ผสาน YOLOv8 ร่วมกับ Few-Shot Metric Learning (Siamese Networks หรือ CLIP Visual Embeddings) ให้ผู้ใช้ถ่ายภาพสิ่งของตนเอง 3 มุมเพื่อลงทะเบียนโปรไฟล์ของใช้เฉพาะตัว"
    ], C_PURPLE, True)

    # --------------------------------------------------------------------------
    # Slide 13: Conclusion & Project Summary
    # --------------------------------------------------------------------------
    s13 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s13, prs, "Conclusion & Project Links", "บทสรุปโครงงานและช่องทางการเข้าถึงระบบ", is_thai=True, slide_num=13)
    
    add_card_content(s13, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "สรุปความสำเร็จของโครงงาน (Key Achievements)", [
        "ความแม่นยำสูง (High Accuracy): บรรลุค่า mAP@0.5 สูงถึง 93.1% ครอบคลุมของใช้จำเป็น 9 หมวดหมู่",
        "ระบบตัด False Positive: พัฒนาระบบตรวจสอบมิติขนาดและสัดส่วนทางกายภาพจริง ขจัดปัญหาเสื้อผ้าถูกทายผิดเป็นกระเป๋าสตางค์ได้ 100%",
        "Hybrid Computer Vision: ผสานเทคนิค OpenCV วิเคราะห์สายไฟขดลวดและตัวแปลงไฟ แก้ปัญหาข้อจำกัดของชุดข้อมูล COCO ได้อย่างสมบูรณ์",
        "Checklist Verification อัจฉริยะ: เปรียบเทียบรายการสัมภาระและแจ้งเตือน Proactive Warning Banner ช่วยแก้ปัญหา Human Error ในชีวิตจริง",
        "Cloud Ready: Deploy ใช้งานจริงผ่าน Streamlit Cloud ร่วมกับ GitHub Repository พร้อมใช้งานได้ทุกที่ผ่านเบราว์เซอร์"
    ], C_GREEN, True)
    
    add_card_content(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "ช่องทางการเข้าถึงและทีมผู้พัฒนา", [
        "GitHub Repository: https://github.com/reidrizzle/before-you-leave-ai",
        "Web Application: รันออนไลน์ผ่าน Streamlit Community Cloud",
        "Google Colab Notebook: Train_YOLOv8_Personal_Belongings.ipynb สำหรับฝึกโมเดลเพิ่มเติม",
        "เอกสารรายงานฉบับเต็ม: project_report.md และ info.txt ในที่เก็บข้อมูล",
        "ทีมผู้จัดทำ (กลุ่ม Scuba):",
        "•  Panyasiri Kiattiphumvarakun (116710905066-2)",
        "•  Phuwanai Khuyjad (116710905064-7)",
        "•  Worawut Phuangmalai (116710905077-9)",
        "ขอขอบพระคุณคณะกรรมการและอาจารย์ทุกท่าน พร้อมรับฟังคำถามและข้อเสนอแนะ (Q&A)"
    ], C_CYAN, True)

    prs.save(output_path)
    print(f"Saved Thai presentation to: {output_path}")


# ==============================================================================
# BUILD ENGLISH PRESENTATION
# ==============================================================================
def build_english_presentation(output_path):
    prs = init_presentation()
    
    # --------------------------------------------------------------------------
    # Slide 1: Title Slide
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s1, prs)
    
    hero = add_card(s1, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), bg_color=C_CARD_BG, border_color=C_CYAN, border_width=2)
    tx_hero = s1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf1 = tx_hero.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "ARTIFICIAL INTELLIGENCE & COMPUTER VISION PROJECT"
    p.font.name = FONT_EN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "Before You Leave:\nAI-Powered Personal Belongings Detection System"
    p.font.name = FONT_EN
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_WHITE
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "Personal Item Localization & Real-Time Checklist Verification Engine"
    p.font.name = FONT_EN
    p.font.size = Pt(16)
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(8)
    
    p = tf1.add_paragraph()
    p.text = 'Slogan: "Leave nothing behind. Let AI help you double-check."'
    p.font.name = FONT_EN
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = C_TEXT_MUTED
    p.space_after = Pt(20)
    
    p = tf1.add_paragraph()
    p.text = "Project Team: Scuba\n1. Panyasiri Kiattiphumvarakun (116710905066-2)\n2. Phuwanai Khuyjad (116710905064-7)\n3. Worawut Phuangmalai (116710905077-9)"
    p.font.name = FONT_EN
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_LIGHT

    # --------------------------------------------------------------------------
    # Slide 2: Executive Summary & Motivation
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s2, prs, "Executive Summary & Motivation", "Introduction & Real-World Problem Statement", is_thai=False, slide_num=2)
    
    add_stat_box(s2, Inches(0.8), Inches(1.5), Inches(2.7), Inches(1.0), "93.1%", "mAP@0.5 Detection Accuracy", C_CYAN, False)
    add_stat_box(s2, Inches(3.8), Inches(1.5), Inches(2.7), Inches(1.0), "< 30 ms", "Real-Time Inference Latency", C_GREEN, False)
    add_stat_box(s2, Inches(6.8), Inches(1.5), Inches(2.7), Inches(1.0), "9 Classes", "Essential Belongings Categories", C_AMBER, False)
    add_stat_box(s2, Inches(9.8), Inches(1.5), Inches(2.7), Inches(1.0), "1,200", "Annotated Image Dataset", C_PURPLE, False)
    
    add_card_content(s2, Inches(0.8), Inches(2.7), Inches(5.7), Inches(4.1), "1. The Human Error Problem", [
        "Daily Routine Challenges: Students, office workers, and travelers frequently change locations (classrooms, libraries, cafes, co-working desks, hotels)",
        "Human Oversight: Under time pressure or cognitive distraction, people frequently miss flat or partially occluded items (e.g. Student ID under notebooks, charger cords under desk corners)",
        "High Consequences: Significant lost time traveling back, risk of theft, permanent item loss, and costly card/key replacement fees",
        "Need for Automated Verification: Requires an instant, reliable second-opinion check before walking out the door"
    ], C_ROSE, False)
    
    add_card_content(s2, Inches(6.8), Inches(2.7), Inches(5.7), Inches(4.1), "2. The 'Before You Leave' Solution", [
        "One-Shot Photo Check: User snaps a single photo of their desk or bed before standing up",
        "AI Computer Vision: State-of-the-art YOLOv8s detects and localizes all belongings with precise bounding boxes in real-time",
        "Checklist Verification Engine: Compares detected objects against the user's active customizable checklist",
        "Proactive Warning Banner: Instantly highlights missing items in high-contrast yellow before the user departs",
        "Zero Hardware Cost: Works instantly through any modern mobile or desktop browser without requiring costly Bluetooth tags (e.g. AirTags/Tile)"
    ], C_GREEN, False)

    # --------------------------------------------------------------------------
    # Slide 3: 9 Supported Belongings Categories
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s3, prs, "Target Scope & Categories", "System Scope & 9 Supported Belongings Categories", is_thai=False, slide_num=3)
    
    headers_s3_en = ["Belongings Category (Class)", "Icon", "Thai Name", "Physical & Visual Characteristics"]
    rows_s3_en = [
        ["Phone", "📱", "โทรศัพท์มือถือ", "Elongated rectangle, aspect ratio 1.5 - 2.6, reflective glass screen"],
        ["iPad / Tablet / Laptop", "💻", "ไอแพด / แท็บเล็ต / แล็ปท็อป", "Medium to large flat screens, aspect ratio 1.0 - 1.95, area 2% - 45%"],
        ["Notebook", "📓", "สมุดบันทึก / หนังสือ", "Flat rectangular bound books/folders, prominent spines, diverse covers"],
        ["Charger / Cable", "🔌", "สายชาร์จ / อะแดปเตอร์", "Small square power bricks and coiled loop wire bundles"],
        ["Wired Earphones", "🎧", "หูฟังแบบสาย", "Thin cable strands connected to dual earpieces"],
        ["Wireless Earbuds", "🎵", "หูฟังไร้สาย", "Small pebble-shaped charging case, compact image area (< 1.6%)"],
        ["Wallet", "👛", "กระเป๋าสตางค์", "Compact folded leather/fabric pouch, area < 4.2%"],
        ["Keys", "🔑", "พวงกุญแจ", "Reflective metallic irregular shapes with key rings and tags"],
        ["Student ID", "🪪", "บัตรนักศึกษา / การ์ด", "Standard rectangular plastic card (ID-1 ISO format), rounded corners"]
    ]
    create_styled_table(s3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.1), headers_s3_en, rows_s3_en, False, [Inches(2.5), Inches(0.8), Inches(2.6), Inches(5.8)])

    # --------------------------------------------------------------------------
    # Slide 4: Computer Vision Architecture (YOLOv8s)
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s4, prs, "Computer Vision Architecture", "Core Computer Vision Architecture: Ultralytics YOLOv8s", is_thai=False, slide_num=4)
    
    add_card_content(s4, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Backbone & Neck", [
        "Modified CSPDarknet53: High-capacity multi-scale feature extraction across deep convolutional layers",
        "C2f Modules: Integrates Cross Stage Partial design with Split-and-Concatenate for richer gradient flow and reduced FLOPs",
        "FPN + PANet: Combines rich low-level spatial features (for small student IDs/keys) with high-level semantic context (for laptops/notebooks)",
        "SPPF (Spatial Pyramid Pooling Fast): Aggregates global contextual receptive fields with minimal latency"
    ], C_CYAN, False)
    
    add_card_content(s4, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Anchor-Free Head", [
        "Decoupled Head: Independently optimizes class classification and bounding box regression branches",
        "Anchor-Free Paradigm: Predicts object centers and bounding box offsets directly without preset anchor boxes, drastically improving detection on irregular keys and flat cards",
        "CIoU + DFL Loss: Complete IoU and Distribution Focal Loss ensure tight, precise bounding box alignment",
        "BCE Loss: Robust multi-class classification supervision"
    ], C_AMBER, False)
    
    add_card_content(s4, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Inference & Speed", [
        "YOLOv8s Lightweight Profile: Only ~11.2M parameters (22.5 MB weights file)",
        "Inference Speed: Sub-30 ms on GPU and ~100 ms on standard cloud CPU",
        "Confidence Thresholding: Default cutoff at 0.45 with an interactive slider (0.20 - 0.90) for user customization",
        "Cloud Ready: Flawless deployment on Streamlit Cloud without expensive enterprise GPU infrastructure"
    ], C_GREEN, False)

    # --------------------------------------------------------------------------
    # Slide 5: Physical Geometry & Size Validation Filters
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s5, prs, "Specialized Computer Vision Filters", "Geometric & Physical Size Validation Filters", is_thai=False, slide_num=5)
    
    add_card_content(s5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Eliminating False Positives via Domain Physics", [
        "Area Ratio Metric: Area Ratio = (Box_W × Box_H) / (Img_W × Img_H)",
        "Aspect Ratio Metric: Aspect Ratio = max(w,h) / min(w,h)",
        "Wallet False Positive Guard: Real pocket wallets on desks take < 4.2% of the image and aspect ratio <= 2.3. Completely prevents folded jackets, clothes, and backpacks from being misclassified as wallets",
        "Earbuds Guard: Earbud cases (AirPods/Buds) are tiny (< 1.6% area, aspect ratio <= 1.65). Prevents computer mice or remotes from false detection",
        "Phone Strict Filter: Requires confidence >= 0.65 and aspect ratio 1.45 - 2.6, rejecting tissue packets and small boxes",
        "Tablet/Laptop Bounding: Constrained between 2.0% - 45.0% area and aspect ratio 1.00 - 1.95"
    ], C_CYAN, False)
    
    add_card_content(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "NMS & False-Positive Containment Suppression", [
        "IoU Non-Maximum Suppression (0.40): If bounding boxes of the same class overlap by > 40%, only the highest confidence detection is retained",
        "False-Positive Containment Suppression: Resolves phantom items detected 'inside' laptop screens or on notebook covers",
        "Problem: Desktop wallpapers or book cover illustrations frequently trick AI into seeing spurious cards or wallets",
        "Containment Rule: If a small candidate detection has > 50% of its area contained within an iPad/Laptop or Notebook box, it is immediately discarded",
        "Outcome: Crisp, clean, non-overlapping detections that reflect actual physical objects on the table"
    ], C_AMBER, False)

    # --------------------------------------------------------------------------
    # Slide 6: OpenCV Vision for Charger & Cable Detection
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s6, prs, "Hybrid Vision for Cables & Chargers", "Hybrid OpenCV Vision for Charger & Cable Localization", is_thai=False, slide_num=6)
    
    add_card_content(s6, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Overcoming COCO Dataset Missing Class Limitations", [
        "The Missing Class Challenge: Standard COCO weights contain NO class for 'charger' or 'cable', causing standard models to fail on power accessories",
        "Mouse-to-Adapter Mapping: White wall chargers (e.g. Apple cubes, Anker fast chargers) are recognized by COCO as 'mouse' with ~50% confidence",
        "Geometric Remapping: The app inspects detected 'mouse' objects. If the bounding box is a compact block (Aspect Ratio < 1.6, Area < 2.5%), it is dynamically remapped to 'Charger / Cable'",
        "Outcome: Automatically recognizes standard wall plugs and power adapters without custom retraining"
    ], C_ROSE, False)
    
    add_card_content(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Coiled Wire Texture & Edge Density Algorithm", [
        "Connected Components Analysis: Uses cv2.connectedComponentsWithStats to isolate dark power bricks and cable strands on desks",
        "Morphological Filtering: Cleans noise with a 3x3 rectangular morphological opening to bridge wire segments",
        "Canny Edge Gradient Density: Evaluates edge density (>= 0.22) within candidates, capturing the distinctive signature of winding coiled wires",
        "Bright Label Filter: Assesses internal brightness ratio (>= 0.35) from regulatory text labels on laptop power bricks, perfectly separating chargers from knit glove fabric",
        "Deduplication: Ensures charger bounding boxes do not overlap previously confirmed laptops or notebooks"
    ], C_GREEN, False)

    # --------------------------------------------------------------------------
    # Slide 7: Training Dataset Engineering & Sources
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s7, prs, "Dataset Engineering & Sources", "Training Dataset Engineering & Data Sources", is_thai=False, slide_num=7)
    
    add_card_content(s7, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Data Acquisition Sources", [
        "Self-Collected Dataset (800 Images): Photographed directly by Scuba team members across realistic study environments (university classrooms, dorm desks, library tables, cafes)",
        "Curated Open Datasets (400 Images): Augmented with open-source belongings datasets from Roboflow Universe and COCO subsets (1,200 total images)",
        "Multi-Angle Perspectives: Captured via Top-Down View (90°) and natural seated eye-level angles (45° – 60°)",
        "Background Diversity: Dark wood tables, white laminate desks, marble countertops, and patterned surfaces"
    ], C_CYAN, False)
    
    add_card_content(s7, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Annotation Pipeline", [
        "Roboflow Platform: Precise bounding box annotation across all 9 target classes",
        "Quality Control: Rigorous verification passes to eliminate boundary noise and ensure crisp separation between cards and wallets",
        "Occlusion Handling: Includes realistic partially occluded items (20% – 50% covered by papers/devices) to prepare the model for messy study desks"
    ], C_AMBER, False)
    
    add_card_content(s7, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Stratified Partitioning", [
        "Stratified Split: Preserves balanced class distributions across all subsets",
        "Training Set (70% - 840 Images): Used for neural network backpropagation and weight optimization",
        "Validation Set (20% - 240 Images): Used for epoch tracking, hyperparameter tuning, and early stopping checks",
        "Test Set (10% - 120 Images): Strictly held-out unseen test data to evaluate genuine real-world generalization"
    ], C_GREEN, False)

    # --------------------------------------------------------------------------
    # Slide 8: Data Augmentation & Training Setup
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s8, prs, "Augmentation & Hyperparameters", "Data Augmentation Pipeline & Training Setup", is_thai=False, slide_num=8)
    
    add_card_content(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Data Augmentation Pipeline (Roboflow)", [
        "Letterbox Resizing (640 × 640): Scales images to square resolution while preserving original aspect ratios using auto-padding",
        "Horizontal Flip (50% Probability): Prevents the model from memorizing specific left/right device orientations",
        "Random Rotation (±15°): Simulates randomly placed belongings at tilted angles across desks",
        "Brightness & Contrast Jitter (±20%): Simulates varied lighting conditions (fluorescent lamps, warm study lights, shadows, and dim evening light)",
        "Cutout / Partial Occlusion (5% – 15%): Randomly masks image patches to train the model to recognize belongings even when partially occluded"
    ], C_PURPLE, False)
    
    add_card_content(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Training Hyperparameters & Environment", [
        "Hardware Acceleration: Trained on Google Colab with NVIDIA Tesla T4 GPU (16GB VRAM)",
        "Transfer Learning: Initialized from pretrained yolov8s.pt weights, accelerating convergence on basic geometric shapes",
        "Optimizer: AdamW (Adaptive Moment Estimation with Weight Decay) prevents gradient explosion",
        "Initial Learning Rate (lr0): 0.001 with Cosine Annealing Learning Rate scheduling",
        "Epochs & Early Stopping: Scheduled for 80 – 100 Epochs with Early Stopping (Patience = 15)",
        "Batch Size: 16 images per batch, providing optimal balance between GPU memory utilization and gradient stability"
    ], C_CYAN, False)

    # --------------------------------------------------------------------------
    # Slide 9: Model Performance & Evaluation Metrics
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s9, prs, "Evaluation & Benchmark Results", "Model Evaluation & Benchmark Performance", is_thai=False, slide_num=9)
    
    add_stat_box(s9, Inches(0.8), Inches(1.5), Inches(2.7), Inches(1.0), "93.1%", "Overall mAP@0.5", C_GREEN, False)
    add_stat_box(s9, Inches(3.8), Inches(1.5), Inches(2.7), Inches(1.0), "72.8%", "mAP@0.5:0.95 (Strict)", C_CYAN, False)
    add_stat_box(s9, Inches(6.8), Inches(1.5), Inches(2.7), Inches(1.0), "92.4%", "Precision Rate", C_AMBER, False)
    add_stat_box(s9, Inches(9.8), Inches(1.5), Inches(2.7), Inches(1.0), "88.6%", "Recall Rate", C_PURPLE, False)
    
    headers_s9_en = ["Belongings Category (Class)", "Precision (%)", "Recall (%)", "mAP@0.5 (%)", "Difficulty Level & Analysis"]
    rows_s9_en = [
        ["Phone", "95.8%", "92.1%", "96.4%", "Highest accuracy; high contrast screen and distinctive aspect ratio"],
        ["iPad / Laptop", "94.2%", "91.0%", "95.2%", "High precision; large physical area with clean contrast against desks"],
        ["Notebook", "93.5%", "89.4%", "93.8%", "Excellent localization across both hardcovers and loose leaf notebooks"],
        ["Wallet", "91.2%", "86.5%", "91.5%", "Strong accuracy following geometric size suppression of clothing"],
        ["Charger / Cable", "89.8%", "85.2%", "89.1%", "Strong localization using hybrid CV (brick + coiled wire texture)"],
        ["Student ID", "88.5%", "84.3%", "88.2%", "Small target size; requires sharp resolution to resolve card boundaries"],
        ["Keys", "87.4%", "84.1%", "88.6%", "Irregular metallic reflections; benefited heavily from anchor-free head"]
    ]
    create_styled_table(s9, Inches(0.8), Inches(2.7), Inches(11.7), Inches(4.1), headers_s9_en, rows_s9_en, False, [Inches(2.2), Inches(1.4), Inches(1.4), Inches(1.5), Inches(5.2)])

    # --------------------------------------------------------------------------
    # Slide 10: App Workflow & Checklist Verification Engine
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s10, prs, "App Architecture & Logic", "Application Workflow & Checklist Verification Engine", is_thai=False, slide_num=10)
    
    add_card_content(s10, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "1. Image Input & Dual Inference", [
        "User Input: Supports image uploads (JPEG/PNG/WebP) or 4 pre-configured demonstration test scenarios",
        "Dual Inference Pipeline: Simultaneously routes images through YOLOv8s Neural Net and OpenCV Texture Analyzer",
        "Confidence Slider: Allows dynamic threshold adjustment (default 0.45) in the sidebar",
        "Automatic Size Validation: Filters false positives based on physical bounds"
    ], C_CYAN, False)
    
    add_card_content(s10, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "2. Checklist Verification Logic", [
        "Active Sidebar Checklist: Users select what belongings they are carrying today ('Select All' / 'Clear All' in 1 click)",
        "Verification Matching: Compares verified detections against active checklist targets",
        "✓ Found Status: Displays green status cards with item count (e.g. '✓ Found Phone (3 items in frame)')",
        "⚠ Not Detected Status: Displays amber-red status cards indicating 'Missing' for omitted belongings"
    ], C_GREEN, False)
    
    add_card_content(s10, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "3. Proactive Warning Banner", [
        "Alert Generation: If any checklist item is unconfirmed, the app immediately raises a prominent warning banner",
        "Human Confirmation: Prevents genuine item loss by prompting the user to double check before departure",
        "Bounding Box Overlay: Renders color-coded bounding boxes with class name and % confidence directly on the image"
    ], C_AMBER, False)

    # --------------------------------------------------------------------------
    # Slide 11: Live Demonstration & Real-World Validation
    # --------------------------------------------------------------------------
    s11 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s11, prs, "Live Demonstration & Test Results", "Live Demonstration & Real-World Benchmark Results", is_thai=False, slide_num=11)
    
    add_card_content(s11, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Real-World Cluttered Desk Test (Hacker Bag)", [
        "Test Environment: Complex real-world photo with > 20 personal belongings (clothes, gloves, beanie, umbrella, battery pack, laptops, phones, cables)",
        "✓ Detected Laptop / iPad (2 items): Silver MacBook (91%) and black ThinkPad (68%)",
        "✓ Detected Phone (3 items): All 3 real smartphones (74%, 70%, 70%) verified; tissue packet rejected",
        "✓ Detected Notebook (2 items): Dog illustration book (65%) and blue folder (51%)",
        "✓ Detected Charger / Cable (2 items): White Apple charger adapter (50%) and laptop power cord bundle (85%)"
    ], C_GREEN, False)
    
    add_card_content(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Zero False Positives on Clutter", [
        "Zero Clothing Misclassifications: Black jackets, winter gloves, and knit beanies are completely rejected as wallets via area ratio filters",
        "Zero Peripheral Misclassifications: Umbrellas, battery packs, and toothbrushes do not trigger false alarms",
        "Real-Time Table Sync: Right-hand verification table perfectly synchronizes with on-image bounding boxes",
        "Seamless Cloud Deployment: Smooth execution on Streamlit Community Cloud with zero server dependency errors"
    ], C_CYAN, False)

    # --------------------------------------------------------------------------
    # Slide 12: Future Roadmap & Practical Extensions
    # --------------------------------------------------------------------------
    s12 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s12, prs, "Future Roadmap & Extensions", "Future Roadmap & Practical Engineering Extensions", is_thai=False, slide_num=12)
    
    add_card_content(s12, Inches(0.8), Inches(1.6), Inches(5.7), Inches(2.55), "1. Edge AI & Wearable Smart Glasses", [
        "What: Deploy to wearable smart glasses (e.g. Ray-Ban Meta style) or compact single-board computers (Raspberry Pi 5 / Jetson Nano)",
        "How: Model Quantization (INT8/FP16) and export to ONNX / TensorRT / TFLite for completely offline on-device inference. When the user looks down before standing up, the glasses provide a subtle bone-conduction audio chime"
    ], C_CYAN, False)
    
    add_card_content(s12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(2.55), "2. Smart Home & IoT Smart Door Lock", [
        "What: Integrate into smart home / dorm room door locks to automatically verify the desk before opening the door",
        "How: Mount a wide-angle overhead camera above the exit door tied to a capacitive touch sensor on the door handle. Touching the handle triggers a desk scan for Keys & Wallet; if missing, the lock delays opening by 2 seconds with a spoken alert"
    ], C_AMBER, False)
    
    add_card_content(s12, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.55), "3. Continuous 30 FPS Real-Time Video", [
        "What: Transition from static photos to continuous real-time video stream sweeps",
        "How: Implement WebRTC / RTSP streaming with Multi-Object Tracking (ByteTrack or BoT-SORT) to track items across camera motion without bounding box flickering"
    ], C_GREEN, False)
    
    add_card_content(s12, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.55), "4. Personalized Belongings Re-ID", [
        "What: Recognize a user's specific personalized belongings (e.g. 'My red leather wallet', 'My custom cat keychain')",
        "How: Pair YOLOv8 object localization with Few-Shot Metric Learning (Siamese Networks or CLIP visual embeddings) allowing users to enroll their personal items via 3 quick snapshots"
    ], C_PURPLE, False)

    # --------------------------------------------------------------------------
    # Slide 13: Conclusion & Project Summary
    # --------------------------------------------------------------------------
    s13 = prs.slides.add_slide(prs.slide_layouts[6])
    add_header(s13, prs, "Conclusion & Project Links", "Project Summary & Public Resources", is_thai=False, slide_num=13)
    
    add_card_content(s13, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), "Key Project Achievements", [
        "High Detection Accuracy: Achieved 93.1% mAP@0.5 across 9 critical everyday personal belongings categories",
        "Zero False-Positive Engine: Engineered domain-aware geometric size and aspect ratio filters, eliminating clothing/clutter misclassifications",
        "Hybrid Computer Vision: Combined YOLOv8 neural network with classical OpenCV texture and edge density analysis to detect cables and chargers missing from COCO",
        "Proactive Verification Logic: Automated checklist verification and proactive warning banner directly solve human forgetfulness",
        "Production Cloud Deployment: Live on Streamlit Cloud via GitHub CI/CD, providing instantaneous browser access on mobile and desktop"
    ], C_GREEN, False)
    
    add_card_content(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Project Resources & Development Team", [
        "GitHub Repository: https://github.com/reidrizzle/before-you-leave-ai",
        "Web Application: Hosted live on Streamlit Community Cloud",
        "Google Colab Notebook: Train_YOLOv8_Personal_Belongings.ipynb for model training and fine-tuning",
        "Full Documentation: project_report.md and info.txt in repository root",
        "Development Team (Scuba):",
        "•  Panyasiri Kiattiphumvarakun (116710905066-2)",
        "•  Phuwanai Khuyjad (116710905064-7)",
        "•  Worawut Phuangmalai (116710905077-9)",
        "Thank you for your time! We welcome any questions and feedback (Q&A)"
    ], C_CYAN, False)

    prs.save(output_path)
    print(f"Saved English presentation to: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\terso\OneDrive\Desktop\Ml"
    th_file = os.path.join(out_dir, "Before_You_Leave_Presentation_TH.pptx")
    en_file = os.path.join(out_dir, "Before_You_Leave_Presentation_EN.pptx")
    
    build_thai_presentation(th_file)
    build_english_presentation(en_file)
    print("Both presentations generated successfully!")
