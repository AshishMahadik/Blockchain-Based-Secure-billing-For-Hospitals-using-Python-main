from logging import exception
from tkinter import *
from tkinter import ttk,messagebox
from tkinter.font import Font
import mysql.connector as mysql
import cv2
from PIL import Image,ImageTk #imagetk help to deal with jpg
import os

def back():
    op=messagebox.askyesno("Log out","Are You Sure, You Want To Log Out?",parent=window)
    if op==True:
        window.destroy()
        os.system("welcome_window.py")


def reset():
        med_id.delete(0,END)
        med_name.delete(0,END)
        med_des.delete(0,END)
        med_price.delete(0,END)
        for record in med_info.get_children():
            med_info.delete(record)

def add():
        if med_id.get()=="" or med_name.get()=="" or med_price.get()=="" or med_des.get()=="":
            messagebox.showerror("ERROR","ALL FIELDS ARE REQUIRED",parent=window)
        else:

            # for memory managment here image compression is done

            img=Image.open("med_photo.jpg")  # -----> opening image using PIL library
            img=img.resize((960,540),Image.ANTIALIAS) # -----> antialising the image (compressing wihtout changing imag resolution)
            img.save("med_photo.jpg") # -------> overwriting  the compressed image into original image
            
            
            # since database can not read image as it is
            # converting the image into binary format

            with open("med_photo.jpg",'rb') as f:
                bi_img = f.read()

            # establishing the database connection
            mydb=mysql.connect(host="127.0.0.1",user='manish',passwd='manish',database='med')
            mycursor=mydb.cursor()
            mycursor.execute("insert into med_info (med_id,med_name,description,med_price,image) values(%s,%s,%s,%s,%s)",
                            (
                                med_id.get(),
                                med_name.get(),
                                med_des.get(),
                                med_price.get(),
                                bi_img  # ----> passing obj of binary image that we have read above
                            )    
                            )
            mydb.commit()
            mydb.close()
            os.remove("med_photo.jpg")
            messagebox.showinfo("","ENTERY ADDED SUCCESSFULLY",parent=window)
            display()

def image():
        try:

            #giving devloper the glance information regarding cv2 window
            messagebox.showinfo("image capture","press ENTER to capture\npress ESC to exit",parent=window)
            
            #importing cv2 methods for capturing images
            cam=cv2.VideoCapture("http://192.168.88.183:8080/video")
            while True:
                ret,frame=cam.read()
                frame=cv2.resize(frame,(0,0),fx=0.40,fy=0.30)
                cv2.imshow('image',frame)
                cv2.setWindowProperty("image",cv2.WND_PROP_TOPMOST,1)
                key=cv2.waitKey(1)
                if key%256==27:
                    break
                elif key%256==13:
                    img_name = "med_photo.jpg" #opencv_frame_
                    cv2.imwrite(img_name,frame)
                    messagebox.showinfo("captured","image captured..!",parent=window)
            cam.release()
            cv2.destroyAllWindows()
        except Exception as e:
            messagebox.showerror("ERROR","IP WEBCAM is not connected...!",parent=window)


def display():
        mydb=mysql.connect(host="127.0.0.1",user='manish',passwd='manish',database='med')
        mycursor=mydb.cursor()
        mycursor.execute(" select * from med_info")
        result=mycursor.fetchall()
        if len(result) != 0:
            med_info.delete(*med_info.get_children())
            for row in result:
                med_info.insert('',END,values =row)
        mydb.commit()
        mydb.close()


def displayvalue(ev):
        view = med_info.focus()
        holdData = med_info.item(view)
        rece_row = holdData['values']
        med_id_var.set(rece_row[0]),
        med_name_var.set(rece_row[1]),
        med_des_var.set(rece_row[2]),
        med_price_var.set(rece_row[3])


def update():

        img=Image.open("med_photo.jpg")  # -----> opening image using PIL library
        img=img.resize((960,540),Image.ANTIALIAS) # -----> antialising the image (compressing wihtout changing imag resolution)
        img.save("medphoto/med_photo.jpg") # -------> overwriting  the compressed image into original image
            
            
        # since database can not read image as it is
        # converting the image into binary format

        with open("med_photo.jpg",'rb') as f:
            bi_img = f.read()

        mydb=mysql.connect(host="127.0.0.1",user='manish',passwd='manish',database='med')
        mycursor=mydb.cursor()
        mycursor.execute(" update med_info set med_id=%s,med_name=%s,description=%s,med_price=%s,image=%s where med_id=%s ",
                            (
                                med_id.get(),
                                med_name.get(),
                                med_des.get(),
                                med_price.get(),
                                bi_img,  # ----> passing obj of binary image that we have read above
                                med_id.get()
                                
                            )    
                            )
        mydb.commit()
        
        mydb.close()
        
        os.remove("medphoto/med_photo.jpg")
        display()
        messagebox.showinfo("","ENTERY UPDATED SUCCESSFULLY",parent=window)
        

def delete():
        if med_id.get()=="" :
           messagebox.showerror("ERROR","Select Medicine ",parent=window) 
        else:
            
            db=mysql.connect(host="127.0.0.1",user='manish',passwd='manish',database='med')
            mycursor=db.cursor()
            mycursor.execute(" delete from med_info WHERE med_id=%s or med_name=%s",
                                    (
                                    med_id.get(),
                                    med_name.get()
                                    )
                            )
            db.commit()
            db.close()
            
            messagebox.showinfo("","ENTERY DELETED SUCCESSFULLY",parent=window)
            x=med_info.selection()[0]
            med_info.delete(x)
        reset()


