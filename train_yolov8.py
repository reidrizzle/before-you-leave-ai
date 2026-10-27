"""
Before You Leave: AI-Powered Personal Belongings Detection System
YOLOv8 Custom Model Training Script
Group: Scuba

This script trains/fine-tunes YOLOv8 specifically on the 9 personal belongings classes.
Can be executed locally with GPU or on Google Colab.
"""

import os
from ultralytics import YOLO

# 1. Define the 9 target classes
CLASSES = [
    "Phone",
    "iPad_Tablet",
    "Notebook",
    "Charger_Cable",
    "Wired_Earphones",
    "Wireless_Earbuds",
    "Wallet",
    "Keys",
    "Student_ID"
]

# 2. Generate data.yaml configuration
yaml_content = f"""
# Before You Leave - Dataset Configuration
path: ./dataset  # dataset root dir
train: images/train  # train images (relative to 'path')
val: images/val      # val images (relative to 'path')
test: images/test    # test images (optional)

# Classes
names:
  0: Phone
  1: iPad_Tablet
  2: Notebook
  3: Charger_Cable
  4: Wired_Earphones
  5: Wireless_Earbuds
  6: Wallet
  7: Keys
  8: Student_ID
"""

def create_yaml():
    with open("dataset.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_content.strip())
    print("Created dataset.yaml successfully!")

def train():
    create_yaml()
    print("Initializing YOLOv8s pretrained weights...")
    model = YOLO("yolov8s.pt")  # Starting from COCO pretrained weights
    
    print("Starting training on custom personal belongings dataset...")
    results = model.train(
        data="dataset.yaml",
        epochs=80,
        imgsz=640,
        batch=16,
        patience=15,
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.01,
        weight_decay=0.0005,
        augment=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=15.0,
        translate=0.1,
        scale=0.5,
        fliplr=0.5,
        mosaic=1.0,
        project="runs/train",
        name="before_you_leave_yolov8s",
        exist_ok=True
    )
    
    print("\nTraining completed!")
    print("Best weights saved at: runs/train/before_you_leave_yolov8s/weights/best.pt")
    
    # Evaluate on validation/test set
    print("\nEvaluating model metrics...")
    metrics = model.val()
    print(f"mAP@0.5: {metrics.box.map50:.4f}")
    print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")

if __name__ == "__main__":
    train()
