from cmath import cosh
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

def cyle(r,angle): ##angle 경사면의 각도 
    
    mul = 1 

    ##경사면 설정 

    w = 700 
    h = 0  



    slength = 700*mul 

    sh = sin(angle)*slength 

    sw = slength*cos(angle) 


    sketch = np.zeros((750,1500,3),dtype=np.uint8)

    cv2.line(sketch,(h-int(sw),750-w-int(sh)),(h,750-w),color,1,cv2.LINE_4)

    cv2.line(sketch,(h+int(sw),750-w+int(sh)),(h,750-w),color,1,cv2.LINE_4)

    cv2.line(sketch,(h+int(sw),750-w+int(sh)),(h+int(sw)+100,750-w+int(sh)),color,1,cv2.LINE_4)

    g = 9.8*mul  

    gf = g*sin(angle)

    m = 0.028

    by1 = 1/((2**0.5)/((10/7)**0.5))

    i = 0

    while(1):
        i += 1
    
    
        color3 = (255,255,255)


        t  = mul*i*0.001 ##시간간격

        rad = r*mul     ##반지름

        cmx1 = 0.5*gf*t*t*cos(angle)*by1 ##원의 x중심
    
        cmy1 = -0.5*gf*t*t*sin(angle)*by1##원의 y중심
        
        x = (cmx1-math.sin(cmx1))+sin(angle)  
        y = (cmy1+(1-math.cos(cmx1)))+cos(angle)-1 

        x = int(x*rad) ## 반지름 
        y = int(y*rad)

        
        if i%20 == 0:
            cmx2 = h+int(rad*cmx1+rad*sin(angle))  ##원의 x위치 
            cmy2 = 750-w-int(rad*cmy1+rad*cos(angle))
            a = (cmx2,cmy2) ##원의 중심위치 

            if  750-w+sh <= cmy2 + rad:
                break

            sketch2 = np.zeros((750,1500,3),dtype=np.uint8)

            sketch2[0:750,0:1500] = sketch[0:750,0:1500]

            cv2.line(sketch,(cmx2,cmy2),(cmx2,cmy2),(0,0,255),1,cv2.LINE_4) ##원의 중심 
            cv2.line(sketch2,a,(x+h,750-w-y),color3,2,cv2.LINE_AA)   ## 원의 반지름 
            cv2.circle(sketch2,a, rad, color3, thickness=1, lineType=cv2.LINE_4) ## 원의 움직임

            cv2.imshow('gg',sketch2)
            cv2.waitKey(5)

    cv2.destroyAllWindows

cyle(10,45)  ## 원의 반지름과 각도 입력, 0~90 사이의 각도 입력 가능 
