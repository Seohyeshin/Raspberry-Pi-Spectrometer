from tkinter import *
from tkinter.font import BOLD
from PIL import ImageTk, Image
import cv2
import ini

def save_window():
    global png
    Save_file = cv2.imread("graph.png")
    cv2.imwrite("save.png", Save_file)
    window2 = Toplevel(window)
    window2.title("Image Save")
    window2.geometry("600x400")
    saveFrame = Frame(window2, width= 600, height=400)
    saveFrame.grid(row=0, column=0)
    Sfile = Label(saveFrame, width=300,height=300)
    png=ImageTk.PhotoImage(file='save.png')  
    Sfile.imgtk = png
    Sfile.configure(image=png)
    Sfile.place(x=0, y=0)

    # 창 만들기
    # 이름 적기
    # 이미지 보여주기
    # name = "save.png"
    # cv2.imwrite(name, Save_file)

window=Tk()
window.title('Video preview')
window.geometry("600x700")

#Layout of display
topFrame =Frame(window,width= 600, height=800)
topFrame.grid(row=0, column=0)

graph = Label(topFrame,width=600,height=500)
graph.place(x=0, y=200)

# 꾸미기
canvas = Canvas(topFrame, width=350, height=252)
canvas.place(x=0, y=0)

img = ImageTk.PhotoImage(file = "img.png")
canvas.create_image(-50, -100, anchor=NW, image=img)
canvas.create_text(180, 100, text = "Raspberry-Pi", font = ('Archivo', 20, BOLD), fill = "white")
canvas.create_text(180, 130, text = "Spectrometer", font = ('Archivo', 20, BOLD), fill = "white")

#저장 버튼
save_file=Button(topFrame, command=save_window,  padx=5, pady=3, width=12, text="저장")
save_file.place(x=220, y=200)



#topFrame
lmain = Label(topFrame,width=250,height=250)
lmain.place(x=350, y=0)


cap=cv2.VideoCapture(0)

def video_stream():

    ret, frame = cap.read()

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, video_stream)

def make_graph():

    ini.making()
    gray=ImageTk.PhotoImage(file='graph.png')
    graph.imgtk = gray
    graph.configure(image=gray)

    graph.after(10, make_graph)


video_stream()
make_graph()
   
window.mainloop()