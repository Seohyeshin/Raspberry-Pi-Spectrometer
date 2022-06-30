import cv2
# from PIL import Image
import numpy as np
import math

import os

k = os.getcwd()
print(k)

##변수 정의(가능하면 변경하지 말 것)

ygra = 300 ## y그래프 높이
# xgra = 25  ## x그래프 높이
gx = 0 ## x그래프 여백
gy = 60 ## y그래프 여백


## 1. 미분류 


def wavetorgb(nm):  ## 파장을 BGR로 변환하는 함수 /  파장값을 입력받으면 그에 해당하는 BGR값을 튜플로 반환

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

def imgshow(img): ##이미지 출력함수 
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def imginf(img):  ##이미지 높이 너비 채널 정보 얻기
    h,w,c = img.shape   
    return h,w,c

def pixinf(img,x,y): ## x,y위치에 있는 bgr 정보 얻기 
    bgr = img[y,x]
    return bgr


## 2. 텍스트파일 입출력


def wrtxt(q,list=[]):  ## 텍스트파일 이름과 리스트를 저장하는 함수 / 입력값 텍스트파일 이름,리스트 / 반환값: 없음
    with open('{0}.txt'.format(q),'w',encoding='utf8') as tf:
        for plz in list:
            tf.write(str(plz)+'\n')

def retxt(name): ## 텍스트파일을 읽어서 리스트로 반환하는 함수 / 입력값 텍스트파일 이름 / 반환값:리스트
    clist = []
    rf = open("{0}.txt".format(name), "r", encoding="utf8")
    for i in rf:
        q = int(i)
        clist.append(q)
    rf.close()
    return clist


## 3. 그래프 그리기(opencv이용)


mul = 3 ## 그래프 글자 크기를 설정(가능하면 변경하지 말 것)

def cvgraph(clist): ## 그래프 그리는 함수  

    lt = len(clist)
    max2 = int(max(clist))
    # print(max2)
    sketch = wave(lt)
    for i in range(lt):
        color = wavetorgb(i+380)
        y = int(clist[i])

        cv2.line(sketch,(i+int(gx/mul),ygra-int(gy/mul)),(i+int(gx/mul),ygra-y-int(gy/mul)),color,1,cv2.LINE_4)
        if i>0:
            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i-1+int(gx/mul),ygra-x-int(gy/mul)),color,1,cv2.LINE_4)
        x = y
    return sketch

def wave(lt): ## 그래프의 틀 만드는 함수  
    
    font=cv2.FONT_HERSHEY_SIMPLEX
    xl = lt*mul
    ygra1 = ygra*mul
    sketch = np.zeros((ygra1+gy,xl+gx,3),dtype=np.uint8)
    sketch.fill(255)
    for i in range(xl): ##세로선 그리기
        if i == 0:
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        if (i-20*mul)%(50*mul) == 0:
            text = str(int(380+i/mul)) + 'nm'
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(220,220,220),2,cv2.LINE_4)
            cv2.line(sketch,(i+gx,ygra1),(i+gx,ygra1),(255,0,0),2,cv2.LINE_4)
            cv2.putText(sketch,text,(i-16*mul,ygra1+gy-25),font,1,(0,0,0),2)

    for j in range(ygra1): ##가로선 그리기 
        if j == 0:
            cv2.line(sketch,(0+gx,ygra1),(xl+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        elif j%100 == 0:
            # text = str(int(j/3))
            cv2.line(sketch,(0+gx,j),(xl+gx,j),(220,220,220),2,cv2.LINE_4)
            # cv2.putText(sketch,text,(0,ygra1-j),font,1,(0,0,0),2)
    sketch = cv2.resize(sketch,(lt,ygra),interpolation=cv2.INTER_AREA)
    return sketch


## 4. 이미지정보 리스트 피크점 리스트를받아서 그래프와 피크점 생성 


def cvgraphp(clist,plist,l): ## grayscale리스트와 피크점 리스트를 받아서 그래프로 출력 l은 피크점 출력위치 선택(l=1이면 피크점 이외의 값은 맨 위에다 출력) 
    lt = len(clist)
    max2 = int(max(clist))
    # print(max2)
    sketch = wavep(clist,plist,l)
    for i in range(lt):
        color = wavetorgb(i+380)
        y = int(clist[i])
        # if cal ==1:
        #     y = cha(y,i,max2)                 ####값 보정
        # if cal ==1:
        #     y = cha1(y,i)
        # y = cha2(y,i)

        cv2.line(sketch,(i+int(gx/mul),ygra-int(gy/mul)),(i+int(gx/mul),ygra-y-int(gy/mul)),color,1,cv2.LINE_4)
        if i>0:
            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i-1+int(gx/mul),ygra-x-int(gy/mul)),color,1,cv2.LINE_4)
        x = y
    return sketch

