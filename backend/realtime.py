# import cv2
# import torch
# import numpy as np
# from collections import deque
# from model import DrowsinessTransformer
# from utils import eye_aspect_ratio, mouth_aspect_ratio, head_pitch_angle, LEFT_EYE, RIGHT_EYE
# import mediapipe as mp
# import warnings
# import pygame
# import threading

# # NEW
# from backend.fatigue import calculate_fatigue_score, fatigue_level
# from backend.logger import log_event

# warnings.filterwarnings("ignore", category=UserWarning, message="SymbolDatabase.GetPrototype")

# # =========================
# # GLOBAL CONTROL FLAGS
# # =========================
# detection_running = False
# last_status = None


# # =========================
# # START DETECTION FUNCTION
# # =========================
# def start_detection():

#     global detection_running
#     global last_status

#     detection_running = True
#     last_status = None

#     pygame.mixer.init()
#     pygame.mixer.music.load("loud_alarm.wav")

#     SEQ_LEN = 30
#     SMOOTHING_WINDOW = 7
#     EYE_CLOSED_EAR = 0.18
#     CLOSED_EYES_FRAME_THRESHOLD = 8

#     EAR_MIN, EAR_MAX = 0.15, 0.35
#     MAR_MIN, MAR_MAX = 0.0, 0.3
#     HEAD_MIN, HEAD_MAX = 0.0, 180.0

#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = DrowsinessTransformer()
#     model.load_state_dict(torch.load("checkpoints/best_model.pt", map_location=device))
#     model.eval()
#     model.to(device)

#     pred_queue = deque(maxlen=SMOOTHING_WINDOW)

#     mp_face_mesh = mp.solutions.face_mesh
#     face_mesh = mp_face_mesh.FaceMesh(
#         static_image_mode=False,
#         max_num_faces=1,
#         refine_landmarks=True
#     )

#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#     seq_features = [[0.5, 0.0, 0.5]] * SEQ_LEN
#     closed_frames = 0

#     while detection_running:

#         ret, frame = cap.read()
#         if not ret:
#             break

#         h, w = frame.shape[:2]
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(rgb)

#         face_detected = False

#         if results.multi_face_landmarks:

#             face_detected = True
#             lm = results.multi_face_landmarks[0]

#             landmarks = {
#                 i: (lmk.x * w, lmk.y * h)
#                 for i, lmk in enumerate(lm.landmark)
#             }

#             ear = (
#                 eye_aspect_ratio(landmarks, LEFT_EYE)
#                 + eye_aspect_ratio(landmarks, RIGHT_EYE)
#             ) / 2

#             mar = mouth_aspect_ratio(landmarks)
#             head_angle = head_pitch_angle(landmarks)

#         else:

#             ear, mar, head_angle = 0.0, 0.0, 0.0

#         ear_norm = np.clip((ear - EAR_MIN) / (EAR_MAX - EAR_MIN), 0, 1)
#         mar_norm = np.clip((mar - MAR_MIN) / (MAR_MAX - MAR_MIN), 0, 1)
#         head_norm = np.clip((head_angle - HEAD_MIN) / (HEAD_MAX - HEAD_MIN), 0, 1)

#         seq_features.append([ear_norm, mar_norm, head_norm])

#         if len(seq_features) > SEQ_LEN:
#             seq_features.pop(0)

#         pred_label = "Alert"

#         if len(seq_features) == SEQ_LEN:

#             x = torch.tensor([seq_features], dtype=torch.float32).to(device)

#             with torch.no_grad():

#                 out = model(x)
#                 out = torch.softmax(out, dim=-1)

#                 pred = torch.argmax(out, dim=-1).item()
#                 pred_queue.append(pred)

#             pred_smoothed = int(np.round(np.mean(pred_queue)))

#             if ear < EYE_CLOSED_EAR:
#                 closed_frames += 1
#             else:
#                 closed_frames = 0

#             if closed_frames >= CLOSED_EYES_FRAME_THRESHOLD or pred_smoothed == 1:
#                 pred_label = "Drowsy 😴"
#             else:
#                 pred_label = "Alert"

#             if face_detected and pred_label == "Drowsy 😴":

#                 if not pygame.mixer.music.get_busy():
#                     pygame.mixer.music.play(-1)

#             else:

#                 pygame.mixer.music.stop()

#         # =========================
#         # FATIGUE SCORE
#         # =========================

#         fatigue_score = calculate_fatigue_score(ear, mar, head_angle)
#         fatigue_status = fatigue_level(fatigue_score)

#         # =========================
#         # SMART EVENT LOGGING
#         # =========================

#         #global last_status

#         if fatigue_status != last_status:

#             log_event(
#                 "driver",
#                 ear,
#                 mar,
#                 head_angle,
#                 fatigue_score,
#                 fatigue_status
#             )

