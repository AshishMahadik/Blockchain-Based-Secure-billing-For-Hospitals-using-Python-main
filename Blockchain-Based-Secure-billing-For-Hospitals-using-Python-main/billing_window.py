from tkinter import font
from tkinter import * 
from tkinter import ttk,messagebox
from tkinter.simpledialog import askinteger
import mysql.connector as mysql
import tkinter.ttk as ttk
import math,random
import os
import hashlib
import cv2
import time
import datetime

###################### FUNCTION TO GENERATE RANDOM NUMBER FOR BILL NO ######################

def generateNo():
    generateNo.x=random.randint(1000,99999)
    return generateNo.x
 

############## CHECKING FOR GENESIS ROW IN BILL_INFO TABLE ##################

db=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
mycursor=db.cursor()
mycursor.execute("SELECT COUNT(*) AS rowCount FROM bill_info")
emptyRow=mycursor.fetchone()
if emptyRow[0]==0:
    print('table is empty')
    os.system("genesis_row.py")
    print("genesis row added")




###################### FUNCTION TO SEARCH THE PATIENT INFORMATION BASED ON THEIR PID OR BILL NO ######################

def searchInfo():
    
    if p_id_var.get()!="":

        try:

            mydb=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb.cursor()
            mycursor.execute("SELECT * FROM p_info where p_id LIKE '%"+p_id_var.get()+"%'")
            result=mycursor.fetchall()
            if len(result) > 0:
                for row in result:
                    p_id_var.set(row[0])
                    name_var.set(row[1])
                    cno_var.set(row[2])
                    age_var.set(row[3])
                    blood_group_var.set(row[5])
                    addr_var.set(row[6])
                    gender_var.set(row[7])
                    welcome_bill() # ---> IF condition satisfies calling the function
            else:
                messagebox.showerror("error","patient not found",parent=window)
        except Exception as e:
            messagebox.showinfo("","{}".format(e),parent=window)
       
        mydb.close()
    
    elif bill_no_var.get()!="":
        try:

            mydb2=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb2.cursor()
            
            mycursor.execute("SELECT * FROM bill_info where bill_no LIKE '%"+ bill_no_var.get()+"%'")
            result=mycursor.fetchone()
            textarea.delete('1.0',END)
            textarea.insert(END,result[3])
            mycursor.execute("SELECT * FROM p_info where p_id={}".format(str(result[1])))
            p_id_res=mycursor.fetchall()
            if len(p_id_res)> 0:
                for row in p_id_res:

                    p_id_var.set(row[0])
                    name_var.set(row[1])
                    cno_var.set(row[2])
                    age_var.set(row[3])
                    blood_group_var.set(row[5])
                    addr_var.set(row[6])
                    gender_var.set(row[7])
                print(p_id_res)
            block_time()
        except Exception as es:
            messagebox.showerror("ERROR","BILL NOT FOUND",parent=window)
            mydb2.commit()
            mydb2.close()


###################### FUNCTION FOR RESETING INFORMATION IN PATIENT DETAIL FRAME ######################

def reset():
    p_id.delete(0,END)
    name.delete(0,END)
    cno.delete(0,END)
    age.delete(0,END)
    blood_group.delete(0,END)
    addr.delete(0,END)
    gender.delete(0,END)
    bill_no.delete(0,END)
    textarea.delete('1.0',END)
    generateNo() # -----> CALLING THE SAME RANDOM NO GENERATION FUNCTION
    

def by_name():
        try:

            mydb=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb.cursor()
            mycursor.execute("SELECT * FROM med_info where med_name LIKE '%"+search_by_name_var.get()+"%'")
            result=mycursor.fetchall()
            if len(result) > 0:
                med_info.delete(*med_info.get_children())
                for row in result:
                    med_info.insert('',END,values =row)
            else:
                med_info.delete(*med_info.get_children())
            mydb.commit()
        except Exception as es:
            messagebox.showinfo("","{}".format(es),parent=window)
            mydb.close()



