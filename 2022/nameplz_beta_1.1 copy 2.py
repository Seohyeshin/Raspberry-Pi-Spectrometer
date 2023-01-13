import cv2
import numpy as np
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
from tkinter import filedialog

ygra = 300 ## y그래프 높이
gx = 0 ## x그래프 여백
gy = 60 ## y그래프 여백

mul = 3

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

    return (rgb["R"], rgb["G"], rgb["B"])

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
        color = wavetorgb(i+380)
        y = int(clist[i])


        cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i+int(gx/mul),ygra-int(gy/mul)),color,1,cv2.LINE_4)
        if i>0:

            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i-1+int(gx/mul),ygra-x-int(gy/mul)),(0,0,0),1,cv2.LINE_AA)
        x = y
    return sketch


## 이미지에서 특정값 찾기 

def mdim(img,loc): ## y(loc)위치에 있는 grayscale값 얻어서 리스트로 반환 
    h,w,C = img.shape
    a = []
    imgg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    for i in range(w):
        a.append(imgg[loc,i])

    return a

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
        color = wavetorgb(380+i)
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


## 파장계산(구현예정)
global ihatethis

iht = [0,0,0,0]

def waca():     

    global setnm,nmnm,cap1

    sx = setnm[0]
    bx = setnm[1]
    sn = setnm[2]
    bn = setnm[3]

    
    px1 = (bn-sn)/(bx-sx) ## 1픽셀당 파장(= nm/px)

    def cpx(nm):
        px = nm/px1
        return int(px)

    stx = sx - cpx((sn-380)) ## 파장 시작 이미지 픽셀 위치 
    stn = 380                ## 이미지 시작 파장 
    if stx<=1:
        stx = 1
        stn = int(sn - px1*(sx-stx))


    btx = bx + cpx((780-bn)) ## 파장 끝 이미지 픽셀 위치
    enn = 780               ## 이미지 끝 파장 
    if btx>=400:
        btx = 400                  ## 파장 끝 이미지 픽셀 위치
        enn = int(bn + (400-bx)*px1)    ## 이미지 끝에서의 파장 
    
    iht[0] = stx 
    iht[1] = stn
    iht[2] = btx
    iht[3] = enn


    sketch1 = np.zeros((300,btx-stx,3),dtype=np.uint8)
    sketch1[0:300,0:btx-stx] = cap1[0:300,stx:btx]
    if stn == 380 and enn == 780:
        sketch1 = cv2.resize(sketch1,(400,300))
        return sketch1

    else:
        sketch2 = np.zeros((300,400,3),dtype=np.uint8)
        sketch1 = cv2.resize(sketch1,(enn-stn,300))
        sketch2[0:300,stn-380:enn-380]=sketch1[0:300,0:enn-stn]
        return sketch2

    ## 이미지 시작위치 구하기 


## UI부분 

win = Tk()

win.geometry("800x625") 

label1 =Label(win) 
label1.grid(row=0, column=0)

## 라즈베리파이에 실행시엔 반드시 for desktop부분을 삭제 또는 주석처리 한 뒤 아래 for raspberry을 주석 해제하여 실행할 것


label =Label(win)
label.grid(row=0, column=1)


global cap1   ##카메라 이미지
global graph1 ##그래프 이미지 
global loc ## 카메라 y축 위치
global pn  ## 이미지 피크점 조절
global px  ## 뭐엿더라
global gc  ## 이미지 밝기
global bt1,bt2,bt3,bt4,bt5 ## 버튼1,2,3,4
global x1,x2 ## 그래프 x1 x2 위치 
global stx ## 그래프 기준점 
global nm1,nm2 ## x1 x2에서 그래프 파장
global setnm ## 파장보정값
global linec ## 선 색 변경 
global select_img ## 카메라 or 이미지 선택 

lox = 0
loy = 0
loc = 150
pn = 5
px = 1
gc = 0
bt1 = -1
bt2 = -1
bt3 = -1
bt4 = -1
bt5 = -1
sy = 100
sx = 400
x1 = 25
x2 = 375
nm1 = 380
nm2 = 780
setnm = [1,400,380,780]
nmnm = []
stx = 0
linec = 1
select_img = 1

for i in range(400):
    nmnm.append(i)


## 스케일 조절(왼쪽 부분 )

 
yloc1 = Label(win, text=' Set Y location ',bg='#50E0F0')  ## 이미지에서 y 위치 조정
yloc1.place(x=1, y=302,height=28,width=400)

def yloc(self):
    global loc
    loc = int(scale1.get())

