import cv2
import numpy as np
import graph_color

ygra = 300 ## y그래프 높이
gx = 0 ## x그래프 여백
gy = 60 ## y그래프 여백
mul = 3
nmnm = []

i = np.zeros((0,400,1),dtype=np.uint8) # for i in range(400): nmnm.append(i)

## 그래프 그리기 함수

def cvgra(clist,blist): ## 그래프 그리는 함수  

    lt = len(clist)
    sketch = wave(lt)
    draw(sketch,clist)
    draw(sketch,blist)

    return sketch

def wave(lt): ## 그래프의 틀 만드는 함수  
    global nmnm
    font=cv2.FONT_HERSHEY_SIMPLEX
    xl = lt*mul
    ygra1 = ygra*mul
    sketch = np.zeros((ygra1+gy,xl+gx,3),dtype=np.uint8)
    sketch.fill(255)
    for i in range(xl): ##세로선 그리기
        if i == 0:
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        if (i-20*mul)%(50*mul) == 0:

            text = str(int(380 + (i/mul)))
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(220,220,220),2,cv2.LINE_4)
            cv2.putText(sketch,text,(i-11*mul,ygra1+gy-25),font,1,(0,0,0),2)

    for j in range(ygra1): ##가로선 그리기 
        if j == 0:
            cv2.line(sketch,(0+gx,ygra1),(xl+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        elif j%100 == 0:
            cv2.line(sketch,(0+gx,j),(xl+gx,j),(220,220,220),2,cv2.LINE_4)
    sketch = cv2.resize(sketch,(lt,ygra),interpolation=cv2.INTER_AREA)
    return sketch

def draw(sketch,clist):
    lt = len(clist)
    for i in range(lt):
        color = graph_color.wavetorgb(i+380)
        y = int(clist[i])

        cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i+int(gx/mul),ygra-int(gy/mul)),color,1,cv2.LINE_4)
        if i>0:

            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i-1+int(gx/mul),ygra-x-int(gy/mul)),(0,0,0),1,cv2.LINE_AA)
        x = y
    return sketch

def pe(img,x): ## x위치에 있는 값을 반환 

    text = str(x + 380)
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.line(img,(x,0),(x,280),(0,0,0),1,cv2.LINE_4)
    cv2.putText(img,text,(165,40),font,1,(0,0,0),2)


## 이미지에서 자동으로 피크점 찾기 

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

def yblock(clist,div):
    qlist =[]

    for i in range(len(clist)):
        qlist.append(int(clist[i]/div)*div)
    
    return qlist
    
## 피크점 그래프 그리기

def cvgraphp(clist,plist,l,pn): ## grayscale리스트와 피크점 리스트를 받아서 그래프로 출력 l은 피크점 출력위치 선택(l=1이면 피크점 이외의 값은 맨 위에다 출력) 
    lt = len(clist)

    sketch = wavep(clist,plist,l,pn)

    for i in range(0,lt,pn):
        color = graph_color.wavetorgb(380+i)
        y = int(clist[i])

        if i < lt-pn:
            yy = int(clist[i+pn])
            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i+pn+int(gx/mul),ygra-yy-int(gy/mul)),(0,0,0),1,cv2.LINE_AA)
        if i >= lt-pn:
            yy = int(clist[399])
            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i+pn+int(gx/mul),ygra-yy-int(gy/mul)),(0,0,0),1,cv2.LINE_AA)


    return sketch

def wavep(clist,plist,l,pn):   ## 그래프틀과 피크점 표시 그리는 함수(lt는 x축 변수, y축은 최대 300으로 고정(grayscale값이0~255사이값을 가지므로) 


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

            text = str(int(380 + (i/mul)))
            cv2.line(sketch,(i+gx,0),(i+gx,ygra1),(220,220,220),2,cv2.LINE_4)
            cv2.putText(sketch,text,(i-11*mul,ygra1+gy-25),font,1,(0,0,0),2)

    for j in range(ygra1): ##가로선 그리기 
        if j == 0:
            cv2.line(sketch,(0+gx,ygra1),(xl+gx,ygra1),(0,0,0),3,cv2.LINE_4)
        elif j%100 == 0:
            cv2.line(sketch,(0+gx,j),(xl+gx,j),(220,220,220),2,cv2.LINE_4)


    for i in range(len(plist)): ## 피크점 표시 
        text = str(380+plist[i]+int(pn/2))

        if l==1:
            y = int(clist[plist[i]]*mul)
            cv2.line(sketch,(int(plist[i])*3,int(ygra1-y-mul*30)),(int(plist[i])*3,int(ygra1-y-mul*15)),(0,0,0),2,cv2.LINE_4)
            cv2.putText(sketch,text,(int(plist[i])*3-10*mul,int(ygra1-y-mul*50)),font,1,(0,0,0),2)
        else:
            cv2.line(sketch,(int(plist[i]+0.5*pn)*3,int(mul*50)),(int(plist[i]*3),int(mul*50)),(0,0,0),2,cv2.LINE_4)
            cv2.putText(sketch,text,(int(plist[i]+0.5*pn)*3-10*mul,int(mul*20)),font,1,(0,0,0),2)

    sketch = cv2.resize(sketch,(lt,ygra),interpolation=cv2.INTER_AREA)
    return sketch

    