#             last_status = fatigue_status

#         # =========================
#         # DISPLAY INFO
#         # =========================

#         cv2.putText(
#             frame,
#             f"EAR:{ear:.2f} MAR:{mar:.2f} Head:{head_angle:.1f} | {fatigue_status} | Score:{fatigue_score}",
#             (10, 30),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 0, 255) if fatigue_status != "Alert" else (0, 255, 0),
#             2
#         )

#         if not face_detected:

#             cv2.putText(
#                 frame,
#                 "No Driver Detected",
#                 (10, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (255, 0, 0),
#                 2
#             )

#         cv2.imshow("Driver Drowsiness Detection", frame)

#         if cv2.waitKey(1) & 0xFF == 27:
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     face_mesh.close()
#     pygame.mixer.quit()


# # =========================
# # STOP FUNCTION
# # =========================
# def stop_detection():

#     global detection_running
#     detection_running = False





# import cv2
# import torch
# import numpy as np
# from collections import deque
# from model import DrowsinessTransformer
# from utils import eye_aspect_ratio, mouth_aspect_ratio, head_pitch_angle, LEFT_EYE, RIGHT_EYE
# import mediapipe as mp
# import warnings
# import pygame
# import threading

# # NEW
# from backend.fatigue import calculate_fatigue_score, fatigue_level
# from backend.logger import log_event

# # NEW
# from datetime import datetime

# warnings.filterwarnings("ignore", category=UserWarning, message="SymbolDatabase.GetPrototype")

# # =========================
# # GLOBAL CONTROL FLAGS
# # =========================
# detection_running = False
# last_status = None

# # =========================
# # SESSION SUMMARY VARIABLES
# # =========================
# session_start_time = None
# session_scores = []
# session_levels = []
# session_drowsy_count = 0


# # =========================
# # START DETECTION FUNCTION
# # =========================
# def start_detection():

#     global detection_running
#     global last_status
#     global session_start_time, session_scores, session_levels, session_drowsy_count

#     detection_running = True
#     last_status = None

#     # RESET SESSION DATA
#     session_start_time = datetime.now()
#     session_scores = []
#     session_levels = []
#     session_drowsy_count = 0

#     pygame.mixer.init()
#     pygame.mixer.music.load("loud_alarm.wav")

#     SEQ_LEN = 30
#     SMOOTHING_WINDOW = 7
#     EYE_CLOSED_EAR = 0.18
#     CLOSED_EYES_FRAME_THRESHOLD = 8

#     EAR_MIN, EAR_MAX = 0.15, 0.35
#     MAR_MIN, MAR_MAX = 0.0, 0.3
#     HEAD_MIN, HEAD_MAX = 0.0, 180.0

#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model = DrowsinessTransformer()
#     model.load_state_dict(torch.load("checkpoints/best_model.pt", map_location=device))
#     model.eval()
#     model.to(device)

#     pred_queue = deque(maxlen=SMOOTHING_WINDOW)

#     mp_face_mesh = mp.solutions.face_mesh
#     face_mesh = mp_face_mesh.FaceMesh(
#         static_image_mode=False,
#         max_num_faces=1,
#         refine_landmarks=True
#     )

#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#     seq_features = [[0.5, 0.0, 0.5]] * SEQ_LEN
#     closed_frames = 0

#     while detection_running:

#         ret, frame = cap.read()
#         if not ret:
#             break

#         h, w = frame.shape[:2]
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(rgb)

#         face_detected = False

#         if results.multi_face_landmarks:

#             face_detected = True
#             lm = results.multi_face_landmarks[0]

#             landmarks = {
#                 i: (lmk.x * w, lmk.y * h)
#                 for i, lmk in enumerate(lm.landmark)
#             }

#             ear = (
#                 eye_aspect_ratio(landmarks, LEFT_EYE)
#                 + eye_aspect_ratio(landmarks, RIGHT_EYE)
#             ) / 2

#             mar = mouth_aspect_ratio(landmarks)
#             head_angle = head_pitch_angle(landmarks)

#         else:
#             ear, mar, head_angle = 0.0, 0.0, 0.0

#         ear_norm = np.clip((ear - EAR_MIN) / (EAR_MAX - EAR_MIN), 0, 1)
#         mar_norm = np.clip((mar - MAR_MIN) / (MAR_MAX - MAR_MIN), 0, 1)
#         head_norm = np.clip((head_angle - HEAD_MIN) / (HEAD_MAX - HEAD_MIN), 0, 1)

#         seq_features.append([ear_norm, mar_norm, head_norm])

#         if len(seq_features) > SEQ_LEN:
#             seq_features.pop(0)

#         pred_label = "Alert"

#         if len(seq_features) == SEQ_LEN:

#             x = torch.tensor([seq_features], dtype=torch.float32).to(device)

