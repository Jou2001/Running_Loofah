import cv2
import mediapipe as mp
import numpy as np

cam = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()
status = False
h = 0
w = 0

def get_mid_point(a, b, mid):
    mid.x = (a.x + b.x)/2
    mid.y = (a.y + b.y)/2
    mid.z = (a.z + b.z)/2
    return mid

def get_vector(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    return ba, bc

def angle_between_points(a, b, c):
    ba, bc = get_vector(a, b, c)
    dot = np.dot(ba, bc) 
    distance_ba = np.linalg.norm(ba)
    distance_bc = np.linalg.norm(bc)
    cosine_angle = dot / (distance_ba * distance_bc)
    angle_rad = np.arccos(cosine_angle)
    angel_deg = np.degrees(angle_rad)
    return angel_deg

def get_distance(a, b):
    return np.linalg.norm(np.array([a.x - b.x, a.y - b.y, a.z - b.z]))

def main():
    global h, w, status
    flag = False
    if not cam.isOpened():
        print("Camera not open")
        exit()

    cv2.namedWindow('frame', 0) 
    cv2.resizeWindow('frame', 600, 500)

    while not flag:
        ret, frame = cam.read()
        if not ret:
            print("Read Error")
            break
        frame = cv2.flip(frame, 1)
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgbframe)
        h, w, _ = frame.shape
        preview = frame.copy()

        if results.pose_world_landmarks:
            mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Landmarks for arms and legs
            wrist_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            wrist_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            elbow_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            elbow_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            shoulder_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            shoulder_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            hip_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            knee_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
            hip_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            knee_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            ankle_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
            ankle_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
            hip_middle = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            hip_middle = get_mid_point(hip_left, hip_right, hip_middle)

            # Calculate angles
            angle_left_hand = angle_between_points(wrist_left, elbow_left, shoulder_left)
            angle_right_hand = angle_between_points(wrist_right, elbow_right, shoulder_right)
            angle_left_knee = angle_between_points(hip_left, knee_left, ankle_left)
            angle_right_knee = angle_between_points(hip_right, knee_right, ankle_right)
            angle_two_leg = angle_between_points(knee_left, hip_middle, knee_right)

            # Calculate distances
            distance_knee_hip_left = get_distance(hip_left, knee_left)
            distance_knee_hip_right = get_distance(hip_right, knee_right)
            distance_shoulder_hip_left = get_distance(hip_left, shoulder_left)
            distance_shoulder_hip_right = get_distance(hip_right, shoulder_right)

            # Good posture
            if (angle_left_knee > 80 and angle_left_knee < 120) and (angle_right_knee > 80 and angle_right_knee < 120) and \
                (distance_knee_hip_left < 0.1 and distance_shoulder_hip_left < 0.1) and \
                (distance_knee_hip_right < 0.1 and distance_shoulder_hip_right < 0.1):
                status = "Good posture"

            # Almost there
            elif (angle_left_knee > 60 and angle_left_knee < 150) and (angle_right_knee > 60 and angle_right_knee < 150) and \
                (distance_knee_hip_left < 0.2 and distance_shoulder_hip_left < 0.2) and \
                (distance_knee_hip_right < 0.2 and distance_shoulder_hip_right < 0.2):
                status = "Almost there"

            # Not good posture
            else:
                status = "Not good posture"

        cv2.putText(preview, status, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('frame', preview)
        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            flag = True
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
