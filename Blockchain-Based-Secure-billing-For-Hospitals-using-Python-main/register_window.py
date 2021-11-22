from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk #imagetk help to deal with jpg
import mysql.connector as mysql
import random
import requests
import time
import os

def back_to():
    window.destroy()
    os.system("welcome_window.py")

    
def send_otp():
        if len(tel_no.get()) > 10 or len(tel_no.get()) < 9:
            messagebox.showerror("ERROR","Enter Valid Mobile No",parent=window)
    
        elif tel_no.get()=="":
            messagebox.showwarning("WARNING","Enter Mobile No.",parent=window)
        else:
            try:    
                global otp1
                otp1=random.randint(1000,9999)
                print(otp1)
                    
                messagebox.showinfo("SUCCESS","OTP Send Successfully...!",parent=window)
                url = "https://www.fast2sms.com/dev/bulkV2"
                querystring = {"authorization":"add your authentication key here","sender_id":"TXTIND","message":"Your Account Registration OTP Is {}".format(otp1),"route":"v3","numbers":"{}".format(int(tel_no.get()))}
                headers = {'cache-control': "no-cache"}
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(int(tel_no.get()))
                print(response.text)
                global t 
                t=59
                while t>=0:
                    timer = ("{}".format(t))
                    v.set(timer)
                    time.sleep(1)
                    t = t - 1
                    window.update()
                
                print("after 60 sec")
                print(otp1)
                result=messagebox.askyesno("Send OTP","Current OTP is expired...!\n\n     Send New OTP ?")
                if result>0:
                    send_otp()
                else:
                    otp1=0
            
            except Exception as e:
                    messagebox.showerror("Network","No Internet/Databse Connection...!",parent=window)

def register():
    #setting validation for empty fields,
    #checking the values in the entery fields
        
    if h_name.get()=="" or reg_no.get()=="" or addr.get()=="" or tel_no.get()=="" or username.get()=="" or password.get()=="":
        messagebox.showerror("ERROR","ALL FIELDS ARE REQUIRED",parent=window)

    elif otp1==0:
        messagebox.showerror("ERROR","This OTP is Expired...!\n     Get New OTP",parent=window)
            
    elif otp_entry.get()!=str(otp1):
        messagebox.showerror("ERROR","OTP Is Wrong",parent=window)
    else:
            
        try:
            #dealing with the database table for entering the information of the user_hospital
            db=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=db.cursor()
            mycursor.execute("insert into user_info (user_id,password,hospital_name,reg_no,address,tel_no) values (%s,%s,%s,%s,%s,%s)",
                               (
                                #tuple had been created for multiple value inseration 
                                username.get(),
                                password.get(),
                                h_name.get(),
                                reg_no.get(),
                                addr.get(),
                                tel_no.get()
                               )
                            )
            db.commit()
            db.close()
            messagebox.showinfo("SUCCESS","REGISTERED SUCCESSFULLY",parent=window)
            
            #define this
            # destroy current window and redirect to welcome page(window)
            
            clear_data()
            #since the table is created wuth unique key for user_id attribute hence,
            # only if same username is found then only except block will execute.
            window.destroy()
            os.system("welcome_window.py")     
        except Exception:
            messagebox.showwarning("WARNING","USER ALREADY EXISTS",parent=window)

def clear_data():
        h_name.delete(0,END)
        password.delete(0,END)
        username.delete(0,END)
        tel_no.delete(0,END)
        addr.delete(0,END)
        reg_no.delete(0,END)
        otp_entry.delete(0,END)
        entry7.delete(0,END)

window = Tk()

#code for tkinter window in centre in screen
window_width,window_height = 1300,690

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2.2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 690,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"registration_images/rsz_background.png")
background = canvas.create_image(
    650.0, 345.0,
    image=background_img)

h_name_img = PhotoImage(file = f"registration_images/img_textBox0.png")
h_name_bg = canvas.create_image(
    546.0, 229.0,
    image = h_name_img)

h_name = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
   font=('ARIAL',15))

h_name.place(
    x = 446.0, y = 204,
    width = 200.0,
    height = 48)

reg_no_img = PhotoImage(file = f"registration_images/img_textBox1.png")
reg_no_bg = canvas.create_image(
    970.0, 229.0,
    image = reg_no_img)

reg_no = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
    font=('ARIAL',15))

reg_no.place(
    x = 870.0, y = 204,
    width = 200.0,
    height = 48)

addr_img = PhotoImage(file = f"registration_images/img_textBox2.png")
addr_bg = canvas.create_image(
    547.0, 345.0,
    image = addr_img)

addr = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
    font=('ARIAL',15))

addr.place(
    x = 447.0, y = 320,
    width = 200.0,
    height = 48)

tel_no_img = PhotoImage(file = f"registration_images/img_textBox3.png")
tel_no_bg = canvas.create_image(
    969.0, 345.0,
    image = tel_no_img)

tel_no = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
    font=('ARIAL',15))

tel_no.place(
    x = 869.0, y = 320,
    width = 200.0,
    height = 48)

username_img = PhotoImage(file = f"registration_images/img_textBox4.png")
username_bg = canvas.create_image(
    544.0, 461.0,
    image = username_img)

username = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
    font=('ARIAL',15))

username.place(
    x = 444.0, y = 436,
    width = 200.0,
    height = 48)

password_img = PhotoImage(file = f"registration_images/img_textBox5.png")
password_bg = canvas.create_image(
    972.0, 461.0,
    image = password_img)

password = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
    font=('ARIAL',15),
    show='*')

password.place(
    x = 872.0, y = 436,
    width = 200.0,
    height = 48)

otp_entry_img = PhotoImage(file = f"registration_images/img_textBox6.png")
otp_entry_bg = canvas.create_image(
    546.0, 577.0,
    image = otp_entry_img)

otp_entry = Entry(
    bd = 0,
    bg = "#7fc5ca",
    highlightthickness = 0,
    font=('ARIAL',15))

otp_entry.place(
    x = 446.0, y = 552,
    width = 200.0,
    height = 48)

entry7_img = PhotoImage(file = f"registration_images/img_textBox7.png")
entry7_bg = canvas.create_image(
    544.0, 624.0,
    image = entry7_img)
    
v = StringVar(window, value='60')
entry7 = Entry(
    bd = 0,
    bg = "#f9c9d8",
    highlightthickness = 0,textvariable=v,
    font=('ARIAL',15))

entry7.place(
    x = 530.0, y = 612,
    width = 28.0,
    height = 22)

back_btn_img = PhotoImage(file = f"registration_images/img0.png")
back_btn = Button(
    image = back_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = back_to,
    relief = "flat")

back_btn.place(
    x = 8, y = 11,
    width = 88,
    height = 45)

send_btn_img = PhotoImage(file = f"registration_images/img1.png")
send_btn = Button(
    image = send_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = send_otp,
    relief = "flat")

send_btn.place(
    x = 677, y = 547,
    width = 97,
    height = 59)

register_btn_img = PhotoImage(file = f"registration_images/img2.png")
register_btn = Button(
    image = register_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = register,
    relief = "flat")

register_btn.place(
    x = 830, y = 528,
    width = 283,
    height = 84)

window.resizable(False, False)
window.mainloop()