def checkhash():
    mydb5=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb5.cursor()
    bill_data=textarea.get('1.0',END)
    f1=open("bills/{}.csv".format(bill_no_var.get()),"w")
    f1.write(bill_data)
    f1.close()
    with open("bills/{}.csv".format(bill_no_var.get()),'rb') as f:
            binary_file = f.read()
    mycursor.execute("insert into check_hash (p_id,bill_no,bill_file) values(%s,%s,%s)",
                    (
                                p_id_var.get(),
                                bill_no_var.get(),
                                binary_file
                    )
                    )
                
    mydb5.commit()
    mydb5.close()

    mydb6=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb6.cursor()
    mycursor.execute("SELECT * FROM bill_info where bill_no LIKE '%"+bill_no_var.get()+"%'")
    res_of_prev_hash=mycursor.fetchone()
    mydb6.commit()
    mydb6.close()

    mydb7=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb7.cursor()
    mycursor.execute("UPDATE check_hash SET prev_hash='{}' WHERE (bill_no = '{}')".format(str(res_of_prev_hash[4]),bill_no_var.get()))
    mydb7.commit()
    mydb7.close()

    mydb8=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb8.cursor()
    mycursor.execute("SELECT * FROM check_hash where bill_no LIKE '%"+bill_no_var.get()+"%'") 
    result=mycursor.fetchone()
    hashedvalue1=hashlib.sha256(str(result).encode('utf-8')).hexdigest()
    mydb8.commit()
    mydb8.close()
    os.remove("bills/{}.csv".format(bill_no_var.get()))
    
    mydb9=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb9.cursor()
    mycursor.execute("UPDATE check_hash SET c_hash='{}' WHERE (bill_no = '{}')".format(hashedvalue1,bill_no.get()))
    mydb9.commit()
    mydb9.close()
    
    mydb10=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb10.cursor()
    mycursor.execute("SELECT c_hash FROM check_hash where bill_no LIKE '%"+bill_no_var.get()+"%'") 
    fetch_hash=mycursor.fetchone()
    if str(fetch_hash)!=res_of_prev_hash[4]:
        messagebox.showerror("error","The BILL BLOCK is already present...!\nDuplicate BILL BLOCKS are not allowed !")
        mycursor.execute("truncate table check_hash") 
        mydb10.close()


###################### FUNCTION FOR GENERATE BILL BUTTON ######################

def generate_bill():
    mydb0=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb0.cursor()  
    mycursor.execute("SELECT * FROM bill_info where bill_no LIKE '%"+bill_no_var.get()+"%'")
    res2=mycursor.fetchone()
    
    if res2!=None:
        checkhash() 
        mydb0.close()
    else:
        op=messagebox.askyesno("save bill","Do You Want To Save?")
        if op >0:
            
            mydb1=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb1.cursor()
            bill_data=textarea.get('1.0',END)
            f1=open("bills/{}.csv".format(bill_no_var.get()),"w")
            f1.write(bill_data)
            f1.close()
            with open("bills/{}.csv".format(bill_no_var.get()),'rb') as f:
                    binary_file = f.read()
            mycursor.execute("insert into bill_info (p_id,bill_no,bill_file) values(%s,%s,%s)",
                            (
                                p_id_var.get(),
                                bill_no_var.get(),
                                binary_file
                            )
                            )
                
            mydb1.commit()
            mydb1.close()
            os.remove("bills/{}.csv".format(bill_no_var.get()))

            mydb2=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb2.cursor()
            mycursor.execute("SELECT c_hash FROM bill_info ORDER BY c_hash DESC LIMIT 2")   
            pre_res=mycursor.fetchone()  
            prev=pre_res[0]   
            mydb2.close

            mydb3=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb3.cursor()
            mycursor.execute("UPDATE bill_info SET prev_hash='{}' WHERE (bill_no = '{}')".format(prev,bill_no_var.get()))
            mydb3.commit()
            mycursor.execute("SELECT * FROM bill_info where bill_no LIKE '%"+bill_no_var.get()+"%'") 
            result=mycursor.fetchone()
            hashedvalue=hashlib.sha256(str(result).encode('utf-8')).hexdigest()
            mydb3.commit()
            mydb3.close()


            mydb4=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
            mycursor=mydb4.cursor()
            mycursor.execute("UPDATE bill_info SET c_hash='{}' WHERE (bill_no = '{}')".format(hashedvalue,bill_no_var.get()))
            mydb4.commit()
            mydb4.close()


        else:
            return
    upload_time()
    textarea.configure(state="disable")
    
    
    



