import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

class Coordinate:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

def get_mid_point(a, b):
    mid = Coordinate()
    mid.x = (a.x + b.x) / 2
    mid.y = (a.y + b.y) / 2
    mid.z = (a.z + b.z) / 2
    return mid

def get_vector(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    return ba, bc

def angle_between_points(a, b, c):
    ba, bc = get_vector(a, b, c)
    dot = np.dot(ba, bc) # 內積(distance_ba * distance_bc * cos0)
    distance_ba = np.linalg.norm(ba)
    distance_bc = np.linalg.norm(bc)

    cosine_angle = dot / (distance_ba * distance_bc)
    angle_rad = np.arccos(cosine_angle) # 算出0 (弧度表示)
    angel_deg = np.degrees(angle_rad) # 將弧度轉為度數
    return angel_deg

def main(cam):

    ret, frame = cam.read()
    if not ret:
        print("Read Error")
        exit()
    frame = cv2.flip(frame, 1) #矩陣左右翻轉   ******
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgbframe) # 從影像增測姿勢    

    if results.pose_world_landmarks:
        # Hand
        wrist_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        wrist_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        elbow_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        elbow_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        shoulder_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Leg
        hip_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        knee_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        hip_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        knee_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        hip_middle = get_mid_point(hip_left, hip_right)

        angle_left_hand = angle_between_points(wrist_left, elbow_left, shoulder_left)
        angle_right_hand = angle_between_points(wrist_right, elbow_right, shoulder_right)
        angle_left_leg = angle_between_points(hip_left, knee_left, hip_middle)
        angle_right_leg = angle_between_points(hip_right, knee_right, hip_middle)
        angle_two_leg = angle_between_points(knee_left, hip_middle, knee_right)

        # GREEN
        if (angle_left_leg >= 15 and angle_left_leg <= 18) and (angle_right_leg >= 15 and angle_right_leg <= 18) and  (angle_two_leg >= 50 and angle_two_leg <= 120) and (angle_left_hand <= 165 and angle_left_hand >= 150) and (angle_right_hand <= 165 and angle_right_hand >= 150): 
            return 1
        # YELLOW   
        elif (angle_left_leg >= 10 and angle_left_leg < 14) and (angle_right_leg >= 10 and angle_right_leg < 14) and  (angle_two_leg >= 50 and angle_two_leg <= 120) and (angle_left_hand < 150 and angle_left_hand >= 135) and (angle_right_hand < 150 and angle_right_hand >= 135): # 黃色
            return 2
        # RED
        else:
            return 3


if __name__ == '__main__':
    main()
