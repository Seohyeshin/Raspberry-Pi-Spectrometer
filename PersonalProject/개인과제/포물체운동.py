import math
import numpy as np
import cv2

color = (255,255,255)

def cos(a):
    if a%180 == 0:
        q = 0
    else:
        q = math.cos(math.radians(a))
    return q

def sin(a):
    if (a+180)%180 ==0:
        q= 0
    else:
        q  = math.sin(math.radians(a))
    return q

sketch = np.zeros((750,1500,3),dtype=np.uint8)

h = 750
w = 1500

color = (255,255,255)

cv2.line(sketch,(0,h-100),(w,h-100),color,1,cv2.LINE_4)
cv2.line(sketch,(50,0),(50,h),color,1,cv2.LINE_4)


xx = 50
yy = 100

mul = 100

g = 9.8


def hmm(vel,angle):
    i = 0
    while(1):
        i += 1
        t = i*0.005


        x_s = int(mul*(vel*cos(angle)*t))
        y_s = int(mul*(vel*sin(angle)*t - g*t*t))

        cv2.line(sketch,(xx+x_s,750 - (yy+y_s)),(xx+x_s,750 - (yy+y_s)),color,1,cv2.LINE_4)

        if i>1 and yy+y_s < 100:
            break
        else:
            cv2.imshow('hh',sketch)
            cv2.waitKey(5)
        

hmm(15,60) ## 속도(지금은 별 의미 없음), 각도 입력 