###################### FUNCTION FOR ADD BUTTON ######################

def add():
    view = med_info.focus()
    holdData = med_info.item(view)
    rece_row = holdData['values']
    qty = askinteger('Quantity', 'Quantity')
    add.price = qty*float(rece_row[3])

    # WHTEVER ADDITION DONE ABOVE WILL BE INSERTED INTO BILL AREA 
    textarea.insert(END,f"  {rece_row[1]}")
    textarea.insert(END,f"                                      {rece_row[2]}")
    textarea.insert(END,"\t\t\t\t\t"f"                     {qty}")
    textarea.insert(END,"\t\t"f"                   {add.price}")
    textarea.insert(END,'\n')
    store_total()
    

###################### FUNCTION TO STORE THE PRICE  IN THE DB AFTER SELECTING QTY ######################

def store_total():
    mydb1=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb1.cursor()
    mycursor.execute("insert into price (price_1,price_2) values(%s,%s)",(add.price,add.price))
    mydb1.commit()
    mydb1.close()


###################### FUNCTION FOR TOTAL BUTTON ######################    
    
def total():
    textarea.configure(state="normal")
    textarea.insert(END,"\n==================================================================")
    mydb1=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydb1.cursor()
    mycursor.execute("select SUM(price_1) from price") # ----> THIS WILL SUM ALL THE PRICES IN THE DB
    result=mycursor.fetchone()
    textarea.insert(END,f"\n  Total: \t\t\t\t\t\t\t               Rs.{result[0]}")
    mydb1.commit()
    truncatedb=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=truncatedb.cursor()
    mycursor.execute("truncate table price")
    truncatedb.commit()
    truncatedb.close()
    mydb1.close()


###################### FUNCTION FOR CLEAR BUTTON ######################

def clear():
    textarea.configure(state="normal")
    textarea.delete('1.0',END)
    #deleteing whtever present in the treeview
    for i in med_info.get_children():
        med_info.delete(i)
        window.update()
    welcome_bill_with_same_bill_no()



def welcome_bill_with_same_bill_no():

    textarea.insert(END,"==================================================================")
    textarea.insert(END,f"  PATIENT ID : {p_id_var.get()}")
    textarea.insert(END,"\t\t\t\t\t"f"BILL NO : {bill_no_var.get()}")
    textarea.insert(END,f"\n  PATIENT NAME : {name_var.get()}")
    textarea.insert(END,"\t\t\t\t"f"\tCONTACT NO : {cno_var.get()}")
    textarea.insert(END,"\n==================================================================")
    textarea.insert(END,"\n   Medicine\t\t                 Description\t\t             \t\t  QTY\t                   Price")
    textarea.insert(END,"\n-----------------------------------------------------------------------------------------------------------------------\n")
    

###################### FUNCTION FOR EXIT BUTTON ######################

def exit():
    
    answer=messagebox.askyesno('EXIT','Do You Want To Exit?')
    if answer > 0:
        window.destroy()
        os.system("user_welcom.py")
    else:
        return



###################### FUNCTION FOR BILL HEADER ######################

