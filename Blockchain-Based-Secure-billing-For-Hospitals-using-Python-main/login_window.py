from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk #imagetk help to deal with jpg
import mysql.connector as mysql
import random
import requests
import time
import os

def back_btn():
    window.destroy()
    os.system("welcome_window.py")



k=0
def login():
    
    if username.get()=="" or password.get()=="":
            messagebox.showerror("field error","ALL FIELDS ARE REQUIRED",parent=window)

        #checking devloper login for redirecting to devloper window 
        
    elif k==0: # checking for user click login without clicking otp
        messagebox.showerror("ERROR","Get OTP First",parent=window)
    
    elif otp_entry.get()=="": #if otp field is empty
        messagebox.showerror("ERROR","Enter OTP",parent=window)
    
    elif otp1==0:
        messagebox.showerror("ERROR","This OTP is Expired...!\n     Get New OTP",parent=window)
        
    elif otp_entry.get()!=str(otp1):
        messagebox.showerror("ERROR","OTP Is Wrong...!",parent=window)
        otp_entry.delete(0,END)   
    else:   

        if username_var.get()=="Devloper@12345" and password_var.get()=="Devloper@12345":
            db5=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=db5.cursor()
            mycursor.execute("select user_id,password from user_info where BINARY user_id=%s and BINARY password=%s",
                        (
                        username_var.get(),
                        password_var.get()
                        )
                        )
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror("credential error","invalid Credentials for DEVELOPER LOGIN",parent=window)
                db5.close()
                login()
            else:
                window.destroy()
                os.system("developer_window.py")
        else:

            #dealing with the user_info table for checking credentials
            db=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=db.cursor()
            mycursor.execute("select user_id,password from user_info where BINARY user_id=%s and BINARY password=%s",
                            (
                            username.get(),
                            password.get()
                            )
                            )
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror("credential error","invalid USERNAME and PASSWORD",parent=window)
                db.close()
                login()
            else:
                window.destroy()
                os.system("user_welcom.py")
            
def send_sms():
    global k
    k=1
    if username.get()=="" or password.get()=="":
        messagebox.showwarning("WARNING","Enter Usename & Password...!",parent=window)
    else:
        try:

            mydb=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb.cursor()
            mycursor.execute("SELECT tel_no FROM user_info where BINARY user_id = %s and BINARY password = %s",
                            (
                                username.get(),
                                password.get()
                            )
                            )
            result=mycursor.fetchone()
            if result==None:
                messagebox.showerror("credential error","invalid USERNAME and PASSWORD",parent=window)
                mydb.commit()
                mydb.close()
            else:
                print(result)
                mydb.commit()
                mydb.close()
         
         
                global otp1
        
                otp1=random.randint(1000,9999)
                print(otp1)
                messagebox.showinfo("SUCCESS","OTP Sended to Registered Number..!",parent=window)
                url = "https://www.fast2sms.com/dev/bulkV2"
                querystring = {"authorization":"add your authentication key here","sender_id":"TXTIND","message":"Your Account Login OTP Is {}".format(otp1),"route":"v3","numbers":result}
                headers = {'cache-control': "no-cache"}
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)
                    
                global t 
                t=59
                while t>=0:
                    timer = ("{}".format(t))
                    v.set(timer)
                    time.sleep(1)
                    t = t - 1
                    window.update()
            
                print("After 60 sec")
                print(otp1)
                result=messagebox.askyesno("Send OTP","Current OTP is expired...!\n\n     Send New OTP ?")
                if result>0:
                    send_sms()
                else:
                    otp1=0
        except Exception as e:
            messagebox.showerror("Network","No Internet/Databse Connection...!",parent=window)
            
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

background_img = PhotoImage(file = f"login_images/rsz_background.png")
background = canvas.create_image(
    646.5, 346.0,
    image=background_img)

username_img = PhotoImage(file = f"login_images/img_textBox0.png")
username_bg = canvas.create_image(
    866.0, 218.0,
    image = username_img)

username_var=StringVar()
username = Entry(
    bd = 0,
    bg = "#67c1f3",
    highlightthickness = 0,
    font=('ARIAL',15),
    textvariable=username_var)

username.place(
    x = 721.0, y = 188,
    width = 290.0,
    height = 58)

password_img = PhotoImage(file = f"login_images/img_textBox1.png")
password_bg = canvas.create_image(
    866.0, 342.0,
    image = password_img)

password_var=StringVar()
password = Entry(
    bd = 0,
    bg = "#67c1f3",
    highlightthickness = 0,
    font=('ARIAL',15),
    show='*',
    textvariable=password_var)

password.place(
    x = 721.0, y = 312,
    width = 290.0,
    height = 58)

otp_entry_img = PhotoImage(file = f"login_images/img_textBox2.png")
otp_entry_bg = canvas.create_image(
    869.0, 465.0,
    image = otp_entry_img)

otp_entry = Entry(
    bd = 0,
    bg = "#67c1f3",
    highlightthickness = 0,
    font=('ARIAL',15))

otp_entry.place(
    x = 724.0, y = 435,
    width = 290.0,
    height = 58)

img0 = PhotoImage(file = f"login_images/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = login,
    relief = "flat")

b0.place(
    x = 724, y = 577,
    width = 290,
    height = 96)

entry3_img = PhotoImage(file = f"login_images/img_textBox3.png")
entry3_bg = canvas.create_image(
    866.0, 546.5,
    image = entry3_img)
    
v = StringVar(window, value='60')
entry3 = Entry(
    bd = 0,
    bg = "#d7eeea",
    highlightthickness = 0,textvariable=v,
    font=('ARIAL',15))

entry3.place(
    x = 853.5, y = 529,
    width = 25.0,
    height = 33)

img1 = PhotoImage(file = f"login_images/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = send_sms,
    relief = "flat")

b1.place(
    x = 1072, y = 435,
    width = 92,
    height = 60)

img2 = PhotoImage(file = f"login_images/img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = back_btn,
    relief = "flat")

b2.place(
    x = 10, y = 20,
    width = 88,
    height = 45)

window.resizable(False, False)
window.mainloop()