def search():
        try:

            mydb=mysql.connect(host="127.0.0.1",user='manish',passwd='manish',database='med')
            mycursor=mydb.cursor()
            mycursor.execute("SELECT * FROM med_info where med_name LIKE '%"+med_name.get()+"%'")
            result=mycursor.fetchall()
            print(result)
            if len(result)==0:
                messagebox.showinfo("","Medicine not found",parent=window)
            if len(result) > 0:
                med_info.delete(*med_info.get_children())
                for row in result:
                    med_info.insert('',END,values =row)
            else:
                med_info.delete(*med_info.get_children())
            mydb.commit()
        except Exception as e:
            messagebox.showinfo("","{}".format(e),parent=window)
            reset()
        mydb.close()

def Exit():
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

window.configure(bg = "#314357")
canvas = Canvas(
    window,
    bg = "#314357",
    height = 690,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"developer_images/rsz_background.png")
background = canvas.create_image(
    650.0, 345.0,
    image=background_img)

med_id_img = PhotoImage(file = f"developer_images/img_textBox0.png")
med_id_bg = canvas.create_image(
    332.0, 180.0,
    image = med_id_img)

med_id_var=StringVar()
med_id = Entry(
    bd = 0,
    bg = "#c4c4c4",
    highlightthickness = 0,
    font=('ARIAL',15),
    textvariable=med_id_var)

med_id.place(
    x = 232.0, y = 155,
    width = 200.0,
    height = 48)

med_name_img = PhotoImage(file = f"developer_images/img_textBox1.png")
med_name_bg = canvas.create_image(
    632.0, 180.0,
    image = med_name_img)

med_name_var=StringVar()
med_name = Entry(
    bd = 0,
    bg = "#c4c4c4",
    highlightthickness = 0,
    font=('ARIAL',15),
    textvariable=med_name_var)

med_name.place(
    x = 532.0, y = 155,
    width = 200.0,
    height = 48)

med_price_img = PhotoImage(file = f"developer_images/img_textBox2.png")
med_price_bg = canvas.create_image(
    332.0, 292.0,
    image = med_price_img)

med_price_var=StringVar()
med_price = Entry(
    bd = 0,
    bg = "#c4c4c4",
    highlightthickness = 0,
    font=('ARIAL',15),
    textvariable=med_price_var)

med_price.place(
    x = 232.0, y = 267,
    width = 200.0,
    height = 48)

med_des_img = PhotoImage(file = f"developer_images/img_textBox3.png")
med_des_bg = canvas.create_image(
    636.0, 292.0,
    image = med_des_img)

med_des_var=StringVar()
med_des = Entry(
    bd = 0,
    bg = "#c4c4c4",
    highlightthickness = 0,
    font=('ARIAL',15),
    textvariable=med_des_var)

med_des.place(
    x = 536.0, y = 267,
    width = 200.0,
    height = 48)

back_btn_img = PhotoImage(file = f"developer_images/img0.png")
back_btn = Button(
    image = back_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = back,
    relief = "flat")

back_btn.place(
    x = 18, y = 21,
    width = 75,
    height = 55)

reset_btn_img = PhotoImage(file = f"developer_images/img1.png")
reset_btn = Button(
    image = reset_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = reset,
    relief = "flat")

reset_btn.place(
    x = 1059, y = 588,
    width = 232,
    height = 80)

search_btn_img = PhotoImage(file = f"developer_images/img2.png")
search_btn = Button(
    image = search_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = search,
    relief = "flat")

search_btn.place(
    x = 1059, y = 486,
    width = 232,
    height = 80)

delete_btn_img = PhotoImage(file = f"developer_images/img3.png")
delete_btn = Button(
    image = delete_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = delete,
    relief = "flat")

delete_btn.place(
    x = 1059, y = 384,
    width = 232,
    height = 80)

update_btn_img = PhotoImage(file = f"developer_images/img4.png")
update_btn = Button(
    image = update_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = update,
    relief = "flat")

update_btn.place(
    x = 1059, y = 282,
    width = 232,
    height = 80)

display_btn_img = PhotoImage(file = f"developer_images/img5.png")
display_btn = Button(
    image = display_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = display,
    relief = "flat")

display_btn.place(
    x = 1059, y = 180,
    width = 232,
    height = 80)

add_btn_img = PhotoImage(file = f"developer_images/img6.png")
add_btn = Button(
    image = add_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = add,
    relief = "flat")

add_btn.place(
    x = 1059, y = 78,
    width = 232,
    height = 80)

upload_btn_img = PhotoImage(file = f"developer_images/img7.png")
upload_btn = Button(
    image = upload_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = image,
    relief = "flat")

upload_btn.place(
    x = 805, y = 200,
    width = 210,
    height = 60)

left_frame=Frame(window,bg='red')
left_frame.place(x=140,y=345,width=840,height=313)

scroll_y=Scrollbar(left_frame,orient=VERTICAL)


med_info=ttk.Treeview(left_frame,height=7,columns=("id","name","description","price"),yscrollcommand=scroll_y.set)
scroll_y.pack(side=RIGHT,fill=Y)

med_info.heading("id",text="ID")
med_info.heading("name",text="MEDICINE NAME")
med_info.heading("description",text="DESCRIPTION")
med_info.heading("price",text="PRICE")

med_info['show']='headings'

med_info.column("id",width=15)
med_info.column("name",width=15)
med_info.column("description",width=15)
med_info.column("price",width=15)

med_info.pack(fill=BOTH,expand=1)
med_info.bind("<ButtonRelease-1>",displayvalue)
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", Exit)
window.mainloop()
