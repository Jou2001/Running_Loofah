import cv2
import mediapipe as mp
import numpy as np

cam = cv2.VideoCapture(1)
mppose = mp.solutions.pose
mpdraw = mp.solutions.drawing_utils
poses = mppose.Pose()
h = 0
w = 0

status = False
 
def calc_angles(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])

    angle = np.abs(radians * 180.0 / np.pi) # 計算絕對值

    if angle > 180:
        angle = 360 - angle

    return angle

# 取得關節結點座標
def get_landmark(landmarks, part_name): 
    return [
        landmarks[mppose.PoseLandmark[part_name].value].x,
        landmarks[mppose.PoseLandmark[part_name].value].y,
        landmarks[mppose.PoseLandmark[part_name].value].z,
    ]

def get_visibility(landmarks): # 偵測測座標
    if landmarks[mppose.PoseLandmark["RIGHT_HIP"].value].visibility < 0.8 or \
            landmarks[mppose.PoseLandmark["LEFT_HIP"].value].visibility < 0.8:
        return False
    else:
        return True

# 計算身體比率函式 *****
def get_body_ratio(landmarks):
    r_body = abs(landmarks[mppose.PoseLandmark["RIGHT_SHOULDER"].value].y
                 - landmarks[mppose.PoseLandmark["RIGHT_HIP"].value].y)
    l_body = abs(landmarks[mppose.PoseLandmark["LEFT_SHOULDER"].value].y
                 - landmarks[mppose.PoseLandmark["LEFT_HIP"].value].y)
    avg_body = (r_body + l_body) / 2
    r_leg = abs(landmarks[mppose.PoseLandmark["RIGHT_HIP"].value].y
                - landmarks[mppose.PoseLandmark["RIGHT_ANKLE"].value].y)
    l_leg = abs(landmarks[mppose.PoseLandmark["LEFT_HIP"].value].y
                - landmarks[mppose.PoseLandmark["LEFT_ANKLE"].value].y)
    if r_leg > l_leg:
        return r_leg / avg_body
    else:
        return l_leg / avg_body

def get_body_angle(landmarks):
    r_shoulder = get_landmark(landmarks, "RIGHT_SHOULDER")
    l_shoulder = get_landmark(landmarks, "LEFT_SHOULDER")

    r_hip = get_landmark(landmarks, "RIGHT_HIP")
    l_hip = get_landmark(landmarks, "LEFT_HIP")

    r_knee = get_landmark(landmarks, "RIGHT_KNEE")
    l_knee = get_landmark(landmarks, "LEFT_KNEE")

    r_body_angle = calc_angles(r_shoulder, r_hip, r_knee)
    l_body_angle = calc_angles(l_shoulder, l_hip, l_knee)

    m_hip = (r_hip + l_hip)
    m_hip = [x / 2 for x in m_hip]
    m_knee = (r_knee + l_knee)
    m_knee = [x / 2 for x in m_knee]
    m_shoulder = (r_shoulder + l_shoulder)
    m_shoulder = [x / 2 for x in m_shoulder]

    mid_angle = calc_angles(m_shoulder, m_hip, m_knee)

    return [int(r_body_angle),int(l_body_angle) ,int(mid_angle)]

def get_hand_angle(landmarks): 
    r_wrist = get_landmark(landmarks, "RIGHT_WRIST")
    l_wrist = get_landmark(landmarks, "LEFT_WRIST")

    r_shoulder = get_landmark(landmarks, "RIGHT_SHOULDER")
    l_shoulder = get_landmark(landmarks, "LEFT_SHOULDER")

    r_elbow = get_landmark(landmarks, "RIGHT_ELBOW")
    l_elbow = get_landmark(landmarks, "LEFT_ELBOW")

    r_hip = get_landmark(landmarks, "RIGHT_HIP")
    l_hip = get_landmark(landmarks, "LEFT_HIP")

    r_hand1_angle = calc_angles(r_wrist, r_elbow, r_shoulder)
    l_hand1_angle = calc_angles(l_wrist, l_elbow, l_shoulder)
    
    r_hand2_angle = calc_angles(r_elbow, r_shoulder, r_hip)
    l_hand2_angle = calc_angles(l_elbow, l_shoulder, l_hip)

    m_hip = (r_hip + l_hip)
    m_hip = [x / 2 for x in m_hip]
    m_elbow = (r_elbow + l_elbow)
    m_elbow = [x/2 for x in m_elbow]
    m_wrist= (r_wrist + r_wrist)
    m_wrist = [x / 2 for x in m_wrist]
    m_shoulder = (r_shoulder + l_shoulder)
    m_shoulder = [x / 2 for x in m_shoulder]

    mid_angle = calc_angles(m_wrist, m_elbow, m_shoulder)
    mid_angle2 = calc_angles(m_elbow, m_shoulder, m_hip)

    return [int(r_hand1_angle),int(l_hand1_angle) ,int(mid_angle)], [int(r_hand2_angle),int(l_hand2_angle) ,int(mid_angle2)]

