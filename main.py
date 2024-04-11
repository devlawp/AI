import cv2

# Load the pre-trained hand cascade
hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_hand.xml')

# Capture video from the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands in the frame
    hands = hand_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around detected hands
    for (x, y, w, h) in hands:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
