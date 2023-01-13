import cv2
import numpy as np
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
from tkinter import filedialog
import intensity
import graph_making
import wavelength_calculate


## UI부분 
## 라즈베리파이에 실행시엔 반드시 for desktop부분을 삭제 또는 주석처리 한 뒤 아래 for raspberry을 주석 해제하여 실행할 것

win = Tk()

win.geometry("800x625") 

label =Label(win)
label.grid(row=0, column=1)

label1 =Label(win) 
label1.grid(row=0, column=0)

global cap1   ##카메라 이미지
global graph1 ##그래프 이미지 
global loc ## 카메라 y축 위치
global pn  ## 이미지 피크점 조절
global px  ## 뭐엿더라
global gc  ## 이미지 밝기
global bt1,bt2,bt3,bt4,bt5 ## 버튼1,2,3,4,5
global x1,x2 ## 그래프 x1 x2 위치 
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
linec = 1
select_img = 1


i = np.zeros((0,400,1),dtype=np.uint8) # for i in range(400): nmnm.append(i)


LAY = Label(win, text='  ',bg='#50E0F0') ## X1 위치조절 추가박스
LAY.place(x=1, y=430,height=40,width=400)


qqw = Label(win, text='',bg='#ADFAFA') ## 위치조절박스
qqw.place(x=403, y=395,height=40,width=400)



## UI 스케일 조절(왼쪽 부분)

change_yloc = Label(win, text=' Set Y location ',bg='#50E0F0')  ## 이미지에서 y 위치 조정
change_yloc.place(x=1, y=302,height=28,width=400)


style = ttk.Style()
style.configure("TScale", background="#ADFAFA") ## UI 조절바 뒷배경 색 조정


def yloc(self): ## 관찰한 스펙트럼(카메라)의 y축 높이 조절
    global loc
    loc = int(scale.get())

scale = ttk.Scale(win,command= yloc, from_=1, to=299, value=0, length=300, orient="horizontal", style="TScale")
scale.place(x=50, y=330,height=42,width=300)


def change_X1(self):  ## 관찰한 스펙트럼(카메라)의 X1 위치 조절
    global x1
    x1 = int(scale_X1.get())

scale_X1 = ttk.Scale(win,orient='horizontal',from_=1, to=400,command=change_X1, length=300)
scale_X1.place(x=50, y=470,height=40,width=300)

grpn_X1 = Label(win, text=' Set X1 ',background="#50E0F0")  
grpn_X1.place(x=1, y=440,height=30,width=400)


def change_X2(self):  ## 관찰한 스펙트럼(카메라)의 X2 위치 조절 
    global x2
    x2 = int(scale_X2.get())

scale_X2 = ttk.Scale(win,orient='horizontal',from_=1, to=400,command=change_X2, length=300)
scale_X2.place(x=50, y=540,height=40,width=300)

grpn_X2 = Label(win, text=' Set X2 ',background="#50E0F0")  
grpn_X2.place(x=1, y=510,height=30,width=400)


## UI 스케일 조절(오른쪽 부분)

def Set_I(self):   ## 밝기 조절 
    global gc
    gc = int(scale_I.get())

scale_I = ttk.Scale(win,orient='horizontal',from_=-255, to=255,command=Set_I, length=300)
scale_I.place(x=450, y=395,height=40,width=300)

grpn_I = Label(win, text=' Set brightness ',background="#50E0F0")  
grpn_I.place(x=403, y=375,height=24,width=400)


def change_nm1(self):  ## 스펙트럼 이미지에서 파장값1 조정
    global nm1
    nm1 = int(scale_nm1.get())

scale_nm1 = Scale(win,orient='horizontal',resolution=1,from_=380, to=780,command=change_nm1, length=300,background="#ADFAFA")
scale_nm1.place(x=425, y=470,height=40,width=350)

grpn_nm1 = Label(win, text=' Set Nm1 ',background="#50E0F0")  
grpn_nm1.place(x=401, y=440,height=30,width=400)


def change_nm2(self):  ## 스펙트럼 이미지에서 파장값2 조정 
    global nm2
    nm2 = int(scale_nm2.get())

scale_nm2 = Scale(win,orient='horizontal',resolution=1,from_=380, to=780,command=change_nm2, length=300,background="#ADFAFA")
scale_nm2.place(x=425, y=540,height=40,width=350)

grpn_nm2 = Label(win, text=' Set Nm2 ',background="#50E0F0") 
grpn_nm2.place(x=401, y=510,height=30,width=400)



## UI 內 Button

def but_flip(): ## 이미지 좌우반전 
    global bt1 
    bt1 = bt1*(-1)

btn_flip = Button(win, text=' Flip ! ',command=but_flip,bg="#00FFFF",borderwidth=0)
btn_flip.place(x=0, y=375,width=75,height=60)