def get_foot_angle(landmarks):

    r_hip = get_landmark(landmarks, "RIGHT_HIP")
    l_hip = get_landmark(landmarks, "LEFT_HIP")

    r_knee = get_landmark(landmarks, "RIGHT_KNEE")
    l_knee = get_landmark(landmarks, "LEFT_KNEE")

    r_ankle = get_landmark(landmarks, "RIGHT_ANKLE")
    l_ankle = get_landmark(landmarks, "LEFT_ANKLE")
    
    r_foot_angle = calc_angles(r_hip, r_knee, r_ankle)
    l_foot_angle = calc_angles(l_hip, l_knee, l_ankle)

    m_hip = (r_hip + l_hip)
    m_hip = [x / 2 for x in m_hip]
    m_knee = (r_knee + l_knee)
    m_knee = [x / 2 for x in m_knee]
    m_ankle = (r_ankle + l_ankle)
    m_ankle = [x / 2 for x in m_ankle]

    mid_angle = calc_angles(m_hip, m_knee, m_ankle)

    return [int(r_foot_angle),int(l_foot_angle) ,int(mid_angle)]

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
        frame = cv2.flip(frame, 1) #矩陣左右翻轉   ******
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        poseoutput = poses.process(rgbframe) # 從影像增測姿勢
        h, w, _ = frame.shape # (480, 640, 3)
        preview = frame.copy()

        if poseoutput.pose_landmarks:
            ### 畫身體支架/關節 ###
            mpdraw.draw_landmarks(preview, poseoutput.pose_landmarks, mppose.POSE_CONNECTIONS)
            body_angle = get_body_angle(poseoutput.pose_landmarks.landmark)
            hand_angle1, hand_angle2 = get_hand_angle(poseoutput.pose_landmarks.landmark)
            foot_angles = get_foot_angle(poseoutput.pose_landmarks.landmark)
            # body_ratio = get_body_ratio(poseoutput.pose_landmarks.landmark)
           
            #左前右後
            if foot_angles[0] >= 135 and foot_angles[0] <= 165 and foot_angles[1] >= 150 and foot_angles[1] <= 180 \
                and hand_angle1[0] >= 160 and hand_angle1[0] <= 180 and hand_angle2[0] >= 160 and hand_angle2[0] <= 175 \
                and body_angle[0] >= 145 and body_angle[0] <= 165 and body_angle[1] >= 160 and body_angle[1] <= 180 : # 綠色 標準動作
                
                cv2.putText(preview, "Left Angle: {:d}".format(foot_angles[0]), (1400, 920)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "Right Angle: {:d}".format(foot_angles[1]), (1400, 960)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "hand Angle1: {:d}".format(hand_angle1[0]), (1400, 1000)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "hand Angle2: {:d}".format(hand_angle2[0]), (1400, 1020)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "body Angle1: {:d}".format(body_angle[0]), (1400, 1050)
                        , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                        ) 
                cv2.putText(preview, "body Angle2: {:d}".format(body_angle[1]), (1400, 1080)
                        , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                        )   
            # 右前左後
            elif foot_angles[1] >= 135 and foot_angles[1] <= 165 and foot_angles[0] >= 150 and foot_angles[0] <= 180 \
                and hand_angle1[0] >= 160 and hand_angle1[0] <= 180 and hand_angle2[0] >= 160 and hand_angle2[0] <= 175 \
                and body_angle[1] >= 145 and body_angle[1] <= 165 and body_angle[0] >= 160 and body_angle[0] <= 180 :

                cv2.putText(preview, "Left Angle: {:d}".format(foot_angles[0]), (1400, 920)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "Right Angle: {:d}".format(foot_angles[1]), (1400, 960)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "hand Angle1: {:d}".format(hand_angle1[0]), (1400, 1000)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "hand Angle2: {:d}".format(hand_angle2[0]), (1400, 1020)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "body Angle1: {:d}".format(body_angle[0]), (1400, 1050)
                        , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                        ) 
                cv2.putText(preview, "body Angle2: {:d}".format(body_angle[1]), (1400, 1080)
                        , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                        )

            else:
                cv2.putText(preview, "Left Angle: {:d}".format(foot_angles[0]), (1400, 920)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "Right Angle: {:d}".format(foot_angles[1]), (1400, 960)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "hand Angle1: {:d}".format(hand_angle1[0]), (1400, 1000)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "hand Angle2: {:d}".format(hand_angle2[0]), (1400, 1020)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )
                cv2.putText(preview, "body Angle1: {:d}".format(body_angle[0]), (1400, 1050)
                        , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                        ) 
                cv2.putText(preview, "body Angle2: {:d}".format(body_angle[1]), (1400, 1080)
                        , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                        )       
                 

            ''''
            
            avg_angle = int((knee_angles[0] + knee_angles[1]) // 2)


            if status:
                if avg_angle > 160:
                    status = False
            else:
                if avg_angle > 100 and avg_angle < 120 and body_ratio > 1.2 and body_ratio < 1.7:
                    status = True


            if status:
                cv2.putText(preview, f"Pose: {status} Angle: {avg_angle:d} ", (1400, 1000)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA
                            )
            else:
                cv2.putText(preview, f"AVG_Angle: {avg_angle:d} Pose: {status}", (1400, 1000)
                            , cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                            )

            '''
        cv2.imshow('frame', preview)
        

        if cv2.waitKey(1) & 0xFF == ord(' '):
            flag = True

    # release camera
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()