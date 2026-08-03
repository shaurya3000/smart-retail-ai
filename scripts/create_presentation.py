import os
import sys
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "screenshots")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_high_res_screenshots():
    """Generates crisp high-resolution UI screenshots for presentation slides."""
    
    # 1. Executive Intelligence Dashboard UI
    img1 = Image.new('RGB', (1600, 900), color='#0e1117')
    draw = ImageDraw.Draw(img1)
    draw.rectangle([50, 40, 1550, 110], fill='#1e293b', outline='#334155', width=3)
    draw.text((80, 60), "📊 Executive Retail Intelligence & System Analytics", fill='#38bdf8')
    
    metrics = [("98", "TOTAL STORE VISITS"), ("5", "REGISTERED CUSTOMERS"), ("45", "CHATBOT QUERIES"), ("HEALTHY", "PIPELINE STATUS")]
    x = 50
    for val, lbl in metrics:
        draw.rectangle([x, 140, x + 350, 270], fill='#1e293b', outline='#38bdf8', width=3)
        draw.text((x + 30, 165), val, fill='#38bdf8')
        draw.text((x + 30, 220), lbl, fill='#94a3b8')
        x += 380
        
    draw.rectangle([50, 310, 770, 840], fill='#1e293b', outline='#94a3b8', width=2)
    draw.text((80, 340), "Customer Feedback Sentiment Distribution", fill='#f8fafc')
    draw.rectangle([120, 750, 250, 810], fill='#38bdf8')
    draw.rectangle([320, 650, 450, 810], fill='#38bdf8')
    draw.rectangle([520, 420, 650, 810], fill='#38bdf8')

    draw.rectangle([820, 310, 1550, 840], fill='#1e293b', outline='#94a3b8', width=2)
    draw.text((850, 340), "Top Chatbot FAQ Inquiries", fill='#f8fafc')
    draw.text((850, 400), "0  order_status            21\n1  return_policy           12\n2  store_hours              9\n3  shipping_costs           7\n4  payment_methods          5", fill='#34d399')
    img1.save(os.path.join(ASSETS_DIR, "executive_dashboard.png"))

    # 2. Chatbot Assistant UI
    img2 = Image.new('RGB', (1600, 900), color='#0e1117')
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([50, 40, 1550, 110], fill='#1e293b', outline='#334155', width=3)
    draw2.text((80, 60), "🤖 AI Retail Customer Support Assistant", fill='#c084fc')
    
    draw2.rectangle([50, 150, 1550, 270], fill='#1e293b', outline='#64748b', width=2)
    draw2.text((90, 180), "🤖 Hello! I am your AI Smart Retail Assistant. How can I help you today with orders, returns...?", fill='#f8fafc')
    
    draw2.rectangle([50, 310, 1550, 420], fill='#1e293b', outline='#ef4444', width=3)
    draw2.text((90, 340), "👤 Where is my order?", fill='#f8fafc')
    
    draw2.rectangle([50, 460, 1550, 630], fill='#1e293b', outline='#34d399', width=3)
    draw2.text((90, 490), "🤖 You can track your order status in real time under 'My Orders' portal or by entering your 8-digit Order Number.", fill='#f8fafc')
    draw2.text((90, 560), "Strategy: Rule-Based FAQ Match | Intent: order_status | Confidence: 99%", fill='#34d399')
    img2.save(os.path.join(ASSETS_DIR, "chatbot_assistant.png"))

    # 3. Face Recognition UI
    img3 = Image.new('RGB', (1600, 900), color='#0e1117')
    draw3 = ImageDraw.Draw(img3)
    draw3.rectangle([50, 40, 1550, 110], fill='#1e293b', outline='#334155', width=3)
    draw3.text((80, 60), "👤 Customer Recognition & Visit Logger", fill='#c084fc')
    
    draw3.rectangle([50, 150, 1550, 240], fill='#064e3b', outline='#10b981', width=3)
    draw3.text((90, 180), "🎉 Welcome back, Bob Johnson! (Platinum Loyalty Member)", fill='#34d399')
    
    draw3.rectangle([50, 270, 1550, 840], fill='#1e293b', outline='#334155', width=2)
    draw3.text((90, 310), """{\n  "Status" : "recognized",\n  "Customer ID" : "CUST_1002",\n  "Name" : "Bob Johnson",\n  "Loyalty Tier" : "Platinum",\n  "Recognition Confidence" : "70.0%",\n  "Total Store Visits" : 37,\n  "Last Visit Timestamp" : "2026-08-03 21:29:01",\n  "Biometric Consent Granted" : true\n}""", fill='#38bdf8')
    img3.save(os.path.join(ASSETS_DIR, "face_recognition.png"))

    # 4. Sentiment Engine UI
    img4 = Image.new('RGB', (1600, 900), color='#0e1117')
    draw4 = ImageDraw.Draw(img4)
    draw4.rectangle([50, 40, 1550, 110], fill='#1e293b', outline='#334155', width=3)
    draw4.text((80, 60), "💬 Customer Feedback & Review NLP Sentiment Engine", fill='#34d399')
    
    draw4.rectangle([50, 150, 780, 340], fill='#064e3b', outline='#10b981', width=3)
    draw4.text((90, 190), "Sentiment: POSITIVE 😄\n\nConfidence Score: 88.2%", fill='#f8fafc')
    
    draw4.rectangle([830, 150, 1550, 340], fill='#1e293b', outline='#64748b', width=2)
    draw4.text((850, 190), "NLP Preprocessing Pipeline:\nRaw Input: 'The quality of this leather jacket is exceptional...'\nCleaned Tokens: 'quality leather jacket exceptional super...'", fill='#34d399')
    img4.save(os.path.join(ASSETS_DIR, "sentiment_analysis_2.png"))

    print(f"Generated high-resolution UI images in {ASSETS_DIR}")

