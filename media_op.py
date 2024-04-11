import cv2
import mediapipe as mp
import pyautogui as p
import time

def count_fingers(lst):
    y_values = [pt.y * 100 for pt in lst.landmark]
    x_values = [pt.x * 100 for pt in lst.landmark]
    thresh = (y_values[0] - y_values[9]) / 2
    cnt = sum(1 for i in range(5, 21, 4) if (y_values[i] - y_values[i-3]) > thresh)
    cnt += 1 if (x_values[5] - x_values[4]) > 6 else 0
    return cnt

cap = cv2.VideoCapture(0)
drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands.Hands(max_num_hands=1)

start_init = False
prev = -1
cooldown_duration = 2
cooldown_start_time = 0

while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)
    frm_rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    frm_rgb_resized = cv2.resize(frm_rgb, (320, 240))  # Resize for faster processing
    res = hands.process(frm_rgb_resized)

    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]
        cnt = count_fingers(hand_keyPoints)

        if prev != cnt:
            current_time = time.time()
            if not start_init or (current_time - cooldown_start_time) > cooldown_duration:
                if cnt == 5:
                    p.press("left")
                    action_text = "Backward"
                elif cnt == 1:
                    p.press("space")
                    action_text = "Play/Pause"
                elif cnt == 2:
                    p.press("up")
                    action_text = "Volume UP"
                elif cnt == 3:
                    p.press("down")
                    action_text = "Volume Down"
                elif cnt == 4:
                    p.press("right")
                    action_text = "Forward"
                else:
                    action_text = ""
                if action_text:
                    cv2.putText(frm, action_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                    cooldown_start_time = current_time
                    prev = cnt
                    start_init = False

        drawing.draw_landmarks(frm, hand_keyPoints, mp.solutions.hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()