#             with torch.no_grad():
#                 out = model(x)
#                 out = torch.softmax(out, dim=-1)

#                 pred = torch.argmax(out, dim=-1).item()
#                 pred_queue.append(pred)

#             pred_smoothed = int(np.round(np.mean(pred_queue)))

#             if ear < EYE_CLOSED_EAR:
#                 closed_frames += 1
#             else:
#                 closed_frames = 0

#             if closed_frames >= CLOSED_EYES_FRAME_THRESHOLD or pred_smoothed == 1:
#                 pred_label = "Drowsy 😴"
#             else:
#                 pred_label = "Alert"

#             if face_detected and pred_label == "Drowsy 😴":
#                 if not pygame.mixer.music.get_busy():
#                     pygame.mixer.music.play(-1)
#             else:
#                 pygame.mixer.music.stop()

#         # =========================
#         # FATIGUE SCORE
#         # =========================

#         fatigue_score = calculate_fatigue_score(ear, mar, head_angle)
#         fatigue_status = fatigue_level(fatigue_score)

#         # =========================
#         # SESSION SUMMARY TRACKING
#         # =========================
#         session_scores.append(fatigue_score)
#         session_levels.append(fatigue_status)

#         if fatigue_status != "Alert":
#             session_drowsy_count += 1

#         # =========================
#         # SMART EVENT LOGGING
#         # =========================

#         if fatigue_status != last_status:

#             log_event(
#                 "driver",
#                 ear,
#                 mar,
#                 head_angle,
#                 fatigue_score,
#                 fatigue_status
#             )

#             last_status = fatigue_status

#         # =========================
#         # DISPLAY INFO
#         # =========================

#         cv2.putText(
#             frame,
#             f"EAR:{ear:.2f} MAR:{mar:.2f} Head:{head_angle:.1f} | {fatigue_status} | Score:{fatigue_score}",
#             (10, 30),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 0, 255) if fatigue_status != "Alert" else (0, 255, 0),
#             2
#         )

#         if not face_detected:
#             cv2.putText(
#                 frame,
#                 "No Driver Detected",
#                 (10, 60),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.7,
#                 (255, 0, 0),
#                 2
#             )

#         cv2.imshow("Driver Drowsiness Detection", frame)

#         if cv2.waitKey(1) & 0xFF == 27:
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     face_mesh.close()
#     pygame.mixer.quit()


# # =========================
# # STOP FUNCTION
# # =========================
# def stop_detection():
#     global detection_running
#     detection_running = False


# # =========================
# # SESSION SUMMARY FUNCTION
# # =========================
# def get_session_summary():

#     global session_start_time, session_scores, session_levels, session_drowsy_count

#     if not session_start_time or len(session_scores) == 0:
#         return {
#             "duration": "0 sec",
#             "total_events": 0,
#             "avg_score": 0,
#             "max_score": 0,
#             "most_common_status": "N/A"
#         }

#     duration = datetime.now() - session_start_time
#     duration_str = str(duration).split(".")[0]

#     avg_score = round(sum(session_scores) / len(session_scores), 2)
#     max_score = round(max(session_scores), 2)

#     most_common_status = max(set(session_levels), key=session_levels.count)

#     return {
#         "duration": duration_str,
#         "total_events": session_drowsy_count,
#         "avg_score": avg_score,
#         "max_score": max_score,
#         "most_common_status": most_common_status
#     }


import cv2
import torch
import numpy as np
from collections import deque
from model import DrowsinessTransformer
from utils import eye_aspect_ratio, mouth_aspect_ratio, head_pitch_angle, LEFT_EYE, RIGHT_EYE
import mediapipe as mp
import warnings
import pygame
import threading

from backend.fatigue import calculate_fatigue_score, fatigue_level
from backend.logger import log_event

from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning, message="SymbolDatabase.GetPrototype")


# GLOBAL CONTROL FLAGS

detection_running = False
last_status = None

# SESSION SUMMARY VARIABLES

session_start_time = None
session_scores = []
session_levels = []
session_timestamps = []
session_drowsy_count = 0



# START DETECTION FUNCTION

