from ultralytics import YOLO
import cv2
import math
import requests
import json

model = YOLO("yolov8m.pt")

video = cv2.VideoCapture(0)
video.set(3, 1280)
video.set(4, 720)


# the below is for the testing of api
esp32_ip = "192.168.245.174"
esp32_port = 80

# Define the URL for the detection endpoint
url = f"http://{esp32_ip}:{esp32_port}/detect"
headers = {'Content-Type': 'application/json'}

classNames = {0: 'person',
              1: 'bicycle',
              2: 'car',
              3: 'motorcycle',
              4: 'airplane',
              5: 'bus',
              6: 'train',
              7: 'truck',
              8: 'boat',
              9: 'traffic light',
              10: 'fire hydrant',
              11: 'stop sign',
              12: 'parking meter',
              13: 'bench',
              14: 'bird',
              15: 'cat',
              16: 'dog',
              17: 'horse',
              18: 'sheep',
              19: 'cow',
              20: 'elephant',
              21: 'bear',
              22: 'zebra',
              23: 'giraffe',
              24: 'backpack',
              25: 'umbrella',
              26: 'handbag',
              27: 'tie',
              28: 'suitcase',
              29: 'frisbee',
              30: 'skis',
              31: 'snowboard',
              32: 'sports ball',
              33: 'kite',
              34: 'baseball bat',
              35: 'baseball glove',
              36: 'skateboard',
              37: 'surfboard',
              38: 'tennis racket',
              39: 'bottle',
              40: 'wine glass',
              41: 'cup',
              42: 'fork',
              43: 'knife',
              44: 'spoon',
              45: 'bowl',
              46: 'banana',
              47: 'apple',
              48: 'sandwich',
              49: 'orange',
              50: 'broccoli',
              51: 'carrot',
              52: 'hot dog',
              53: 'pizza',
              54: 'donut',
              55: 'cake',
              56: 'chair',
              57: 'couch',
              58: 'potted plant',
              59: 'bed',
              60: 'dining table',
              61: 'toilet',
              62: 'tv',
              63: 'laptop',
              64: 'mouse',
              65: 'remote',
              66: 'keyboard',
              67: 'cell phone',
              68: 'microwave',
              69: 'oven',
              70: 'toaster',
              71: 'sink',
              72: 'refrigerator',
              73: 'book',
              74: 'clock',
              75: 'vase',
              76: 'scissors',
              77: 'teddy bear',
              78: 'hair drier',
              79: 'toothbrush'}

while True:
    ret, frame = video.read()
    results = model(source=frame)

    for result in results:
        boxes = result.boxes
        obj_count = 0
        cat_count = 0
        dog_count = 0
        cow_count = 0
        classes = set()
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            conf = math.ceil((box.conf[0] * 100)) / 100

            cls = int(box.cls[0])
            currentClass = classNames[cls]
            # print(cls)
            # print(currentClass)

            if currentClass == "dog" or currentClass == "cat" or currentClass == "cow":
                classes.add(currentClass)
                obj_count = obj_count + 1
                # classes.add(currentClass)
                # if currentClass == "dog":
                #     dog_count += 1
                # if currentClass == "cat":
                #     cat_count += 1
                # if currentClass == "cow":
                #     cow_count += 1
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.putText(frame, currentClass, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (0, 0, 255), 2)  # print(x1, y1)


                # if cow_count>=3:
                #     requests.get("http://192.168.227.174/excesscow")
                # if dog_count>=3:
                #     requests.get("http://192.168.227.174/excessdog")
                # if cat_count>=3:
                #     requests.get("http://192.168.227.174/excesscat")

        if obj_count>=3:
            requests.get("http://192.168.245.174/excess")


        payload = {
            "classes": list(classes),
            "count": obj_count
        }

        # Convert payload to JSON string
        payload_json = json.dumps(payload)
        response = requests.post(url, data=payload_json, headers=headers)
        print(response)



    cv2.imshow("Image", frame)
    cv2.waitKey(1)
