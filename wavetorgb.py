import numpy as np 
import cv2


def wavetorgb(nm): ## 파장을 BGR로 변환하는 함수 /  파장값을 입력받으면 그에 해당하는 파장값을 튜플로 반환 

    gamma = 0.8
    max_intensity = 255
    factor = 0

    rgb = {"R": 0, "G": 0, "B": 0}

    if 380 <= nm <= 439:
        rgb["R"] = -(nm - 440) / (440 - 380)
        rgb["G"] = 0.0
        rgb["B"] = 1.0
    elif 440 <= nm <= 489:
        rgb["R"] = 0.0
        rgb["G"] = (nm - 440) / (490 - 440)
        rgb["B"] = 1.0
    elif 490 <= nm <= 509:
        rgb["R"] = 0.0
        rgb["G"] = 1.0
        rgb["B"] = -(nm - 510) / (510 - 490)
    elif 510 <= nm <= 579:
        rgb["R"] = (nm - 510) / (580 - 510)
        rgb["G"] = 1.0
        rgb["B"] = 0.0
    elif 580 <= nm <= 644:
        rgb["R"] = 1.0
        rgb["G"] = -(nm - 645) / (645 - 580)
        rgb["B"] = 0.0
    elif 645 <= nm <= 780:
        rgb["R"] = 1.0
        rgb["G"] = 0.0
        rgb["B"] = 0.0

    if 380 <= nm <= 419:
        factor = 0.3 + 0.7 * (nm - 380) / (420 - 380)
    elif 420 <= nm <= 700:
        factor = 1.0
    elif 701 <= nm <= 780:
        factor = 0.3 + 0.7 * (780 - nm) / (780 - 700)

    if rgb["R"] > 0:
        rgb["R"] = int(max_intensity * ((rgb["R"] * factor) ** gamma))
    else:
        rgb["R"] = 0

    if rgb["G"] > 0:
        rgb["G"] = int(max_intensity * ((rgb["G"] * factor) ** gamma))
    else:
        rgb["G"] = 0

    if rgb["B"] > 0:
        rgb["B"] = int(max_intensity * ((rgb["B"] * factor) ** gamma))
    else:
        rgb["B"] = 0

    return (rgb["B"], rgb["G"], rgb["R"])

def cvtnm(number): ## 1nm의 간격을 number만큼의 pixel로 설정하는 함수 
    
    nm = number

    sketch = np.zeros((25,400,3),dtype=np.uint8)  ## 스케치 높이 너비 설정 

    
    for i in range(0,400): ##기본 스펙트럼이미지 생성 

        color = wavetorgb(380+i)
        cv2.line(sketch,(i,0),(i,25),color,1,cv2.LINE_4)
    if number>1:
        dst2 = cv2.resize(sketch, dsize=(0, 0), fx=nm, fy=1, interpolation=cv2.INTER_LINEAR) ##이미지 늘리기 
    else:
        dst2 = cv2.resize(sketch, dsize=(0, 0), fx=nm, fy=1, interpolation=cv2.INTER_AREA)   ##이미지 줄이기 
    
    cv2.imshow("hh",dst2)
    cv2.waitKey(0)
    cv2.destroyAllWindows

def setnm(x1,x2,nm): ## 두 간격을 nm만큼의 파장으로 설정해서 나머지 스펙트럼을 만드는 함수(구현예정)
    
    pass

##wavetorgb함수를 이용하여 그린 스펙트럼 이미지 

sketch1 = np.zeros((200,400,3),dtype=np.uint8)

for i in range(0,400): 

    color = wavetorgb(380+i)
    cv2.line(sketch1,(i,0),(i,200),color,1,cv2.LINE_4)

cv2.imshow("hh",sketch1)
cv2.waitKey(0)
cv2.destroyAllWindows