def start_detection():

    global detection_running
    global last_status
    global session_start_time, session_scores, session_levels, session_timestamps, session_drowsy_count

    detection_running = True
    last_status = None

    # RESET SESSION DATA
    session_start_time = datetime.now()
    session_scores = []
    session_levels = []
    session_timestamps = []
    session_drowsy_count = 0

    pygame.mixer.init()
    pygame.mixer.music.load("loud_alarm.wav")

    SEQ_LEN = 30
    SMOOTHING_WINDOW = 7
    EYE_CLOSED_EAR = 0.18
    CLOSED_EYES_FRAME_THRESHOLD = 8

    EAR_MIN, EAR_MAX = 0.15, 0.35
    MAR_MIN, MAR_MAX = 0.0, 0.3
    HEAD_MIN, HEAD_MAX = 0.0, 180.0

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DrowsinessTransformer()
    model.load_state_dict(torch.load("checkpoints/best_model.pt", map_location=device))
    model.eval()
    model.to(device)

    pred_queue = deque(maxlen=SMOOTHING_WINDOW)

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    seq_features = [[0.5, 0.0, 0.5]] * SEQ_LEN
    closed_frames = 0

    while detection_running:

        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        face_detected = False

        if results.multi_face_landmarks:

            face_detected = True
            lm = results.multi_face_landmarks[0]

            landmarks = {
                i: (lmk.x * w, lmk.y * h)
                for i, lmk in enumerate(lm.landmark)
            }

            ear = (
                eye_aspect_ratio(landmarks, LEFT_EYE)
                + eye_aspect_ratio(landmarks, RIGHT_EYE)
            ) / 2

            mar = mouth_aspect_ratio(landmarks)
            head_angle = head_pitch_angle(landmarks)

        else:
            ear, mar, head_angle = 0.0, 0.0, 0.0

        
        # FEATURE NORMALIZATION
      
        ear_norm = np.clip((ear - EAR_MIN) / (EAR_MAX - EAR_MIN), 0, 1)
        mar_norm = np.clip((mar - MAR_MIN) / (MAR_MAX - MAR_MIN), 0, 1)
        head_norm = np.clip((head_angle - HEAD_MIN) / (HEAD_MAX - HEAD_MIN), 0, 1)

        seq_features.append([ear_norm, mar_norm, head_norm])

        if len(seq_features) > SEQ_LEN:
            seq_features.pop(0)

        pred_label = "Alert"

        
        # TRANSFORMER PREDICTION
      
        if len(seq_features) == SEQ_LEN:

            x = torch.tensor([seq_features], dtype=torch.float32).to(device)

            with torch.no_grad():
                out = model(x)
                out = torch.softmax(out, dim=-1)

                pred = torch.argmax(out, dim=-1).item()
                pred_queue.append(pred)

            pred_smoothed = int(np.round(np.mean(pred_queue)))

            if ear < EYE_CLOSED_EAR:
                closed_frames += 1
            else:
                closed_frames = 0

            if closed_frames >= CLOSED_EYES_FRAME_THRESHOLD or pred_smoothed == 1:
                pred_label = "Drowsy 😴"
            else:
                pred_label = "Alert"

            if face_detected and pred_label == "Drowsy 😴":
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

        # FATIGUE SCORE
       
        fatigue_score = calculate_fatigue_score(ear, mar, head_angle)
        fatigue_status = fatigue_level(fatigue_score)

        
        # SESSION TRACKING + LOGGING
        
        if fatigue_status != last_status:

            session_scores.append(fatigue_score)
            session_levels.append(fatigue_status)
            session_timestamps.append(datetime.now().strftime("%H:%M:%S"))

            if fatigue_status != "Alert":
                session_drowsy_count += 1

            log_event(
                "driver",
                ear,
                mar,
                head_angle,
                fatigue_score,
                fatigue_status
            )

            last_status = fatigue_status

        
        # DISPLAY INFO
       
        cv2.putText(
            frame,
            f"EAR:{ear:.2f} MAR:{mar:.2f} Head:{head_angle:.1f} | {fatigue_status} | Score:{fatigue_score}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255) if fatigue_status != "Alert" else (0, 255, 0),
            2
        )

        if not face_detected:
            cv2.putText(
                frame,
                "No Driver Detected",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

        cv2.imshow("Driver Drowsiness Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()
    pygame.mixer.quit()



# STOP FUNCTION

def stop_detection():
    global detection_running
    detection_running = False



# SESSION SUMMARY FUNCTION

def get_session_summary():

    global session_start_time, session_scores, session_levels, session_drowsy_count

    if not session_start_time or len(session_scores) == 0:
        return {
            "duration": "0 sec",
            "total_events": 0,
            "avg_score": 0,
            "max_score": 0,
            "most_common_status": "N/A"
        }

    duration = datetime.now() - session_start_time
    duration_str = str(duration).split(".")[0]

    avg_score = round(sum(session_scores) / len(session_scores), 2)
    max_score = round(max(session_scores), 2)

    most_common_status = max(set(session_levels), key=session_levels.count)

    return {
        "duration": duration_str,
        "total_events": session_drowsy_count,
        "avg_score": avg_score,
        "max_score": max_score,
        "most_common_status": most_common_status
    }



# SESSION ANALYTICS FUNCTION

def get_session_analytics():

    global session_scores, session_levels, session_timestamps

    if len(session_scores) == 0:
        return {"data": []}

    rows = []
    for i in range(len(session_scores)):
        rows.append([
            session_timestamps[i],
            session_scores[i],
            session_levels[i]
        ])

    return {"data": rows}