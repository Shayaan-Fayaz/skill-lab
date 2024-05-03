import json

import cv2
from ultralytics import YOLO
import math
import requests

post_url = "http://192.168.94.174/detection"

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

model = YOLO("C:/Users/Mohammed Shayaan/Desktop/cool_stuffs/obj/runs/detect/train8/weights/best.pt")

# Read the image
img = cv2.VideoCapture(0)
img.set(3, 1280)
img.set(4, 720)
classNames = ["Headphones"]


while True:
    ret, frame = img.read()
    # gra
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    results = model(source=frame, stream=True)

    for result in results:
        boxes = result.boxes
        # print(boxes)
        headphone_count = len(boxes)

        cv2.putText(frame, f"Count{headphone_count}", (50,50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
        classes = set()
        for box in boxes:
            # print(box)
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



                # response = requests.post(post_url)
        classList = list(classes)
        data = {"classes": classList, "count": headphone_count}
        data = json.dumps(data)
        response = requests.post(post_url, json=data)
        print(response.status_code)

    cv2.imshow('Image', frame)
    cv2.waitKey(200)
# Convert the image to grayscale

# Detect faces

# Draw bounding boxes around the detected faces


# Display the result

# cv2.destroyAllWindows()
