import cv2
import mediapipe as mp
from mediapipe.tasks import python

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

#model_path = "./media_player_gesture/gesture_recognizer.task"
model_path = "./test_media_player_gesture/gesture_recognizer.task"

GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

#temporary fix to file loading
model_file = open(model_path, "rb")
model_data = model_file.read()
model_file.close()

options = GestureRecognizerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_buffer=model_data),
    running_mode=VisionRunningMode.IMAGE
)
with GestureRecognizer.create_from_options(options) as recognizer:
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        if frame is not None:

            x, y, c = frame.shape

            frame = cv2.flip(frame, 1)

            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Get hand landmarks
            result = hands.process(framergb)

            className = ''

            # post process the result
            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)

                        landmarks.append([lmx, lmy])

                        mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=framergb)
                # Predict the hand gesture
                recognizer_result = recognizer.recognize(image)

                print(len(recognizer_result.gestures))
                if len(recognizer_result.gestures) > 0:
                    cv2.putText(frame, recognizer_result.gestures[0][0].category_name + " (%" +
                                str(recognizer_result.gestures[0][0].score) + ")", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("Output", frame)

        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

