from tkinter import *
from tkinter import ttk,messagebox
import os

def bill_page():
    window.destroy()
    os.system("billing_window.py")

def add_patient():
    window.destroy()
    os.system("patient_window.py")

def logout():
    op=messagebox.askyesno("Log out","Are You Sure, You Want To Log Out?",parent=window)
    if op==True:
        window.destroy()
        os.system("login_window.py")


def exit():
        op=messagebox.askyesno("Log out","Are You Sure,You Want To EXIT?",parent=window)
        if op==True:
            window.destroy()


window = Tk()

#code for tkinter window in centre in screen
window_width,window_height = 1300,690

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2.2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

window.configure(bg = "#103c4a")
canvas = Canvas(
    window,
    bg = "#103c4a",
    height = 690,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"user_images/rsz_background.png")
background = canvas.create_image(
    650.0, 345.0,
    image=background_img)

logout_btn_img = PhotoImage(file = f"user_images/img0.png")
logout_btn = Button(
    image = logout_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = logout,
    relief = "flat")

logout_btn.place(
    x = 1130, y = 29,
    width = 95,
    height = 45)

billing_btn_img = PhotoImage(file = f"user_images/img1.png")
billing_btn = Button(
    image = billing_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = bill_page,
    relief = "flat")

billing_btn.place(
    x = 145, y = 479,
    width = 155,
    height = 160)

add_patient_btn_img = PhotoImage(file = f"user_images/img2.png")
add_patient_btn = Button(
    image = add_patient_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = add_patient,
    relief = "flat")

add_patient_btn.place(
    x = 145, y = 229,
    width = 155,
    height = 160)

window.protocol("WM_DELETE_WINDOW", exit)
window.resizable(False, False)
window.mainloop()
