from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
from pymavlink import mavutil
import time
import socket
import cv2
import numpy as np
import torch

# 연결 시도
def connectMyCopter():
    try:
        vehicle = connect('/dev/ttyS0', baud=57600, wait_ready=True)
        print("Connected to vehicle.")
        print("version : %s" % vehicle.version)
        print("Attitude : %s" % vehicle.attitude)
        return vehicle
    except APIException as e:
        print(f"Failed to connect to vehicle: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
    

print("pixhawk.py run")
vehicle = connectMyCopter()

# 시동
def arm():
    print("try Arming")
    time.sleep(2)
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(2)
    vehicle.armed=True
    while vehicle.armed==False or not vehicle.mode.name == 'GUIDED':
        print("Waiting for drone to become armed...")
        time.sleep(1)
        vehicle.mode = VehicleMode("GUIDED")
        time.sleep(2)
        vehicle.armed=True
    print("Vehicle is now armed.")
    print("OMG props are spinning!!!")
    return None

# 이륙
def takeOff(TargetAltitude):
    print("Taking off")
    time.sleep(1)
    vehicle.simple_takeoff(TargetAltitude)
    while True:
        time.sleep(1)
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= TargetAltitude:
            print("Reached target altitude")
            break
    return None

# 좌표로 이동
def goToTarget(latitude, longitude):
    targetLocation = LocationGlobalRelative(latitude, longitude, vehicle.location.global_relative_frame.alt)
    vehicle.simple_goto(targetLocation)
    print(f"Moving to target location: {latitude}, {longitude}")
    while True:
        distance = get_distance_metres(vehicle.location.global_frame, targetLocation)
        print(f"Distance to target: {distance} meters")
        if distance < 2:  # 2미터 이내로 도달하면 멈춤
            print("Reached target location")
            break
        time.sleep(1)
    return None

# 드론 위치와 목표 위치 간 거리 계산
def get_distance_metres(aLocation1, aLocation2):
    dlat = aLocation2.lat - aLocation1.lat
    dlon = aLocation2.lon - aLocation1.lon
    return np.sqrt((dlat * 1.113195e5) ** 2 + (dlon * 1.113195e5) ** 2)

# 풍선 추적 함수
def highjack():
    # YOLOv5 모델 로드
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
    model.eval()

    # 웹캠 초기화
    cap = cv2.VideoCapture(0)

    # 드론의 속도 설정
    def set_velocity_body(vehicle, vx, vy, vz):
        """이 함수를 사용해 드론의 속도를 조정할 수 있음"""
        msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0, 0, 0,    # 타임스탬프, 목표 시스템 및 컴포넌트
            mavutil.mavlink.MAV_FRAME_BODY_NED,  # 좌표계: 드론을 기준으로 NED
            0b0000111111000111,  # 속도 사용, 위치는 사용 안함
            0, 0, 0,  # x, y, z 위치
            vx, vy, vz,  # x, y, z 속도 (m/s)
            0, 0, 0,  # 가속도
            0, 0)  # 요 값 및 속도
        vehicle.send_mavlink(msg)
        vehicle.flush()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from webcam")
                break

            # 객체 탐지 수행
            results = model(frame)

            # 풍선 탐지 여부 확인
            for *box, conf, cls in results.xyxy[0]:
                x1, y1, x2, y2 = [int(i) for i in box]
                label = model.names[int(cls)]
                
                if label == 'balloons':
                    print("Balloons detected!")
                    
                    # 풍선의 중앙 좌표 계산
                    balloon_center_x = (x1 + x2) // 2
                    balloon_center_y = (y1 + y2) // 2

                    # 화면 중앙 좌표 계산
                    frame_center_x = frame.shape[1] // 2
                    frame_center_y = frame.shape[0] // 2

                    # 드론의 고도 조정 (화면 상에서 풍선이 중앙에 오도록)
                    if balloon_center_y < frame_center_y - 50:
                        print("Ascending to match balloon height")
                        set_velocity_body(vehicle, 0, 0, -0.5)  # 드론 상승
                    elif balloon_center_y > frame_center_y + 50:
                        print("Descending to match balloon height")
                        set_velocity_body(vehicle, 0, 0, 0.5)  # 드론 하강
                    else:
                        print("Maintaining altitude")
                        set_velocity_body(vehicle, 0, 0, 0)  # 고도 유지

                    # 드론의 전진/후진 조정 (풍선과 부딪히기 위해 전진)
                    balloon_width = x2 - x1  # 풍선의 너비
                    if balloon_width < 100:  # 풍선이 작게 보이면 (멀리 있을 때)
                        print("Moving forward towards the balloon")
                        set_velocity_body(vehicle, 1, 0, 0)  # 드론 전진
                    else:
                        print("Stopping, balloon is close")
                        set_velocity_body(vehicle, 0, 0, 0)  # 멈춤
                        
                    break

            # ESC키로 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

try:
    # 드론 시동 및 이륙
    arm()
    takeOff(10)  # 10미터 고도로 이륙
    
    vehicle.airspeed = 5
    vehicle.groundspeed = 5
    
    # 서버로부터 좌표 수신
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)

    print('Waiting for connection...')
    connection, address = server_socket.accept()
    print(f'Connected by {address}')

    data = connection.recv(1024).decode()
    latitude, longitude, city = data.split(',')

    print(f"Latitude: {latitude}, Longitude: {longitude}")

    # 받은 좌표로 이동
    goToTarget(float(latitude), float(longitude))

    # 풍선 추적 모드 실행
    highjack()

    # 미션 완료 후 홈으로 복귀
    print("Return to launch")
    vehicle.mode = VehicleMode("RTL")

    print("Vehicle close")
    connection.close()
    vehicle.close()

except Exception as e:
    print(f"Error: {e}")
    print("Returning to launch")
    vehicle.mode = VehicleMode("RTL")
    vehicle.close()
