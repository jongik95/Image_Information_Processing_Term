import cv2
import LaneModule, ObjectModule2
from time import sleep

def printCarStatus(speed, angle) :
    print('Car Speed :', speed, 'Steer Angle :', angle)

def speedUp(speed, maxSpeed) :
    if speed > maxSpeed :
        newSpeed = speed - 1
    elif speed + 0.5 >= maxSpeed :
        newSpeed = maxSpeed
    elif speed + 0.5 < maxSpeed :
        newSpeed = speed + 0.5
    
    return newSpeed
        
def maxSpeedLimit(text) :
    ret = None
    if text == '30' :
        ret = 30
    elif text == '50' :
        ret = 50
    return ret

cam = cv2.VideoCapture('./test.mp4')

if cam.isOpened() :
    capTime = 31
    nowSpeed = 0
    maxSpeed = 50
    forDis = 0

    try :
        while True :
            if(cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT)):
                cam.open('./test.mp4')

            textObject = None
            ret, frame = cam.read()
            
            steer = LaneModule.laneTracking(frame)
            if capTime > 30 :
                capTime = 0
                textObject = ObjectModule2.findObject(frame)

            if textObject == 'STOP' or textObject == '5TOP' or textObject == 'CTOP' or textObject == 'ST0P' :
                print('Car Stop 3 Seconds')
                nowSpeed = 0
                sleep(3)
            elif textObject != None :
                tmp = maxSpeedLimit(textObject)
                if tmp != None :
                    maxSpeed = tmp
            
            printCarStatus(nowSpeed, steer)
            nowSpeed = speedUp(nowSpeed, maxSpeed)

            capTime += 1
            if cv2.waitKey(30) & 0xff == 27 :
                break
    except Exception as e :
        print(e)
    finally :
        cv2.destroyAllWindows()
        cam.release()
else :
    print('NoVideo')