yloc11 = Label(win, text='',bg='#ADFAFA')
yloc11.place(x=1, y=330,height=40,width=400)

style1 = ttk.Style()
style1.configure("TScale", background="#ADFAFA")


scale1 = ttk.Scale(win,command= yloc, from_=1, to=299, value=0, length=300, orient="horizontal", style="TScale")
scale1.place(x=50, y=330,height=42,width=300)


LAY = Label(win, text=' ',bg='#50E0F0')
LAY.place(x=1, y=430,height=40,width=400)

grpn44 = Label(win, text=' Set X1 ',background="#50E0F0")  ## 카메라에서 x1 위치 조정
grpn44.place(x=1, y=440,height=30,width=400)

def grpn4(self):  
    global x1
    x1 = int(scale4.get())

yloc11 = Label(win, text='',bg='#ADFAFA')
yloc11.place(x=1, y=470,height=40,width=400)

scale4 = ttk.Scale(win,orient='horizontal',from_=1, to=400,command=grpn4, length=300)
scale4.place(x=50, y=470,height=40,width=300)



grpn55 = Label(win, text=' Set X2 ',background="#50E0F0")  ## 카메라에서 x2 위치 조정 
grpn55.place(x=1, y=510,height=30,width=400)

def grpn5(self):
    global x2
    x2 = int(scale5.get())

grpn55 = Label(win, text=' ',background="#ADFAFA")  
grpn55.place(x=1, y=540,height=70,width=400)

scale5 = ttk.Scale(win,orient='horizontal',from_=1, to=400,command=grpn5, length=300)
scale5.place(x=50, y=540,height=40,width=300)




## 스케일 조절(오른쪽 부분)

grpn22 = Label(win, text=' Set brightness ',background="#50E0F0")   ## 밝기 조절 
grpn22.place(x=403, y=375,height=24,width=400)

def grpn2(self):
    global gc
    gc = int(scale2.get())

qqw = Label(win, text='',bg='#ADFAFA')
qqw.place(x=403, y=395,height=40,width=400)


scale2 = ttk.Scale(win,orient='horizontal',from_=-255, to=255,command=grpn2, length=300)
scale2.place(x=450, y=395,height=40,width=300)


def switch_peak1():                 ## 그래프에서 찾을 x값 위치 조정

    qqw = Label(win, text='',bg='#50E0F0')
    qqw.place(x=726, y=302,height=40,width=100)

    grpn11 = Label(win, text=' Find peak by manual ',bg='#50E0F0')  
    grpn11.place(x=401, y=302,width=275,height=28)

    qqw = Label(win, text='',bg='#ADFAFA')
    qqw.place(x=401, y=330,height=40,width=400)

    def grpn1(self):
        global px
        px = int(scale3.get()-380)

    
    scale3 = ttk.Scale(win,orient='horizontal',from_=380, to=779,command=grpn1, length=300,style="TScale")
    scale3.set(px)
    scale3.place(x=450, y=330,height=40,width=300)

    qqw = Label(win, text='',bg='WHITE') ## 중앙선
    qqw.place(x=402, y=301,height=325,width=2)


switch_peak1()


def switch_peak2():                 ## 자동으로 피크점 구하기 

    qqw = Label(win, text='',bg='#50E0F0')
    qqw.place(x=726, y=302,height=40,width=100)

    grpn11 = Label(win, text=' Find peak by auto ',bg='#50E0F0') 
    grpn11.place(x=401, y=302,width=275,height=28)

    qqw = Label(win, text='',bg='#ADFAFA')
    qqw.place(x=401, y=330,height=40,width=400)

    def auto(self):
        global pn
        pn = int(scale33.get())

    scale33 = ttk.Scale(win,orient='horizontal',from_=1, to=25,command=auto, length=300)
    scale33.set(pn)
    scale33.place(x=450, y=330,height=40,width=300)

    qqw = Label(win, text='',bg='WHITE') ## 중앙선
    qqw.place(x=402, y=301,height=325,width=2)



grpn66 = Label(win, text=' Set Nm1 ',background="#50E0F0")  ## 사진에서 파장값1 조정 
grpn66.place(x=401, y=440,height=30,width=400)

def grpn6(self): 
    global nm1
    nm1 = int(scale6.get())

scale6 = Scale(win,orient='horizontal',resolution=1,from_=380, to=780,command=grpn6, length=300,background="#ADFAFA")
scale6.place(x=425, y=470,height=40,width=350)



grpn77 = Label(win, text=' Set Nm2 ',background="#50E0F0")  ## 사진에서 파장값2 조정 
grpn77.place(x=401, y=510,height=30,width=400)

