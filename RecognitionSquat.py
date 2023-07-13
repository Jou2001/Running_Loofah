import cv2
import mediapipe as mp
import numpy as np

# cam = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
status = False

pose = mp_pose.Pose()

def angle_between_points(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    

    dot = np.dot(ba, bc) # 內積(distance_ba * distance_bc * cos0)
    distance_ba = np.linalg.norm(ba)
    distance_bc = np.linalg.norm(bc)

    cosine_angle = dot / (distance_ba * distance_bc)
    angle_rad = np.arccos(cosine_angle) # 算出0 (弧度表示)
    angel_deg = np.degrees(angle_rad) # 將弧度轉為度數
    return angel_deg

def main(preview):
    global status
    flag = False
    
    rgbframe = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
    results = pose.process(rgbframe) # 從影像增測姿勢    

    if results.pose_world_landmarks:
        # mp_drawing.draw_landmarks(preview, results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
        
        hip_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        hip_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        knee_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        knee_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        ankle_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        ankle_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

        angle_left_knee = angle_between_points(hip_left, knee_left, ankle_left)
        angle_right_knee = angle_between_points(hip_right, knee_right, ankle_right)

        if (angle_left_knee >= 90 and angle_left_knee <= 120) and (angle_right_knee >= 90 and angle_right_knee <= 120): # 綠色 標準動作
            return 1
        elif (( angle_left_knee >= 80 and angle_left_knee <= 90 ) or (angle_left_knee > 120 and angle_left_knee < 130)) and ( ( angle_right_knee >= 80 and angle_right_knee <= 90 ) or (angle_right_knee > 120 and angle_right_knee < 130)): # 黃色
            return 2
        else: # 紅色 
            return 2

if __name__ == '__main__':
    main()