from tkinter import*
from PIL import Image,ImageTk
import cv2
from tkinter import ttk,messagebox
import os
import sys

win = Tk()
#code for tkinter window in centre in screen
window_width,window_height = 600,310

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

position_top = int(screen_height / 2.2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

win.configure(bg ='#1b407a')


canvas = Canvas(
    win,
    bg = "#0074bd",
    height = 310,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"patient_images/backgroundcam.png")
background = canvas.create_image(
    300.5, 122.0,
    image=background_img)
    
img0 = PhotoImage(file = f"patient_images/imgcap.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: take_copy(rgb),
    relief = "flat")

b0.place(
    x = 108, y = 252,
    width = 105,
    height = 45)

img1 = PhotoImage(file = f"patient_images/imgsave.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda : Save(),
    relief = "flat")

b1.place(
    x = 403, y = 252,
    width = 105,
    height = 45)

color = "red"
color1 = "black"
frame_1 = Frame(win,width = 240,height =190,bg = color).place(x=41,y=54)
frame_2 = Frame(win,width = 240,height =190,bg = color1).place(x=320,y=54)

v = Label(frame_1, width=240, height=190)
v.place(x=41, y=54)

print (sys.argv[1])
def take_copy(im):
    la = Label(frame_2, width=240, height=190)
    la.place(x=320, y=54)
    copy = im.copy()
    copy = cv2.resize(copy, (250, 250))
    rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(copy)
    imgtk = ImageTk.PhotoImage(image)
    image.save('patient_photo/{}.jpg'.format(sys.argv[1]))
    la.configure(image=imgtk)
    la.image = imgtk



def select_img():
    global rgb
    _, img = cap.read()
    img = cv2.resize(img, (250, 250))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image)
    v.configure(image=imgtk)
    v.image = imgtk
    v.after(10, select_img)
  

def Save():
        image = Image.fromarray(rgb)
        messagebox.showinfo("SUCCESS","Image Saved Successfully...!",parent=win)

cap = cv2.VideoCapture(0)
select_img()
win.mainloop()