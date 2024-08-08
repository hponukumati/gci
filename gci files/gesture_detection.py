# gesture_recognition.py
import cv2
import mediapipe as mp
import os
import json

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[id * 4 + 4].y < hand_landmarks.landmark[id * 4 + 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

def load_settings():
    if os.path.exists('gesture_settings.json'):
        with open('gesture_settings.json', 'r') as f:
            return json.load(f)
    return {str(i): '' for i in range(1, 6)}

def open_application(fingers_count, settings):
    app_path = settings.get(str(fingers_count), '')
    if app_path:
        os.system(f'open "{app_path}"')

def capture_video():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    hands = mp_hands.Hands()
    settings = load_settings()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB

        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Count fingers and open applications
                fingers_count = count_fingers(hand_landmarks)
                open_application(fingers_count, settings)
                cv2.putText(frame, f'Fingers: {fingers_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Webcam Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
