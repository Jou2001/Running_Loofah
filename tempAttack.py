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

def is_hand_raised(wrist, shoulder):
    # 如果手腕的垂直位置（y坐标）低于肩膀，则认为手没有举起
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

def main():
    global h, w, status
    flag = False
    if not cam.isOpened():
        print("Camera not open")
        exit()

    cv2.namedWindow('frame', 0) # 設定視窗名稱
    cv2.resizeWindow('frame', 600, 500)  #重設視窗大小

    while not flag:
        ret, frame = cam.read()
        if not ret:
            print("Read Error")
            break
        # frame = cv2.flip(frame, 1) #矩陣左右翻轉   ******
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgbframe) # 從影像增測姿勢   
        frame = cv2.flip(frame, 1) #矩陣左右翻轉   ****** 
        h, w, _ = frame.shape # (480, 640, 3)
        preview = frame.copy()

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

            # 计算角度
            angle_left_hand = angle_between_points(wrist_left, elbow_left, shoulder_left)
            angle_right_hand = angle_between_points(wrist_right, elbow_right, shoulder_right)
            angle_left_shoulder = angle_between_points(elbow_left, shoulder_left, hip_left)   
            angle_right_shoulder = angle_between_points(elbow_right, shoulder_right, hip_right)

            # 判断每只手是否举起
            left_hand_raised = is_hand_raised(wrist_left, shoulder_left)
            right_hand_raised = is_hand_raised(wrist_right, shoulder_right)

            if ( (angle_left_hand <= 180 and angle_left_hand >= 150 ) and (angle_left_shoulder <= 180 and angle_left_shoulder >= 150 ) and (left_hand_raised and not right_hand_raised)) :
                print( "PlayAgain")
            #    return "PlayAgain"
                # print( "PlayAgain")
            
            elif( (angle_right_hand <= 180 and angle_right_hand >= 150 ) and (angle_right_shoulder <= 180 and angle_right_shoulder >= 150 ) and (right_hand_raised and not left_hand_raised)) : # 綠色 標準動作
                print( "End")
                # return "End"
                # print( "End")
                    
            else :
                # return 3
                print( "3")

        cv2.imshow('frame', preview)
        

        if cv2.waitKey(1) & 0xFF == ord(' '):
            flag = True

    # release camera
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()