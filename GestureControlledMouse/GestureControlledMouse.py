import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

index_x, index_y = 0, 0
thumb_x, thumb_y = 0, 0
dragging = False
drag_start = (0, 0)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    
                    # Check distance between index and thumb for click or drag
                    distance = abs(index_y - thumb_y)
                    
                    if distance < 20:
                        if not dragging:
                            pyautogui.click()
                            pyautogui.sleep(1)
                    elif 20 <= distance < 100:
                        pyautogui.moveTo(index_x, index_y)
                        
                    # Implement drag and drop functionality
                    if distance >= 100:
                        if not dragging:
                            dragging = True
                            drag_start = (index_x, index_y)
                            pyautogui.mouseDown()
                    else:
                        if dragging:
                            dragging = False
                            pyautogui.mouseUp()
                    
                    # Implement right-click gesture
                    if len(hands) == 1:  # Assume single hand for right-click
                        if distance > 100:  # Thumb far from index finger
                            pyautogui.rightClick()
                    
                    # Implement keyboard control (example: 'a' key)
                    if len(hands) == 2:  # Two-hand gesture for keyboard control
                        hand1 = hands[0]
                        hand2 = hands[1]
                        
                        if hand1 and hand2:
                            landmarks1 = hand1.landmark
                            landmarks2 = hand2.landmark
                            
                            # Check if fingers are close enough to simulate typing 'a'
                            if (landmarks1[4].y - landmarks1[8].y < -0.1 * frame_height and
                                landmarks2[4].y - landmarks2[8].y < -0.1 * frame_height):
                                pyautogui.press('a')
                                
    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
