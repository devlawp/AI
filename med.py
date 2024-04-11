import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe hands module
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

# Initialize video capture
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Unable to open camera.")
    exit()

prev = -1

while True:
    # Capture frame-by-frame
    ret, frm = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Flip the frame horizontally
    frm = cv2.flip(frm, 1)

    # Process the frame with MediaPipe hands
    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    # Your hand detection and gesture recognition logic goes here
    # ...

    # Display the frame
    cv2.imshow("window", frm)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
