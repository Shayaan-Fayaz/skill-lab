import cv2

# Open the default camera (usually the first camera connected)
cap = cv2.VideoCapture(0)

# Create the background subtractor object
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Morphological operations to remove noise
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel=None)

    # Find contours in the foreground mask
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found (motion detected), print a message
    if contours:
        print("Object in motion detected!")

    # Draw bounding boxes around the detected motion
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow('Motion Detection', frame)

    # Check for key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