def preview_photo():
    view = med_info.focus()
    holdData = med_info.item(view)
    row_received = holdData['values']
    #image having 4th indes
    
    mydbpic=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor=mydbpic.cursor()
    mycursor.execute("select image from med_info where med_id={}".format(row_received[0])) # ----> THIS WILL SUM ALL THE PRICES IN THE DB
    result=mycursor.fetchone()
    fetch_image=result[0]
    mydbpic.commit()
    mydbpic.close()
    with open ("fetch_IMG/image.jpeg",'wb') as f:
        f.write(fetch_image)
    get_img=cv2.imread("fetch_IMG/image.jpeg")
    cv2.imshow("PriceTag",get_img)
    
    if cv2.waitKey()%256==27:
        
        cv2.destroyAllWindows()
    os.remove("fetch_IMG/image.jpeg")


def welcome_bill():
    textarea.delete('1.0',END)
    # CALLING THE RANDOM NUMBER GENERATOR FUNCTION TO GENERATE RANDOM NUMBER
    generateNo()
    bill_no_var.set(str(generateNo.x))
    textarea.insert(END,"==================================================================")
    textarea.insert(END,f"  PATIENT ID : {p_id_var.get()}")
    textarea.insert(END,"\t\t\t\t\t"f"BILL NO : {bill_no_var.get()}")
    textarea.insert(END,f"\n PATIENT NAME : {name_var.get()}")
    textarea.insert(END,"\t\t\t\t"f"\tCONTACT NO : {cno_var.get()}")
    textarea.insert(END,"\n==================================================================")
    textarea.insert(END,"\n   Medicine\t\t                 Description\t\t             \t\t  QTY\t                   Price")
    textarea.insert(END,"\n-----------------------------------------------------------------------------------------------------------------------\n")
    


def Exit():
        op=messagebox.askyesno("Log out","Are You Sure,You Want To EXIT?",parent=window)
        if op==True:
            window.destroy()

def upload_time():
    #code for date and time of generated bill
    no1 = datetime.datetime.now()
    blk_date= no1.strftime("%d-%m-%y")
    blk_time= no1.strftime("%H:%M:%S %p")
    mydb_blk1=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor_blk1=mydb_blk1.cursor()
    mycursor_blk1.execute("insert into block_time (bill_no,blk_date,blk_time) values(%s,%s,%s)",
                            (
                                bill_no_var.get(),
                                blk_date,
                                blk_time
                            )
                        )
    mydb_blk1.commit()
    
    block_time()
    
def block_time():
    
    mydb_blk=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor_blk=mydb_blk.cursor()  
    mycursor_blk.execute("SELECT * FROM bill_info where bill_no LIKE '%"+bill_no_var.get()+"%'")
    result_blk=mycursor_blk.fetchone()
    
    mydb_blk2=mysql.connect(host="127.0.0.1",user="manish",password="manish",database="med")
    mycursor_blk2=mydb_blk2.cursor()  
    mycursor_blk2.execute("SELECT * FROM block_time where bill_no LIKE '%"+bill_no_var.get()+"%'")
    result_blk2=mycursor_blk2.fetchone()
    
    print(result_blk)
    textarea.insert(END,"\n\n============================Block Information==========================")
    textarea.insert(END,f"\n Block Id       :  {result_blk2[0]}")
    textarea.insert(END,f"\n Block Date  :  {result_blk2[2]}")
    textarea.insert(END,f"\n Block Time  :  {result_blk2[3]}")
    textarea.insert(END,f"\n\n Previous Block Hash : \n\t\n      {result_blk[0]}")
    textarea.insert(END,f"\n\n Current Block Hash : \n\t\n     {result_blk[4]}")
    textarea.insert(END,"\n==================================================================")
   
        
        
        
        
        
        
        
window = Tk()

#code for tkinter window in centre in screen
window_width,window_height = 1300,690

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

position_top = int(screen_height / 2.2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

window.configure(bg = "#284a53")
canvas = Canvas(
    window,
    bg = "#284a53",
    height = 690,
    width = 1300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"billing_images/rsz_background.png")
background = canvas.create_image(
    650, 345,
    image=background_img)

p_id_img = PhotoImage(file = f"billing_images/img_textBox0.png")
p_id_bg = canvas.create_image(
    230.0, 132.0,
    image = p_id_img)

p_id_var=StringVar()
p_id = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=p_id_var)

