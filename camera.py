from tkinter import *
from tkinter.font import BOLD
from PIL import ImageTk, Image
import cv2
import ini

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

    ini.making()
    gray=ImageTk.PhotoImage(file='graph.png')
    graph.imgtk = gray
    graph.configure(image=gray)

    lmain.after(1, video_stream)


video_stream()
   
window.mainloop()