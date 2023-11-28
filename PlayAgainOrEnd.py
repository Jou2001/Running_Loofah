import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def is_hand_raised(wrist, shoulder):
    return wrist.y <= shoulder.y

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

def main(cam):
    
    ret, frame = cam.read()
    if not ret:
        print("Read Error")
        exit()
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgbframe) # 從影像增測姿勢 
    frame = cv2.flip(frame, 1) #矩陣左右翻轉   ******

    if results.pose_world_landmarks:
        # mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # Hand
        wrist_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        wrist_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        elbow_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        elbow_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        shoulder_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        hip_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        hip_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

        
        angle_left_hand = angle_between_points(wrist_left, elbow_left, shoulder_left)
        angle_right_hand = angle_between_points(wrist_right, elbow_right, shoulder_right)
        angle_left_shoulder = angle_between_points(elbow_left, shoulder_left, hip_left)   
        angle_right_shoulder = angle_between_points(elbow_right, shoulder_right, hip_right)
        left_hand_raised = is_hand_raised(wrist_left, shoulder_left)
        right_hand_raised = is_hand_raised(wrist_right, shoulder_right)


        if ( (angle_left_hand <= 180 and angle_left_hand >= 150 ) and (angle_left_shoulder <= 180 and angle_left_shoulder >= 150 ) and (left_hand_raised and not right_hand_raised)) :
           return "PlayAgain"
        
        elif( (angle_right_hand <= 180 and angle_right_hand >= 150 ) and (angle_right_shoulder <= 180 and angle_right_shoulder >= 150 ) and (right_hand_raised and not left_hand_raised)) : 
            return "End"
                
        else :
            return 3

if __name__ == '__main__':
    main()