def grpn7(self):
    global nm2
    nm2 = int(scale7.get())

scale7 = Scale(win,orient='horizontal',resolution=1,from_=380, to=780,command=grpn7, length=300,background="#ADFAFA")
scale7.place(x=425, y=540,height=40,width=350)




## 버튼 

yloc11 = Label(win, text='',bg='#FFFFFF')
yloc11.place(x=1, y=370,height=70,width=400)

def but1(): ## 이미지 좌우반전 
    global bt1 
    bt1 = bt1*(-1)

btn1 = Button(win, text=' Flip ! ',command=but1,bg="#00FFFF",borderwidth=0)
btn1.place(x=0, y=375,width=75,height=60)


def save_window():       ## 그래프 저장버튼 
    global px
    global gc
    global bt1
    global graph1

    def save():
        name = "save_file/"+input_text.get()+".png"
        cv2.imwrite(name, graph1)

    window2 = Toplevel(win)
    window2.title("Image Save")
    window2.geometry("420x350")


    graph2 = Image.fromarray(graph1)
    img=ImageTk.PhotoImage(image = graph2)
    
    graph = Label(window2, width=400,height=300, image=img)
    graph.place(x=10, y=10)
    graph.imgtk = img
    graph.configure(image=img)

    input_text = StringVar()
    input_text_enterd = Entry(window2, width=30, textvariable=input_text)
    input_text_enterd.place(x=20, y= 323)
    action = Button(window2,height=1,text= "Enter", command = save)
    action.place(x= 240, y= 320)

btnw = Button(win, text=' Save ! ',command=save_window,bg="#B5FFFF",borderwidth=0)
btnw.place(x=75, y=375,width=75,height=60)

def but2(): ## 이미지 y축 위치 선 표시 
    global bt2 
    bt2 = bt2*(-1)
    if bt2 == -1:
        btn2 = Button(win, text=' Show Y ',command=but2,bg="#00FFFF",borderwidth=0)
        btn2.place(x=150, y=375,width=75,height=60)
    else:
        btn2 = Button(win, text=' Hide Y ',command=but2,bg="#00FFFF",borderwidth=0)
        btn2.place(x=150, y=375,width=75,height=60)

btn2 = Button(win, text=' Show Y',command=but2,bg="#00FFFF",borderwidth=0)
btn2.place(x=150, y=375,width=75,height=60)

def but3(): ## 이미지 x축 위치 선 표시 
    global bt3 
    bt3 = bt3*(-1)
    if bt3 == -1:
        btn2 = Button(win, text=' Show X ',command=but3,bg="#B5FFFF",borderwidth=0)
        btn2.place(x=225, y=375,width=75,height=60)
    else:
        btn2 = Button(win, text=' Hide X ',command=but3,bg="#B5FFFF",borderwidth=0)
        btn2.place(x=225, y=375,width=75,height=60)

btn2 = Button(win, text=' Show X ',command=but3,bg="#B5FFFF",borderwidth=0)
btn2.place(x=225, y=375,width=75,height=60)

def but44(): ## 선 색 변경 
    global linec
    linec = linec*(-1)
    if linec ==-1:
        btn44 = Button(win, text=' Change Color ',command=but44,bg="#00FFFF",borderwidth=0,fg="WHITE")
        btn44.place(x=300, y=375,width=100,height=60)
    else:
        btn44 = Button(win, text=' Change Color ',command=but44,bg="#00FFFF",borderwidth=0,fg="BLACK")
        btn44.place(x=300, y=375,width=100,height=60)

btn44 = Button(win, text=' Change Color ',command=but44,bg="#00FFFF",borderwidth=0,fg="BLACK")
btn44.place(x=300, y=375,width=101,height=60)

def but5(): ## 피크점 구하기 자동,수동 설정 
    global bt5 
    bt5 = bt5*(-1)
    if bt5 == -1:
        switch_peak1()
    else:
        switch_peak2()


btn5 = Button(win, text=' Change ',command=but5,bg="#00FFFF",borderwidth=0)
btn5.place(x=675, y=302,height=29,width=50)

def but4(): ## 파장 설정(구현 예정)
    global setnm,x1,x2,nm1,nm2,iht
    if x1 != x2 and nm1 != nm2:
        setnm = [x1,x2,nm1,nm2]
        if setnm[0]>setnm[1]:
            mx1 = setnm[1]
            mx2 = setnm[0]
        else:
            mx2 = setnm[1]
            mx1 = setnm[0]
        if setnm[2]>setnm[3]:
            mnm2 = setnm[2]
            mnm1 = setnm[3]
        else:
            mnm2 = setnm[3]
            mnm1 = setnm[2]

        setnm=[mx1,mx2,mnm1,mnm2]
    # print(setnm)
    # print(iht)
    # print("please")