p_id.place(
    x = 175.0, y = 112,
    width = 110.0,
    height = 38)

name_img = PhotoImage(file = f"billing_images/img_textBox1.png")
name_bg = canvas.create_image(
    503.0, 131.0,
    image = name_img)

name_var=StringVar()
name = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=name_var)

name.place(
    x = 448.0, y = 111,
    width = 110.0,
    height = 38)

gender_img = PhotoImage(file = f"billing_images/img_textBox2.png")
gender_bg = canvas.create_image(
    756.0, 131.0,
    image = gender_img)

gender_var=StringVar()
gender = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=gender_var)

gender.place(
    x = 701.0, y = 111,
    width = 110.0,
    height = 38)

age_img = PhotoImage(file = f"billing_images/img_textBox3.png")
age_bg = canvas.create_image(
    1004.0, 131.0,
    image = age_img)

age_var=StringVar()
age = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=age_var)

age.place(
    x = 949.0, y = 111,
    width = 110.0,
    height = 38)

blood_group_img = PhotoImage(file = f"billing_images/img_textBox4.png")
blood_group_bg = canvas.create_image(
    230.0, 189.0,
    image = blood_group_img)

blood_group_var=StringVar()
blood_group = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=blood_group_var)

blood_group.place(
    x = 175.0, y = 169,
    width = 110.0,
    height = 38)

cno_img = PhotoImage(file = f"billing_images/img_textBox5.png")
cno_bg = canvas.create_image(
    503.0, 189.0,
    image = cno_img)

cno_var=StringVar()
cno = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=cno_var)

cno.place(
    x = 448.0, y = 169,
    width = 110.0,
    height = 38)

addr_img = PhotoImage(file = f"billing_images/img_textBox6.png")
addr_bg = canvas.create_image(
    756.0, 190.0,
    image = addr_img)

addr_var=StringVar()
addr = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=addr_var)

addr.place(
    x = 701.0, y = 170,
    width = 110.0,
    height = 38)

bill_no_img = PhotoImage(file = f"billing_images/img_textBox7.png")
bill_no_bg = canvas.create_image(
    1004.0, 190.0,
    image = bill_no_img)

bill_no_var=StringVar()
bill_no = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=bill_no_var)

bill_no.place(
    x = 949.0, y = 170,
    width = 110.0,
    height = 38)

search_by_name_img = PhotoImage(file = f"billing_images/img_textBox8.png")
search_by_name_bg = canvas.create_image(
    326.0, 259.0,
    image = search_by_name_img)

search_by_name_var=StringVar()
search_by_name = Entry(
    bd = 0,
    bg = "#ffd7be",
    highlightthickness = 0,
    font=('ARIAL',12),
    textvariable=search_by_name_var)

search_by_name.place(
    x = 214.0, y = 239,
    width = 224.0,
    height = 38)


reset_btn_img = PhotoImage(file = f"billing_images/img0.png")
reset_btn = Button(
    image = reset_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = reset,
    relief = "flat")

reset_btn.place(
    x = 1122, y = 101,
    width = 155,
    height = 55)

search_btn_img = PhotoImage(file = f"billing_images/img1.png")
search_btn = Button(
    image = search_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = searchInfo,
    relief = "flat")

search_btn.place(
    x = 1122, y = 166,
    width = 155,
    height = 55)

search_by_name_btn_img = PhotoImage(file = f"billing_images/img2.png")
search_by_name_btn = Button(
    image = search_by_name_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = by_name,
    relief = "flat")

search_by_name_btn.place(
    x = 480, y = 232,
    width = 165,
    height = 55)

add_btn_img = PhotoImage(file = f"billing_images/img3.png")
add_btn = Button(
    image = add_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = add,
    relief = "flat")

