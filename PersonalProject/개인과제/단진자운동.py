import cv2 
import numpy as np 



def pene(angle):

    sketch1 = np.zeros((750,1500,3),dtype=np.uint8)

    y_line = 175
    x_line = 750

    cv2.line(sketch1,(1,375),(1500,375),(255,255,255),1,cv2.LINE_4)
    cv2.line(sketch1,(750,1),(750,750),(255,255,255),1,cv2.LINE_4)

    g = 9.8

    Length = 150 ## 실의 길이 

    f_theta = angle

    theta = 180 - f_theta ## 



    d_theta = 0 ##  각속도
    

    d_theta2_1 = 0


    for i in range(1000):

        sketch = np.zeros((750,1500,3),dtype=np.uint8)
        sketch[:,:] = sketch1[:,:]


        ## 첫번째 진자

        angle_speed = g*np.sin(np.radians(theta))/Length ## w = v/r 공식 이용해서 얻은 각속도 값

        d_theta += angle_speed ## 각속도의 변화
        
        theta += d_theta  ## 각도의 값 

        x = int(Length*np.sin(np.radians(theta)))
        y = int(Length*np.cos(np.radians(theta)))


        cv2.line(sketch,(x_line,y_line),(x_line+x,y_line-y),(255,255,255),1,cv2.LINE_AA)
        cv2.circle(sketch,(x_line+x,y_line-y),20,(255,255,255),1,cv2.LINE_AA)
        
        
        ## y축의 변화

        cv2.line(sketch1,(x_line+x,y_line+i),(x_line+x,y_line+i),(255,255,255),1,cv2.LINE_4) 
        cv2.line(sketch,(x_line+x,y_line-y),(x_line+x,y_line+i),(255,255,255),1,cv2.LINE_4)

        ## x축의 변화 

        cv2.line(sketch1,(x_line+i,y_line-y),(x_line+i,y_line-y),(255,255,255),1,cv2.LINE_4)
        cv2.line(sketch,(x_line+x,y_line-y),(x_line+i,y_line-y),(255,255,255),1,cv2.LINE_4)

        # cv2.circle(sketch,(x_line+x,y_line-y),20,(255,255,255),1,cv2.LINE_AA)
        cv2.imshow("gg",sketch)
        cv2.waitKey(10)


pene(75)