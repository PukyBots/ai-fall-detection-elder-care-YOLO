from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train-2/weights/best.pt")

# Run detection
results = model.predict(
    source="videos/f3.mp4",
    conf=0.40,
    save=True
)

print("Detection completed.")