def wavep(clist,plist,l):   ## 그래프 틀 만드는 함수(lt는 x축 변수, y축은 최대 300으로 고정(grayscale값이0~255사이값을 가지므로) 


    lt = len(clist)
    font=cv2.FONT_HERSHEY_SIMPLEX
    xl = lt*mul
    ygra1 = ygra*mul
    sketch = np.zeros((ygra1+gy,xl+gx,3),dtype=np.uint8)
    sketch.fill(255)


    for i in range(xl): ##세로선 그리기
        if i == 0:
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        if (i-20*mul)%(50*mul) == 0:
            text = str(int(380+i/mul)) + 'nm'
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(220,220,220),2,cv2.LINE_4)
            # cv2.line(sketch,(i+gx,ygra1),(i+gx,ygra1),(255,0,0),2,cv2.LINE_4)
            cv2.putText(sketch,text,(i-16*mul,ygra1+gy-25),font,1,(0,0,0),2)

    for j in range(ygra1): ##가로선 그리기 
        if j == 0:
            cv2.line(sketch,(0+gx,ygra1),(xl+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        elif j%100 == 0:
            # text = str(int(j/3))
            cv2.line(sketch,(0+gx,j),(xl+gx,j),(220,220,220),2,cv2.LINE_4)
            # cv2.putText(sketch,text,(0,ygra1-j),font,1,(0,0,0),2)

    for i in range(len(plist)): ## 피크점 표시 
        text = str(plist[i]+380)
        if l==1:
            y = int(clist[plist[i]]*mul)
            cv2.line(sketch,(int(plist[i])*3,int(ygra1-y-mul*30)),(int(plist[i]*3),ygra1),(0,0,0),2,cv2.LINE_4)
            cv2.putText(sketch,text,(int(plist[i])*3-10*mul,int(ygra1-y-mul*50)),font,1,(0,0,0),2)
        else:
            cv2.line(sketch,(int(plist[i])*3,int(mul*50)),(int(plist[i]*3),ygra1),(0,0,0),2,cv2.LINE_4)
            cv2.putText(sketch,text,(int(plist[i])*3-10*mul,int(mul*40)),font,1,(0,0,0),2)

    sketch = cv2.resize(sketch,(lt,ygra),interpolation=cv2.INTER_AREA)
    return sketch


## 5. 이미지 분석 및 기준 리스트 만들기


def colinf(img):  ## 이미지정보를 bgr튜플로 이루어진 리스트로 반환하는 함수(컴퓨터로 생성한 스펙트럼에만 사용)

    rc = []

    h,w,c = img.shape

    for i in range(0,w):
        
        col = img[3][i]
        b = int(col[0])
        g = int(col[1])
        r = int(col[2])

        rc.append((b,g,r))

    return rc

def grainf(img):  ## 이미지정보를 grayscale로 이루어진 리스트로 반환하는 함수(컴퓨터로 생성한 스펙트럼에만 사용 )

    rc = []

    h,w,c = img.shape

    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    for i in range(0,w):
        
        col = int(img[3][i])

        rc.append(col)
    
    return rc

def cvtnm(number,c): ## 380~780nm파장에서 1nm의 간격을 number만큼의 pixel로 설정하고 얻은 색 정보들을 리스트로 반환하는 함수 c를 1로 설정하면 컬러 그 외엔 흑백으로 반환
    
    nm = number

    sketch = np.zeros((10,400,3),dtype=np.uint8)  ## 스케치 높이 너비 설정 
    
    for i in range(0,400): ##기본 스펙트럼이미지 생성 
        color = wavetorgb(380+i)
        cv2.line(sketch,(i,0),(i,10),color,1,cv2.LINE_4)
        
        
    if number>1:
        dst2 = cv2.resize(sketch, dsize=(0, 0), fx=nm, fy=1, interpolation=cv2.INTER_LINEAR) ##이미지 늘리기 
    else:
        dst2 = cv2.resize(sketch, dsize=(0, 0), fx=nm, fy=1, interpolation=cv2.INTER_AREA)   ##이미지 줄이기 
    
    if c == 1:
        rc = colinf(dst2) ## bgr로 이미지 정보 저장

    else:
        rc = grainf(dst2) ## grayscale로 이미지 정보 저장 

    return rc

def stimg(img): ##이미지를 기준으로 보정값 리스트를 생성하는 함수 
    
    h,w = img.shape
    
    if w>400:
        dst2 = cv2.resize(img,(400,300), interpolation=cv2.INTER_LINEAR) ##이미지 늘리기 
    else:
        dst2 = cv2.resize(img,(400,300), interpolation=cv2.INTER_AREA)   ##이미지 줄이기 
       
    rc = imgrgb(dst2)

    return rc

def setnm(x1,x2,nm1,nm2): ## 두 픽셀x위치의 의 간격을 nm만큼의 파장길이로 설정해서 나머지 스펙트럼을 만드는 함수(구현예정)
    
    nm = nm2 - nm1
    
    pix = x2 - x1

    pix_1 = nm/pix

    col = cvtnm(pix_1,1)

    sketch = np.zeros((10,len(col),3),dtype=np.uint8)

    for i in range(0,len(col)):

        cv2.line(sketch,(i,0),(i,10),col[i],1,cv2.LINE_4)
    
    cv2.imshow("sketch",sketch)
    cv2.waitKey(0)
    cv2.destroyAllWindows

def imgrgb(img):  ##한 열의 gray값을 각각 더한후 각 열의 gray값의 평균을 구하는 함수 
    h = img.shape[0]
    w = img.shape[1]
    clist = []
    for i in range(w):
        tg = 0
        for j in range(h):
            tg += img[j,i]
        cs = int((tg)/(h))
        clist.append(cs)
    return clist


## 6. 보정작업 (프로그램 실행시 한가지만 선택할 것)


def cali1(list): ## 보정1 컴퓨터로 구한 스펙트럼을 바탕으로 보정값을 넣어서 생성  
    a = []
    for i in range(len(list)):
        k = int(list[i]*(226/gs[i]))
        if k >= 226:
            k = 226
        elif k < 29:
            k = 0
        a.append(k)
    return a

def cali2(list,cal,max): ## 보정2 cal리스트와 최댓값max를 바탕으로 보정값을 넣어서 생성  
    a = []
    for i in range(len(list)):
        k = int(list[i]*(max/cal[i]))
        if k >= max:
            k = max
        a.append(k)
    return a

def cali3(img,min):  ## 보정3 한 열에서 min값보다 큰 grayscale값을 모두 더하는 방식으로 생성
    h = img.shape[0]
    w = img.shape[1]
    clist = []
    for i in range(w):
        tg = 0
        for j in range(h):
            if img[j,i]>=min:
                tg += 1
        clist.append(int(tg*0.6))
    return clist

def cali4(list,stlist): ## 보정4 기준리스트와 유사도를 통해 생성 
    a = []
    
    for i in range(len(list)):
        if list[i]>=stlist[i]:
            k = stlist[i]/list[i]
        else:
            k = list[i]/stlist[i]
        a.append(k*200)
    return a


## 7. 피크점 구하기


def block1(clist,div):  ## 리스트를 div만큼 블록화 시킨 후 기존 데이터와 다른 새로운 리스트로 생성
    a= []
    for i in range(len(clist)):
        a.append(clist[i])
    leng = len(clist)
    if leng%div != 0:
        leng = leng - div
    for i in range(0,leng,div):
        q = 0 
        for j in range(div):
            q += clist[i+j]
        q = int(round(q/div))
        for k in range(div):
            a[i+j] = q
    return a

def block(clist,div):  ## 리스트를 div만큼 블록화시켜서 바꾸기
    a = clist
    leng = len(clist)
    if leng%div != 0:
        leng = leng - div
    for i in range(0,leng,div):
        q = 0 
        for j in range(div):
            q += a[i+j]
        q = int(round(q/div))
        for k in range(div):
            a[i+k] = q
    return a

def peak(clist,n):  ## 블록화된 리스트를 기반으로 피크점 구하기 
    a = []
    for i in range(0,len(clist)-n,int(n)):
        if i < n:
            if clist[i]>clist[i+n]:
                a.append(i)
        elif clist[i]>clist[i-n] and clist[i]>clist[i+n]:
            a.append(i)
    # print(a)
    return a



##프로그램 실행 


## 1. 보정값 기준 스펙트럼 리스트 생성 (produce mono spcetrum info list)

## 1-1. 컴퓨터로 그린 스펙트럼값을 기준으로 정한 보정값 

gs = cvtnm(1,0) 

## 1-2. 이미지로 받은 스펙트럼값을 기준으로 정한 보정값 

std = cv2.imread("stimg.png")                 ## 사진으로 받은 이미지를 기준으로 정한 보정값      
std = cv2.flip(std,1)                       ## 이미지 좌우반전(파장은 380~780nm(보라색파장부터 빨간색파장까지)이미지정렬이 되어야함 
std = cv2.cvtColor(std,cv2.COLOR_BGR2GRAY)  ## 이미지를 흑백으로 변환하기 convert img to grapscale

gg = stimg(std) ##이미지보강 기준점 생성 
mg = max(gg)    ##이미지보강 기준 max값 생성 




## 2.이미지를 불러와서 grayscale값을 리스트로 저장 후 txt파일로 덮어쓰기 및 출력 

ori = cv2.imread("WWTTFF.png") 
ori = cv2.resize(ori,(400,300),interpolation=cv2.INTER_AREA)
ori = cv2.cvtColor(ori,cv2.COLOR_BGR2GRAY)
list1 = imgrgb(ori)                                ## 이미지 정보 리스트에 저장  
name = str(input("Enter the name of img info txt file that you want to save "))   ## 이미지 정보 리스트 이름 입력 후 메모장에 저장
wrtxt(name,list1)                                  
name1 = str(input("Enter the name of img info txt file that you want to find "))         ## 메모장에 있는 이미지정보 리스트로 불러오기 
readtxt = retxt(name1)     
print(readtxt)                      
img = cvgraph(readtxt)                                   ## 그래프 그리기 draw graph
imgshow(img)


q = list1

# 3. 각 보정방법에 따른 피크점 구하기 

##   pn은 보정값으로 UI를 통해 이 값을 변경시킬 수 있도록 만들어야함  

# 3-1. 컴퓨터로 그린 스펙트럼을 보정값으로 사용

s = cali1(q) 

# for i in range(1,25):
#     pn = i
#     second = block1(s,pn)
#     peak1 = peak(second,pn)
#     img = cvgraphp(s,peak1,0)
#     img1 = cvgraphp(second,peak1,0)
#     cv2.imshow('originalgraph1',img)
#     cv2.imshow('blockgraph1',img1)
#     cv2.waitKey(250)
# cv2.destroyAllWindows()

# # 3-2. 이미지로 받은 스펙트럼을 보정값으로 사용 

# s = cali2(q,gg,mg) 

# for i in range(1,25):
#     pn = i
#     second = block1(s,pn)
#     peak1 = peak(second,pn)
#     img = cvgraphp(s,peak1,0)
#     img1 = cvgraphp(second,peak1,0)
#     cv2.imshow('originalgraph2',img)
#     cv2.imshow('blockgraph2',img1)
#     cv2.waitKey(250)
# cv2.destroyAllWindows()
# # 3-3. 이미지의 특정 grayscale이상의 값을 갖는 값을 기준으로 리스트를 생성

# s = cali3(ori,25)  

# for i in range(1,25):
#     pn = i
#     second = block1(s,pn)
#     peak1 = peak(second,pn)
#     img = cvgraphp(s,peak1,0)
#     img1 = cvgraphp(second,peak1,0)
#     cv2.imshow('originalgraph3',img)
#     cv2.imshow('blockgraph3',img1)
#     cv2.waitKey(250)
# cv2.destroyAllWindows()
# # 3-4. 기준 리스트와 유사도로 리스트를 생성 

# s = cali4(q,gs)  ##컴퓨터로 생성한 스펙트럼의 리스트인 gs를 기준으로 생성

# for i in range(1,25):
#     pn = i
#     second = block1(s,pn)
#     peak1 = peak(second,pn)
#     img = cvgraphp(s,peak1,0)
#     img1 = cvgraphp(second,peak1,0)
#     cv2.imshow('originalgraph4',img)
#     cv2.imshow('blockgraph4',img1)
#     cv2.waitKey(250)
# cv2.destroyAllWindows()



#카메라를 통해 실시간으로 그래프 그리기(여기서는 3-4번 보정방법을 사용하였고 보정값은 3으로 설정)


cap = cv2.VideoCapture(0,cv2.CAP_ANY)  ## for laptop camera 
# cap = cv2.VideoCapture(0,cv2.CAP_V4L) ## for raspberry camera 

pn = 3 ##보정값 

while cap.isOpened():

    ret, img = cap.read()
    
    img = cv2.resize(img,(400,300))
    img = cv2.flip(img,1)
    sketch = img[0:300,0:400]
    cv2.imshow('camera',sketch)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    list1 = imgrgb(img)
    list1 = cali4(list1,gs)

    second = block(list1,pn)
    peak1 = peak(second,pn)
    img = cvgraphp(list1,peak1,1)

    cv2.imshow('result', img)
    
    if cv2.waitKey(25) == ord('q'):
        
        break
cv2.destroyAllWindows()
cap.release() # 동영상 파일 닫고 메모리 해제