def save_window(): ## 그래프 저장버튼 
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

btn_save = Button(win, text=' Save ! ',command=save_window,bg="#B5FFFF",borderwidth=0)
btn_save.place(x=75, y=375,width=75,height=60)

def but_yline(): ## 스펙트럼 이미지 y축 위치 선 표시 (Show Y)
    global bt2 
    bt2 = bt2*(-1)
    if bt2 == -1:
        btn2 = Button(win, text=' Show Y ',command=but_yline,bg="#00FFFF",borderwidth=0)
        btn2.place(x=150, y=375,width=75,height=60)
    else:
        btn2 = Button(win, text=' Hide Y ',command=but_yline,bg="#00FFFF",borderwidth=0)
        btn2.place(x=150, y=375,width=75,height=60)

btn_yline = Button(win, text=' Show Y',command=but_yline,bg="#00FFFF",borderwidth=0)
btn_yline.place(x=150, y=375,width=75,height=60)

def but_xline(): ## 스펙트럼 이미지 x축 위치 선 표시 (Show X)
    global bt3 
    bt3 = bt3*(-1)
    if bt3 == -1:
        btn2 = Button(win, text=' Show X ',command=but_xline,bg="#B5FFFF",borderwidth=0)
        btn2.place(x=225, y=375,width=75,height=60)
    else:
        btn2 = Button(win, text=' Hide X ',command=but_xline,bg="#B5FFFF",borderwidth=0)
        btn2.place(x=225, y=375,width=75,height=60)

btn_xline = Button(win, text=' Show X ',command=but_xline,bg="#B5FFFF",borderwidth=0)
btn_xline.place(x=225, y=375,width=75,height=60)

def but_change_linecolor(): ## X,Y 축 선 색 변경 (Change Color)
    global linec
    linec = linec*(-1)
    if linec ==-1:
        btn44 = Button(win, text=' Change Color ',command=but_change_linecolor,bg="#00FFFF",borderwidth=0,fg="WHITE")
        btn44.place(x=300, y=375,width=100,height=60)
    else:
        btn44 = Button(win, text=' Change Color ',command=but_change_linecolor,bg="#00FFFF",borderwidth=0,fg="BLACK")
        btn44.place(x=300, y=375,width=100,height=60)

btn_change_linecolor = Button(win, text=' Change Color ',command=but_change_linecolor,bg="#00FFFF",borderwidth=0,fg="BLACK")
btn_change_linecolor.place(x=300, y=375,width=101,height=60)

def but_change(): ## 피크점 구하기 자동,수동 설정 (find peak by manual 옆에 change 버튼!)
    global bt5 
    bt5 = bt5*(-1)
    if bt5 == -1:
        switch_peak1()
    else:
        switch_peak2()

btn_change = Button(win, text=' Change ',command=but_change,bg="#00FFFF",borderwidth=0)
btn_change.place(x=675, y=302,height=29,width=50)

def switch_peak1():   ## 그래프에서 찾을 x값 위치 조정

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

def switch_peak2():  ## 자동으로 피크점 구하기 

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


def but_camera_image(): ## 카메라 / 이미지 선택버튼 
    global select_img
    select_img = select_img*(-1)
    if select_img ==-1:
        btn66 = Button(win, text=' Img ',command=but_camera_image,bg="#50E0F0",borderwidth=0)
        btn66.place(x=170, y=585,height=29,width=50)
        btn666 = Button(win, text='Open Img', command=cap_open,bg="#50E0F0",borderwidth=0)
        btn666.place(x=80, y=585,height=29,width=70)
    else:
        qqw = Label(win, text='',bg='#ADFAFA')
        qqw.place(x=0, y=585,height=35,width=400)
        btn66 = Button(win, text=' Camera ',command=but_camera_image,bg="#50E0F0",borderwidth=0)
        btn66.place(x=170, y=585,height=29,width=50)

but_camera_image()

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
        cap1 = cap_image                                     ## 이미지로 분석
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
    cap2 = wavelength_calculate.waca()
    a= intensity.mdim(cap2,loc)
    b = []

    b = np.zeros((0,400,1),dtype=np.uint8)
   

    if bt5 == -1:

        cv2image= graph_making.cvgra(a,b)

        graph_making.pe(cv2image,px)
        graph1 = cv2image

    else:

        aa = graph_making.block(a,pn)
        cc = graph_making.yblock(aa,pn)
        bb = graph_making.peak(cc,pn)

        cv2image = graph_making.cvgraphp(aa,bb,1,pn)
        # cv2image = waca()

        graph1 = cv2image


    cv2image = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = cv2image)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    label1.after(50, show_frames)


show_frames()


win.mainloop()