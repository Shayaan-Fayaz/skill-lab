import json
import cv2
from ultralytics import YOLO
import math
import requests

post_url = "http://192.168.245.174/detection"
headers = {'Content-Type': 'application/json'}


# the below is for the testing of api
esp32_ip = "192.168.245.174"
esp32_port = 80

# Define the URL for the detection endpoint
url = f"http://{esp32_ip}:{esp32_port}/detect"

# Define the JSON payload

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

model = YOLO("C:/Users/Mohammed Shayaan/Desktop/cool_stuffs/obj/runs/detect/train8/weights/best.pt")


img = cv2.VideoCapture(0)
img.set(3, 1280)
img.set(4, 720)
classNames = ["Headphones"]


while True:
    ret, frame = img.read()

    results = model(source=frame, stream=True)

    for result in results:
        boxes = result.boxes

        headphone_count = len(boxes)

        cv2.putText(frame, f"Count{headphone_count}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255))
        classes = set()
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            conf = math.ceil((box.conf[0] * 100)) / 100
            # class name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "Headphones":
                classes.add(currentClass)
            # assert isinstance(boxes.length, object)
                cv2.putText(frame, currentClass, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (0, 0, 255), 2)  # print(x1, y1)
        print(list(classes))
        payload = {
            "classes": list(classes),
            "count": headphone_count
        }

        # Convert payload to JSON string
        payload_json = json.dumps(payload)

        response = requests.post(url, data=payload_json, headers=headers)
        print("Response:")
        print(response.status_code)
        print(response.text)

    cv2.imshow('Image', frame)
    cv2.waitKey(200)