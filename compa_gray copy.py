import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk



ygra = 300 ## y그래프 높이
gx = 0 ## x그래프 여백
gy = 60 ## y그래프 여백

mul = 3

def cvgra(clist,blist): ## 그래프 그리는 함수  

    lt = len(clist)
    sketch = wave(lt)
    draw(sketch,clist)
    draw(sketch,blist)

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
        if (i)%(50*mul) == 0:
            text = str(int(i/mul))
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
        color = (0,0,0)
        y = int(clist[i])

        cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i+int(gx/mul),ygra-y-int(gy/mul)),color,1,cv2.LINE_4)
        if i>0:
            cv2.line(sketch,(i+int(gx/mul),ygra-y-int(gy/mul)),(i-1+int(gx/mul),ygra-x-int(gy/mul)),color,1,cv2.LINE_4)
        x = y
    return sketch

def mdim(img,loc): ## y(loc)위치에 있는 grayscale값 얻어서 리스트로 반환 
    h,w,C = img.shape
    a = []
    imgg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    for i in range(w):
        a.append(imgg[loc,i])

    return a

def pe(img,list,x): ## x위치에 있는 값을 반환 

    text = str(list[x])
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.line(img,(x,0),(x,300),(0,0,0),1,cv2.LINE_4)
    cv2.putText(img,text,(175,125),font,1,(0,0,0),2)


win = Tk()

win.geometry("800x400")

label1 =Label(win) 
label1.grid(row=0, column=0)
# cap= cv2.imread('example.jpg')
# cap2= cv2.imread('image.png') ## 변화시킬 그래프 

cap= cv2.VideoCapture(0)

# cap1= cv2.imread('plzz.png')## 기준점 그래프 
# cap1= cv2.resize(cap1,(400,300))


label =Label(win)
label.grid(row=0, column=1)


global loc
global pn
global px
global gc
global bt1

loc = 150
pn = 5
px = 1
gc = 0
bt1 = -1

# cap += gc


## 스케일 조절

def yloc(self): ## 이미지에서 y 위치 조정
    global loc
    loc = int(scale1.get())

scale1 = Scale(win,orient='horizontal',resolution=1,from_=1, to=299,command=yloc, length=300)
scale1.grid(row=1,column=0)

def grpn1(self): ## 그래프에서 찾을 x값 위치 조정 
    global px
    px = int(scale3.get())

scale3 = Scale(win,orient='horizontal',resolution=1,from_=0, to=399,command=grpn1, length=300)
scale3.grid(row=1,column=1)

def grpn2(self): ## 밝기 조절????
    global gc
    gc = int(scale2.get())

scale2 = Scale(win,orient='horizontal',resolution=1,from_=0, to=255,command=grpn2, length=300)
scale2.grid(row=2,column=1)

## 버튼 

def but1(): ## 이미지 좌우반전 
    global bt1 
    bt1 = bt1*(-1)

btn1 = Button(win, text=' Flip ! ',command=but1)
btn1.place(x=150, y=350)


def save_window():
    global px
    global gc
    global bt1

    def save():
        name = "save_file/"+input_text.get()+".png"
        cv2.imwrite(name, cv2image)

    window2 = Toplevel(win)
    window2.title("Image Save")
    window2.geometry("420x350")


    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    cv2image= cv2.resize(cv2image,(400,300),interpolation=cv2.INTER_AREA)

    if bt1 == 1:
        cv2image= cv2.flip(cv2image,1)

        
    cv2image+= gc
    a = mdim(cv2image,loc)
    b = []
    for i in range(400):
        b.append(0)
    
    cv2image= cvgra(a,b)
    pe(cv2image,a,px)
    img = Image.fromarray(cv2image)
    img=ImageTk.PhotoImage(image = img)
    
    graph = Label(window2, width=400,height=300, image=img)
    graph.place(x=10, y=10)
    graph.imgtk = img
    graph.configure(image=img)

    input_text = StringVar()
    input_text_enterd = Entry(window2, width=30, textvariable=input_text)
    input_text_enterd.place(x=20, y= 323)
    action = Button(window2,height=1,text= "Enter", command = save)
    action.place(x= 240, y= 320)

btn2 = Button(win, text=' save ! ',command=save_window)
btn2.place(x=200, y=350)


## 카메라 프레임 
def show_frames():

    global loc
    global gc
    global bt1

    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB) 
    # cv2image= cv2.cvtColor(cap2,cv2.COLOR_BGR2RGB)  
    cv2image= cv2.resize(cv2image,(400,300),interpolation=cv2.INTER_AREA)
    if bt1 == 1:
        cv2image= cv2.flip(cv2image,1)

    cv2image += gc
    cv2.line(cv2image,(0,300-loc),(400,300-loc),(0,0,0),1,cv2.LINE_4)

    img = Image.fromarray(cv2image)

    imgtk = ImageTk.PhotoImage(image = img)
    label1.imgtk = imgtk
    label1.configure(image=imgtk)

    label1.after(50, show_frames)


## 그래프 프레임 

def show_graph():

    global px
    global gc
    global bt1

    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    # cv2image= cv2.cvtColor(cap2,cv2.COLOR_BGR2RGB)
    cv2image= cv2.resize(cv2image,(400,300),interpolation=cv2.INTER_AREA)

    if bt1 == 1:
        cv2image= cv2.flip(cv2image,1)

    
    cv2image+= gc
    a = mdim(cv2image,loc)
    b = []
    for i in range(400):
        b.append(0)
    # b = mdim(cap1,3)
    cv2image= cvgra(a,b)

    pe(cv2image,a,px)
    img = Image.fromarray(cv2image)

    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    label.after(50, show_graph)


show_frames()
show_graph()

win.mainloop()
