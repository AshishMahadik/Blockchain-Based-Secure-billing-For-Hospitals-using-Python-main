from tkinter import *
import os

def logRe():
    window.destroy()
    os.system ("login_window.py")
    


def regRe():
    window.destroy()
    os.system("register_window.py")
    
window = Tk()

#code for tkinter window in centre in screen
window_width,window_height = 1300,690

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2.2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

window.title("BLOCKCHAIN BASED SECURE BILLING FOR HOSPITALS")
window.configure(bg = "#a66565")
canvas = Canvas(
    window,
    bg = "#a66565",
    height = 690,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"welcome_images/rsz_background.png")
background = canvas.create_image(
    650.0, 345.0,
    image=background_img)

login_btn_img = PhotoImage(file = f"welcome_images/img0.png")
login_btn = Button(
    image = login_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = logRe,
    relief = "flat")

login_btn.place(
    x = 736, y = 359,
    width = 200,
    height = 200)

reg_btn_img = PhotoImage(file = f"welcome_images/img1.png")
reg_btn = Button(
    image = reg_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = regRe,
    relief = "flat")

reg_btn.place(
    x = 1037, y = 359,
    width = 200,
    height = 200)

window.resizable(False, False)
window.mainloop()