def build_presentation():
    generate_high_res_screenshots()
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    BG_COLOR = RGBColor(15, 23, 42)
    TEXT_PRIMARY = RGBColor(248, 250, 252)
    ACCENT_BLUE = RGBColor(56, 189, 248)
    ACCENT_PURPLE = RGBColor(192, 132, 252)

    def set_slide_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_slide_header(slide, title):
        tx = slide.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12.0), Inches(0.6))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s1)
    tx = s1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(2.0))
    tf = tx.text_frame
    p = tf.paragraphs[0]
    p.text = "Smart Retail & Customer Intelligence Platform"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "Live Application Demonstration Deck with Embedded High-Resolution UI Screenshots"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_PURPLE

    # Slide 2: Face Recognition (Pasting Picture)
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s2)
    add_slide_header(s2, "Module A: Biometric Face Recognition & Customer Visit Logger")
    img_path2 = os.path.join(ASSETS_DIR, "face_recognition.png")
    s2.shapes.add_picture(img_path2, Inches(0.6), Inches(1.1), Inches(12.13), Inches(6.0))

    # Slide 3: Sentiment Engine (Pasting Picture)
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s3)
    add_slide_header(s3, "Module B: Customer Feedback Sentiment Analysis NLP Engine")
    img_path3 = os.path.join(ASSETS_DIR, "sentiment_analysis_2.png")
    s3.shapes.add_picture(img_path3, Inches(0.6), Inches(1.1), Inches(12.13), Inches(6.0))

    # Slide 4: Chatbot Assistant (Pasting Picture)
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s4)
    add_slide_header(s4, "Module B: AI Retail Customer Support Assistant")
    img_path4 = os.path.join(ASSETS_DIR, "chatbot_assistant.png")
    s4.shapes.add_picture(img_path4, Inches(0.6), Inches(1.1), Inches(12.13), Inches(6.0))

    # Slide 5: Executive Analytics Dashboard (Pasting Picture)
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_bg(s5)
    add_slide_header(s5, "Module C: Executive Retail Intelligence Telemetry Dashboard")
    img_path5 = os.path.join(ASSETS_DIR, "executive_dashboard.png")
    s5.shapes.add_picture(img_path5, Inches(0.6), Inches(1.1), Inches(12.13), Inches(6.0))

    out_path = os.path.join(BASE_DIR, "Smart_Retail_Platform_Demo_Presentation.pptx")
    prs.save(out_path)
    print(f"SUCCESS: Created presentation with embedded picture shapes at {out_path}")

if __name__ == "__main__":
    build_presentation()
