
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

##이미지 출력함수 

def imgshow(img): 
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

##이미지 높이 너비 채널 정보

def imginf(img):
    h,w,c = img.shape   
    return h,w,c

## x,y위치에 있는 bgr 정보 출력 

def pixinf(img,x,y): 
    bgr = img[y,x]
    return bgr

##한 열의 rgb값을 각각 더한후 각 열의 rgb값의 평균을 구하는 함수 //리스트값으로 저장 

def imgrgb(img):  
    h = imginf(img)[0]
    w = imginf(img)[1]
    clist = []
    for i in range(w):
        tg = 0
        for j in range(h):
            tg += int(pixinf(img,i,j)[0])
        cs = (tg)/(h)
        clist.append(cs)
        # print("{0}번째 열의 색상값".format(i))
        # print("R:{0:.2f} G:{1:.2f} B:{2:.2f}".format(tr/h,tg/h,tb/h))
        # HSV = RtoH(tr/h,tg/h,tb/h)
        # print("H:{0:.2f} S:{1:.2f} V:{2:.2f}".format(HSV[0],HSV[1],HSV[2]))
    return clist
##이미지에서 얻은 rgb값을 이용해 다시 그림을 그리는 함수 

# def imgdraw(img): 
#     h = imginf(img)[0]
#     w = imginf(img)[1]
#     sketch = np.zeros((h,w,3),dtype=np.uint8)
#     for i in range(w):
#         for j in range(h):
#             r = int(pixinf(img,i,j)[2])
#             g = int(pixinf(img,i,j)[1])
#             b = int(pixinf(img,i,j)[0])
#             color = (b,g,r)
#             cv2.line(sketch,(i,j),(i,j),color,1,cv2.LINE_4)
#     imgshow(sketch)

##rgb를 HSV로 변환하는 함수 




##동영상 출력 함수

def showvid(video):
    while video.isOpened():
        ret,frame = video.read()
        if not ret:
            print("더이상 가져올 프레임이 없음")
            break
        
        cv2.imshow('video',frame)
    
        if cv2.waitKey(25) == ord('x'):
            print("사용자 입력에 의해 종료")
            break  
    video.release() #자원해제
    cv2.destroyAllWindows()



##얻은 rgb값의 위치별 분포 -- 실패

# def imgrgb(img): 
#     w = imginf(img)[1]
#     h = imginf(img)[0]
#     sketch = np.zeros((300,w,3),dtype=np.uint8)
#     for i in range(w):
#         for j in range(h):
#             r = int(pixinf(img,i,j)[2])
#             g = int(pixinf(img,i,j)[1])
#             b = int(pixinf(img,i,j)[0])
#             color = (b,g,r)
#             cv2.line(sketch,(i,299-r),(i,300-r),(0,0,255),1,cv2.LINE_AA)
#             cv2.line(sketch,(i,299-g),(i,300-g),(0,255,0),1,cv2.LINE_AA)
#             cv2.line(sketch,(i,299-b),(i,300-b),(255,0,0),1,cv2.LINE_AA)
#     imgshow(sketch)

ori = cv2.imread("img1.jpg", cv2.COLOR_BGR2GRAY)

x1 = ori.shape[1]
print(type(x1))
x = list(range(x1))
y = imgrgb(ori)
plt.plot(x, y)
n = len(y) - 12
Y = []
X = []
for i in range(n) :
    j= i+1
    if y[j] != 0:
        if (y[j]-y[j-10]) > 5 and (y[j]-y[j+10]) >5:
            Y.append(y[j])
            X.append(x[j])

plt.scatter(X,Y)
plt.show()

# vid = cv2.VideoCapture('video.mp4')
# showvid(vid)

# print(imginf(ori))

# imgdraw(ori)

## 이미지를 받는 방법 
## 텍스트파일로 리스트 저장  
## 이 텍스트파일을 읽어오는 것
## 그래프 겹치기 
## 그래프 모양 꾸미기 
## 그래프 정보