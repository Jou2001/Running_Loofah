import cv2
import mediapipe as mp
import numpy as np

cam = cv2.VideoCapture(1)
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

def main():
    global status
    flag = False
    if not cam.isOpened():
        print("Camera not open")
        exit()

    #cv2.namedWindow('frame', 0) # 設定視窗名稱
    #cv2.resizeWindow('frame', 800, 700)  #重設視窗大小


    while not flag:
        ret, frame = cam.read()
        if not ret:
            print("Read Error")
            break

        frame = cv2.flip(frame, 1) #矩陣左右翻轉   ******
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgbframe) # 從影像增測姿勢
        frame = cv2.resize(frame, (650, 500))
        
        preview = frame.copy()

        if results.pose_world_landmarks:
            mp_drawing.draw_landmarks(preview, results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
            # 获取关键点坐标
            hip_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            hip_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            knee_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
            knee_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            ankle_left = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
            ankle_right = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

            # 计算角度
            angle_left_knee = angle_between_points(hip_left, knee_left, ankle_left)
            angle_right_knee = angle_between_points(hip_right, knee_right, ankle_right)

            # 左腳
            if angle_left_knee >= 90 and angle_left_knee <= 120: # 綠色 標準動作
                cv2.putText(preview, "Left Angle: {:f} ".format(angle_left_knee), (400, 360)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA
                            )
            elif ( angle_left_knee >= 80 and angle_left_knee <= 90 ) or (angle_left_knee > 120 and angle_left_knee < 130): # 黃色
                cv2.putText(preview, "Left Angle: {:f} ".format(angle_left_knee), (400, 360)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA
                            )
            else: # 紅色 
                cv2.putText(preview, "Left Angle: {:f} ".format(angle_left_knee), (400, 360)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                            )

            #判斷右腳角度
            if angle_right_knee >= 90 and angle_right_knee <= 120:
                cv2.putText(preview, "Right Angle: {:f} ".format(angle_right_knee), (400, 400)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA
                            )
            elif ( angle_right_knee >= 80 and angle_right_knee <= 90 ) or (angle_right_knee > 120 and angle_right_knee < 130):
                cv2.putText(preview, "Right Angle: {:f} ".format(angle_right_knee), (400, 400)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA
                            )
            else:
                cv2.putText(preview, "Right Angle: {:f} ".format(angle_right_knee), (400 , 400)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                            )

            
            avg_angle = int((angle_left_knee + angle_right_knee) // 2)


            if status:
                if avg_angle > 160:
                    status = False
            else:
                if avg_angle >= 90 and avg_angle <= 120 :
                    status = True


            if status:
                cv2.putText(preview, f"Pose: {status} Angle: {avg_angle:d} ", (400, 440)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA
                            )
            else:
                cv2.putText(preview, f"AVG_Angle: {avg_angle:d} Pose: {status}", (400, 440)
                            , cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA
                            )

            # 输出角度
           # print("Left knee angle: ", angle_left_knee)
           # print("Right knee angle: ", angle_right_knee)

        # 显示画面
        # rgbframe.flags.writeable = True
        # rgbframe = cv2.cvtColor(rgbframe, cv2.COLOR_RGB2BGR)

        # 绘制姿态估计结果
        # mp_drawing.draw_landmarks(rgbframe, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # cv2.imshow("MediaPipe Pose Estimation", rgbframe)
        cv2.imshow('frame', preview)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
