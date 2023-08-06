import cv2
import mediapipe as mp
from mediapipe.tasks import python
import time

def start(send_queue, receieve_queue):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
    mp_draw = mp.solutions.drawing_utils

    # model_path = "./media_player_gesture/gesture_recognizer.task"
    model_path = "./test_media_player_gesture/gesture_recognizer.task"

    gesture_recognizer = mp.tasks.vision.GestureRecognizer
    gesture_recognizer_options = mp.tasks.vision.GestureRecognizerOptions
    vision_running_mode = mp.tasks.vision.RunningMode

    # temporary fix to file loading
    model_file = open(model_path, "rb")
    model_data = model_file.read()
    model_file.close()

    options = gesture_recognizer_options(
        base_options=mp.tasks.BaseOptions(model_asset_buffer=model_data),
        running_mode=vision_running_mode.IMAGE
    )
    with gesture_recognizer.create_from_options(options) as recognizer:
        cap = cv2.VideoCapture(0)
        gesture = 'none'
        time_elapsed = 0
        last_time = 0

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

                            mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)
                    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=framergb)
                    # Predict the hand gesture
                    recognizer_result = recognizer.recognize(image)

                    # gesture detection filter
                    if len(recognizer_result.gestures) > 0 and recognizer_result.gestures[0][0].score > 0.80 and \
                            recognizer_result.gestures[0][0].category_name != 'none' and \
                            len(recognizer_result.gestures[0][0].category_name) > 0:
                        # if the gesture has changed, reset the elapsed time
                        if recognizer_result.gestures[0][0].category_name != gesture:
                            time_elapsed = 0
                            gesture = recognizer_result.gestures[0][0].category_name
                        else:
                            time_elapsed += (time.time() * 1000) - (last_time * 1000)
                        # if gesture is long enough, send message, reset time
                        if time_elapsed > 1000:
                            print(recognizer_result.gestures[0][0].category_name)
                            send_queue.put(recognizer_result.gestures[0][0].category_name)
                            time_elapsed = 0
                    else:
                        time_elapsed = 0

                    # reset last time
                    last_time = time.time()
                    # display the image on the webcam
                    if len(recognizer_result.gestures) > 0:
                        cv2.putText(frame, recognizer_result.gestures[0][0].category_name + " (%" +
                                    str(recognizer_result.gestures[0][0].score) + ")", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow("Output", frame)
                cv2.waitKey(10)

            # If a message is sent from the media player to the gesture detector, end the loop
            if not receieve_queue.empty():
                break

    cap.release()
    cv2.destroyAllWindows()