btn4 = Button(win, text=' Set Nm ',command=but4,bg="#50E0F0",borderwidth=0)
btn4.place(x=570, y=585,height=29,width=50)

global cap_image

def cap_open():
    global cap_image # 함수에서 이미지를 기억하도록 전역변수 선언 (안하면 사진이 안보임)
    win.filename = filedialog.askopenfilename(initialdir='', title='select_file', filetypes=(
    ('png files', '*.png'), ('jpg files', '*.jpg'), ('all files', '*.*')))
 
    # numpy_image=np.array(pil_image) 
    my_image = np.array(Image.open(win.filename))
    cap_image = my_image



def but6(): ## 카메라 / 이미지 선택 
    global select_img
    select_img = select_img*(-1)
    if select_img ==-1:
        btn66 = Button(win, text=' Img ',command=but6,bg="#50E0F0",borderwidth=0)
        btn66.place(x=170, y=585,height=29,width=50)
        btn666 = Button(win, text='Open Img', command=cap_open,bg="#50E0F0",borderwidth=0)
        btn666.place(x=80, y=585,height=29,width=70)
    else:
        qqw = Label(win, text='',bg='#ADFAFA')
        qqw.place(x=0, y=585,height=35,width=400)
        btn66 = Button(win, text=' Camera ',command=but6,bg="#50E0F0",borderwidth=0)
        btn66.place(x=170, y=585,height=29,width=50)


 
 



but6()

## 카메라 프레임 

cap = cv2.VideoCapture(0) ## for desktop
# cap = cv2.VideoCapture(0,cv2.CAP_V4L2) ## for raspberry
cap1 = cv2.imread("many.png")
cap_image = cv2.cvtColor(cap1,cv2.COLOR_BGR2RGB)

win.configure(bg='#ADFAFA')

qqw = Label(win, text='',bg='WHITE') ## 중앙선
qqw.place(x=402, y=301,height=325,width=2)



def show_frames():

    global loc,gc,bt1,bt2,bt3,bt5,cap1
    global px,graph1,pn
    global linec,select_img,cap_image


    if select_img == 1:

        cap1 = cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB) ## 카메라로 실시간 분석

    else:
        cap1 = cap_image                           ## 이미지로 분석
        # cap1 = cv2.cvtColor(cap1,cv2.COLOR_BGR2RGB)

    cap1 = cv2.resize(cap1,(400,300),interpolation=cv2.INTER_AREA)
    if bt1 == 1:
        cap1= cv2.flip(cap1,1)

    ## 이미지 밝기 조절 

    if gc>=0:
        array = np.full(cap1.shape,(gc,gc,gc),dtype=np.uint8)
        cap1= cv2.add(cap1,array)
        
    else:
        array = np.full(cap1.shape,(-gc,-gc,-gc),dtype=np.uint8)
        cap1 = cv2.subtract(cap1,array)


    cam = np.zeros((300,400,3),dtype=np.uint8)
    

    cam[0:300,0:400] = cap1[0:300,0:400]

    if linec == 1:
        lcl = (0,0,0)
    else:
        lcl = (255,255,255)

    if bt2 ==1:
        cv2.line(cam,(0,loc),(400,loc),lcl,1,cv2.LINE_4)

    if bt3 ==1:
        cv2.line(cam,(x1,300),(x1,0),lcl,1,cv2.LINE_4)
        cv2.line(cam,(x2,300),(x2,0),lcl,1,cv2.LINE_4)


    
    img = Image.fromarray(cam)

    imgtk = ImageTk.PhotoImage(image = img)
    label1.imgtk = imgtk
    label1.configure(image=imgtk)


    ## 그래프 프레임 
    cap2 = waca()
    a= mdim(cap2,loc)
    b = []



    for i in range(400):
        b.append(0)


    if bt5 == -1:

        cv2image= cvgra(a,b)

        pe(cv2image,px)
        graph1 = cv2image

    else:


        aa = block(a,pn)
        cc = yblock(aa,pn)
        bb = peak(cc,pn)


        cv2image = cvgraphp(aa,bb,1,pn)
        # cv2image = waca()

        graph1 = cv2image


    cv2image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = cv2image)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    label1.after(50, show_frames)


show_frames()


win.mainloop()