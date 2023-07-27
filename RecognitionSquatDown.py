import cv2
import mediapipe as mp
import numpy as np

#cam = cv2.VideoCapture(0)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()
status = False
h = 0
w = 0

 
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

def main(cap):
    global h, w, status
    
    if not cap.isOpened():
        print("Camera not open")
        exit()

    #cv2.namedWindow('frame', 0) # 設定視窗名稱
    #cv2.resizeWindow('frame', 600, 500)  #重設視窗大小

    ret, frame = cap.read()
    if not ret:
        print("Read Error")
        exit()

    preview = frame.copy()       
    rgbframe = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
    results = pose.process(rgbframe) # 從影像增測姿勢    
    h, w, _ = frame.shape # (480, 640, 3)


    if results.pose_world_landmarks:
        mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # Leg
        hip_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        hip_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        knee_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        knee_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
        ankle_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        ankle_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

        # 计算角度
        angle_left_knee = angle_between_points(hip_left, knee_left, ankle_left)
        angle_right_knee = angle_between_points(hip_right, knee_right, ankle_right)

        
        if (angle_left_knee <= 180 and angle_left_knee >= 150 and angle_right_knee >= 90 and angle_right_knee <= 120)or (angle_right_knee <= 180 and angle_right_knee >= 150 and angle_left_knee >= 90 and angle_left_knee <= 120): # 綠色 標準動作
            #cv2.putText(preview, "Left Angle: {:f}".format(angle_left_knee), (1400, 920), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
            return 1
              
        elif (angle_left_knee < 150 and angle_left_knee >= 120 and angle_right_knee > 120 and angle_right_knee <= 150) or (angle_right_knee <= 150 and angle_right_knee >= 120 and angle_left_knee > 120 and angle_left_knee <= 150): # 黃色
            #cv2.putText(preview, "Left Angle: {:f} ".format(angle_left_knee), (400, 360), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            return 2

        else:
            #cv2.putText(preview, "Left Angle: {:f}".format(angle_left_knee), (1400, 920), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            return 3


if __name__ == '__main__':
    main()