import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

##함수 정의 

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

##한 열의 rgb값을 각각 더한후 각 열의 rgb값의 평균을 구하는 함수 //리스트값으로 저장+ 텍스트파일로 저장 

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
    return clist

##이미지에서 얻은 rgb값을 이용해 다시 그림을 그리는 함수 

def imgdraw(img): 
    h = imginf(img)[0]
    w = imginf(img)[1]
    sketch = np.zeros((h,w,3),dtype=np.uint8)
    for i in range(w):
        for j in range(h):
            r = int(pixinf(img,i,j)[2])
            g = int(pixinf(img,i,j)[1])
            b = int(pixinf(img,i,j)[0])
            color = (b,g,r)
            cv2.line(sketch,(i,j),(i,j),color,1,cv2.LINE_4)
    imgshow(sketch)

## 텍스트파일 이름과 리스트를 저장하는 함수 / 입력값 텍스트파일 이름,리스트 / 반환값: 없음

def wrtxt(q,list=[]):
    with open('{0}.txt'.format(q),'w',encoding='utf8') as tf:
        for plz in list:
            tf.write(str(plz)+'\n')

## 텍스트파일을 읽어서 리스트로 반환하는 함수 / 입력값 텍스트파일 이름 / 반환값:리스트

def retxt(name):
    clist = []
    rf = open("{0}.txt".format(name), "r", encoding="utf8")
    for i in rf:
        i = float(i[:-2])
        clist.append(i)
    rf.close()
    return clist

## 그래프 그리는 함수 

def drawgra(img,rlist=[]):
    a =[300,400,500,600]
    b = [100,20,300,50]
    x1 = img.shape[1]
    x = list(range(x1))


    y = rlist
    plt.plot(x, y)
    plt.plot(a,b)
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



##실행

ori = cv2.imread("img1.jpg", cv2.COLOR_BGR2GRAY)    ## 이미지를 흑백으로 불러오기
list1 = imgrgb(ori)                                ## 이미지 정보 리스트에 저장 
name = str(input("저장할 텍스트파일 이름을 입력"))   ## 이미지 정보 리스트 이름 입력 후 메모장에 저장
wrtxt(name,list1)                                  
name1 = str(input("찾을 파일 이름을 입력"))         ## 메모장에 있는 리스트 불러오기
readtxt = retxt(name1)                             ## 그래프 그리기  
drawgra(ori,readtxt)





## 이미지를 받는 방법? 
## 텍스트파일로 리스트 저장  
## 이 텍스트파일을 읽어오는 것
## 그래프 겹치기 
## 그래프 모양 꾸미기 
## 그래프 정보