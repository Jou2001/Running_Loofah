import cv2
import mediapipe as mp
import numpy as np

cam = cv2.VideoCapture(0)
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
    print("a: ", a)
    print("b: ", b)
    print("mid: ", mid)
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

def main():
    if not cam.isOpened():
        print("Camera not open")
        exit()

    cv2.namedWindow('frame', 0) # 設定視窗名稱
    cv2.resizeWindow('frame', 600, 500)  #重設視窗大小

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Read Error")
            break
        frame = cv2.flip(frame, 1) #矩陣左右翻轉   ******
        rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgbframe) # 從影像增測姿勢    
        h, w, _ = frame.shape # (480, 640, 3)
        preview = frame.copy()

        if results.pose_world_landmarks:
            mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
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


            print("hip_left", hip_left)
            print("hip_right", hip_right)
            print("hip_middle", hip_middle.x, hip_middle.y, hip_middle.z)

            angle_left_hand = angle_between_points(wrist_left, elbow_left, shoulder_left)
            angle_right_hand = angle_between_points(wrist_right, elbow_right, shoulder_right)
            angle_left_leg = angle_between_points(hip_left, knee_left, hip_middle)
            angle_right_leg = angle_between_points(hip_right, knee_right, hip_middle)
            angle_two_leg = angle_between_points(knee_left, hip_middle, knee_right)
            
            is_lunge_step = abs(angle_left_leg - angle_right_leg) > 30  # Define your threshold for lunge step here

            # Use angle_left_leg and angle_right_leg in your logic instead of angle_left_leg and angle_right_leg
            # GREEN
            if (angle_left_leg >= 15 and angle_left_leg <= 20) and (angle_right_leg >= 15 and angle_right_leg <= 20) and  (angle_two_leg >= 50 and angle_two_leg <= 120) and (angle_left_hand <= 180 and angle_left_hand >= 150) and (angle_right_hand <= 180 and angle_right_hand >= 150): 
                
                cv2.putText(preview, "Left Angle: {:f}".format(angle_left_leg), (300, 360), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(preview, "Right Angle: {:f}".format(angle_right_leg), (300, 410), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(preview, "Right Hand Angle: {:f}".format(angle_right_hand), (300, 460), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(preview, "Two Leg Angle: {:f}".format(angle_two_leg), (300, 510), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

            # YELLOW   
            elif (( angle_left_leg >= 80 and angle_left_leg <= 90 ) or (angle_left_leg > 120 and angle_left_leg < 130)) and ( ( angle_right_leg >= 80 and angle_right_leg <= 90 ) or (angle_right_leg > 120 and angle_right_leg < 130)) and  (angle_two_leg >= 60 and angle_two_leg < 90) : # 黃色
                cv2.putText(preview, "Left Angle: {:f} ".format(angle_left_leg), (300, 360), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(preview, "Right Angle: {:f}".format(angle_right_leg), (300, 410), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(preview, "Right Hand Angle: {:f}".format(angle_right_hand), (300, 460), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(preview, "Two Leg Angle: {:f}".format(angle_two_leg), (300, 510), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            # RED
            else:
                cv2.putText(preview, "Left Angle: {:f}".format(angle_left_leg), (300, 360), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(preview, "Right Angle: {:f}".format(angle_right_leg), (300, 410), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(preview, "Right Hand Angle: {:f}".format(angle_right_hand), (300, 460), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(preview, "Two Leg Angle: {:f}".format(angle_two_leg), (300, 510), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            

        cv2.imshow('frame', preview)
        
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    # release camera
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
