from tkinter import font
from tkinter import * 
from tkinter import ttk,messagebox
from tkinter.simpledialog import askinteger
import mysql.connector as mysql
from PIL import Image,ImageTk #imagetk help to deal with jpg
import math,random
import os
import hashlib
import cv2
import time
import datetime
import sys
import requests

def back():
    window.destroy()
    os.system("user_welcom.py")

###################### FUNCTION TO ADD PATIENT INFORMATION INTO DATABASE ######################

def add():
    if p_id.get()=="" or p_name.get()=="" or p_cno.get()=="" or p_weight.get()=="" or p_age.get()=="" or p_blood_group.get()=="" or p_add.get()=="" or p_gender.get()=="":
        messagebox.showerror("ERROR","ALL FIELDS ARE REQUIRED",parent=window)
    elif len(p_cno.get())>10 or len(p_cno.get())<10:
        messagebox.showerror("ERROR","INVALID CONTACT NO",parent=window)
    else:
        try:

            #dealing with the database table for entering the information of the patient
                db=mysql.connect(host="127.0.0.1",user='manish',password='manish',database='med')
                mycursor=db.cursor()
                mycursor.execute("insert into p_info (p_id,p_name,contact,age,weight,bg,address,gender) values (%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (
                                    #tuple had been created for multiple value inseration 
                                    p_id.get(),
                                    p_name.get(),
                                    p_cno.get(),
                                    p_age.get(),
                                    p_weight.get(),
                                    p_blood_group.get(),
                                    p_add.get(),
                                    p_gender.get()
                                    )
                                    )
                db.commit()
                db.close()
                messagebox.showinfo("SUCCESS","Pid:- {} \nPATIENT REGISTERED SUCCESSFULLY".format(p_id.get()),parent=window)
     
        except Exception:
                messagebox.showwarning("WARNING","PATIENT ID ALREADY EXISTS\nPLEASE ENTER ANOTHER ID",parent=window)
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    querystring = {"authorization":"NqXnDSpJdFfbBozOjMGx45PQTv89lVCW23rUt0Lek16EAHcYyiQoPgVAIyrpwbvTOX1scC7dNqiWuYBa","sender_id":"TXTIND","message":"Your Patient Id Is {} Note It For Future Usage.".format(p_id.get()),"route":"v3","numbers":p_cno.get()}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    reset() 

def exit():
        op=messagebox.askyesno("Log out","Are You Sure,You Want To EXIT?",parent=window)
        if op==True:
            window.destroy()
            


def reload_id():
        no = datetime.datetime.now()
        print(no.strftime("%y%m%d%H%M"))
        p_id_var.set(no.strftime("%y%m%d%H%M"))

def capture():
    os.system("cam.py {}".format(p_id.get()))
    
    
    photo = 'patient_photo/{}.jpg'.format(p_id.get())
    window.photo = ImageTk.PhotoImage(Image.open(photo))
   
    capture.vlabel=Label(window,image=window.photo)
    capture.vlabel.place(
        x=913,y=169,
        width=250,
        height=250
    )

def reset():
        p_id.delete(0,END)
        p_name.delete(0,END)
        p_gender.delete(0,END)
        p_age.delete(0,END)

        p_weight.delete(0,END)
        p_blood_group.delete(0,END)
        p_cno.delete(0,END)
        p_add.delete(0,END)
        capture.vlabel.destroy()
  

window = Tk()
#code for tkinter window in centre in screen
window_width,window_height = 1300,690

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2.2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

window.configure(bg = "#aed1e7")
canvas = Canvas(
    window,
    bg = "#aed1e7",
    height = 690,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"patient_images/rsz_background.png")
background = canvas.create_image(
    466.5, 356.0,
    image=background_img)

p_id_img = PhotoImage(file = f"patient_images/img_textBox0.png")
p_id_bg = canvas.create_image(
    277.0, 224.0,
    image = p_id_img)

p_id_var=StringVar()
p_id = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15),
    textvariable=p_id_var)

p_id.place(
    x = 177.0, y = 199,
    width = 200.0,
    height = 48)


p_name_img = PhotoImage(file = f"patient_images/img_textBox1.png")
p_name_bg = canvas.create_image(
    657.0, 224.0,
    image = p_name_img)

p_name = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
   font=('ARIAL',15))

p_name.place(
    x = 557.0, y = 199,
    width = 200.0,
    height = 48)


p_gender_img = PhotoImage(file = f"patient_images/img_textBox2.png")
p_gender_bg = canvas.create_image(
    277.0, 348.0,
    image = p_gender_img)

p_gender = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15))

p_gender.place(
    x = 177.0, y = 323,
    width = 200.0,
    height = 48)


p_age_img = PhotoImage(file = f"patient_images/img_textBox3.png")
p_age_bg = canvas.create_image(
    657.0, 348.0,
    image = p_age_img)

p_age = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15))

p_age.place(
    x = 557.0, y = 323,
    width = 200.0,
    height = 48)


p_weight_img = PhotoImage(file = f"patient_images/img_textBox4.png")
p_weight_bg = canvas.create_image(
    277.0, 473.0,
    image = p_weight_img)

p_weight = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15))

p_weight.place(
    x = 177.0, y = 448,
    width = 200.0,
    height = 48)


p_blood_group_img = PhotoImage(file = f"patient_images/img_textBox5.png")
p_blood_group_bg = canvas.create_image(
    657.0, 473.0,
    image = p_blood_group_img)

p_blood_group = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15))

p_blood_group.place(
    x = 557.0, y = 448,
    width = 200.0,
    height = 48)


p_cno_img = PhotoImage(file = f"patient_images/img_textBox6.png")
p_cno_bg = canvas.create_image(
    277.0, 596.0,
    image = p_cno_img)

p_cno = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15))

p_cno.place(
    x = 177.0, y = 571,
    width = 200.0,
    height = 48)

p_add_img = PhotoImage(file = f"patient_images/img_textBox7.png")
p_add_bg = canvas.create_image(
    657.0, 596.0,
    image = p_add_img)

p_add = Entry(
    bd = 0,
    bg = "#7199c5",
    highlightthickness = 0,
    font=('ARIAL',15))

p_add.place(
    x = 557.0, y = 571,
    width = 200.0,
    height = 48)

capture_btn_img = PhotoImage(file = f"patient_images/img0.png")
capture_btn = Button(
    image = capture_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = capture,
    relief = "flat")

capture_btn.place(
    x = 943, y = 478,
    width = 190,
    height = 70)

add_patient_btn_img = PhotoImage(file = f"patient_images/img1.png")
add_patient_btn = Button(
    image = add_patient_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = add,
    relief = "flat")

add_patient_btn.place(
    x = 903, y = 581,
    width = 270,
    height = 80)

back_btn_img = PhotoImage(file = f"patient_images/img2.png")
back_btn = Button(
    image = back_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = back,
    relief = "flat")

back_btn.place(
    x = 24, y = 22,
    width = 88,
    height = 45)

p_id_reload_img = PhotoImage(file = f"patient_images/img3.png")
p_id_reload_btn = Button(
    image = p_id_reload_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = reload_id,
    relief = "flat")

p_id_reload_btn.place(
    x = 411, y = 199,
    width = 50,
    height = 50)


photoFrame=Frame(
        window, borderwidth=1,
        relief="solid",
        bg="#aed1e7",
        bd=2)

photoFrame.place(
    x=913,y=169,
    width=250,
    height=250)

window.protocol("WM_DELETE_WINDOW", exit)
window.resizable(False, False)
window.mainloop()
