import cv2
from ultralytics import YOLO
import requests

model = YOLO("runs/detect/train-2/weights/best.pt")

cap = cv2.VideoCapture(0)

NTFY_TOPIC = "pulkit-fall-alert"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

# Prevent sending notification on every frame
fall_alert_sent = False

def send_ntfy(message):
    try:
        response = requests.post(
            NTFY_URL,
            data=message.encode("utf-8"),
            headers={
                "Title": "Fall Detected",
                "Priority": "high",
                "Tags": "warning",
            },
            timeout=10
        )

        if response.status_code == 200:
            print("ntfy notification sent")
        else:
            print("ntfy error:", response.status_code)

    except Exception as e:
        print("ntfy connection failed:", e)


while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        frame,
        conf=0.80,
        verbose=False
    )

    annotated_frame = results[0].plot()

    detected_fall = False

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        class_name = model.names[class_id]

        print(class_name)

        if class_name.lower() == "fall-detected":
            detected_fall = True

    # -----------------------------
    # Send ntfy notification
    # -----------------------------
    if detected_fall and not fall_alert_sent:

        send_ntfy(
            "Fall detected by the camera. "
            "Please check the person immediately."
        )

        fall_alert_sent = True

    # Reset after fall disappears
    if not detected_fall:
        fall_alert_sent = False

    cv2.imshow(
            "Fall Detection",
            annotated_frame
        )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()



    