add_btn.place(
    x = 69, y = 623,
    width = 155,
    height = 55)

total_btn_img = PhotoImage(file = f"billing_images/img4.png")
total_btn = Button(
    image = total_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = total,
    relief = "flat")

total_btn.place(
    x = 236, y = 623,
    width = 155,
    height = 55)

generate_btn_img = PhotoImage(file = f"billing_images/img5.png")
generate_btn = Button(
    image = generate_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = generate_bill,
    relief = "flat")

generate_btn.place(
    x = 404, y = 623,
    width = 155,
    height = 55)

preview_btn_img = PhotoImage(file = f"billing_images/img6.png")
preview_btn = Button(
    image = preview_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = preview_photo,
    relief = "flat")

preview_btn.place(
    x = 572, y = 623,
    width = 155,
    height = 55)

Print_btn_img = PhotoImage(file = f"billing_images/img7.png")
Print_btn = Button(
    image = Print_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    # command = btn_clicked,
    relief = "flat")

Print_btn.place(
    x = 740, y = 623,
    width = 155,
    height = 55)

clear_btn_img = PhotoImage(file = f"billing_images/img8.png")
clear_btn = Button(
    image = clear_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = clear,
    relief = "flat")

clear_btn.place(
    x = 908, y = 623,
    width = 155,
    height = 55)

exit_btn_img = PhotoImage(file = f"billing_images/img9.png")
exit_btn = Button(
    image = exit_btn_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = exit,
    relief = "flat")

exit_btn.place(
    x = 1076, y = 623,
    width = 155,
    height = 55)


###################### TREE VIEW AREA ######################

#CREATING FRAME FOR TREEVIEW
treeframe=Frame(window,bd=5,relief=GROOVE,bg='white')
treeframe.place(x=0,y=297,width=650,height=315)

# CREATING SCROLLBAR FOR TREEVIEW
scroll_y=Scrollbar(treeframe,orient=VERTICAL)
scroll_y.pack(side=RIGHT,fill=Y)

# CREATING TREE VIEW INSTANCE        
med_info=ttk.Treeview(treeframe,height=12,columns=("id","name","description","price","image"),yscrollcommand=scroll_y.set)
style = ttk.Style()
style.configure("Treeview.Heading", font=("times new roman", 10))
# MAKING COLUMN HEADERS
med_info.heading("id",text="ID")
med_info.heading("name",text="MEDICINE NAME")
med_info.heading("description",text="DESCRIPTION")
med_info.heading("price",text="PRICE")
med_info.heading("image",text="PHOTO")
med_info['show']='headings'

# MAKING ROW VALUE ALLIGNMENT 

med_info.column("id",width=5,minwidth=5,anchor=CENTER)
med_info.column("name",width=5)
med_info.column("description",width=5,anchor=CENTER)
med_info.column("price",width=5,anchor=CENTER)
med_info.column("image",width=0)
med_info.tag_configure('T',font=("times new roman", 10))
#CONFIGURING TREEVIEW
med_info.pack(fill=BOTH,expand=1)
med_info.bind("<ButtonRelease-1>",add)


###################### FRAME FOR BILLING AREA ######################

bill_area=Frame(window,bd=3,relief=GROOVE,bg='white')
bill_area.place(x=675,y=227,width=625,height=385)
bill_title=Label(bill_area,text='BILL AREA',font=('arial',15,'bold'),bd=6,relief=GROOVE).pack(fill=X)
bill_scroll_y=Scrollbar(bill_area,orient=VERTICAL)
textarea=Text(bill_area,yscrollcommand=bill_scroll_y.set,undo=True,font=('ARIAL',11))
bill_scroll_y.pack(side=RIGHT,fill=Y)
bill_scroll_y.config(command=textarea.yview)
textarea.pack(fill=BOTH,expand=1)
window.protocol("WM_DELETE_WINDOW", Exit)
window.resizable(False, False)
window.mainloop()






