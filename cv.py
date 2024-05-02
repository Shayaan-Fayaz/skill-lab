import cv2

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the image
img = cv2.VideoCapture(0)

while True:
    ret, frame = img.read()
    # gra
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Image', frame)
    cv2.waitKey(1)
# Convert the image to grayscale

# Detect faces

# Draw bounding boxes around the detected faces


# Display the result

# cv2.destroyAllWindows()
