from tkinter import StringVar
import mysql.connector as mysql
import hashlib
class genesis():
    def __init__(self) -> None:
        
        mydb2=mysql.connect(host="127.0.0.1",user='manish',passwd='manish',database='med')
        mycursor=mydb2.cursor()
        
        # creating the data for genesis block
        phash='0'
        pid='0'
        bno='0'
        bill_data='this is genesis file for the blockchain'
        # making genesis dummy txt file for 1st row
        f1=open("bills/0.txt","w")
        f1.write(bill_data)
        f1.close()
        #reading it as binary for using its object for further operation on DB
        with open("bills/0.txt",'rb') as f:
            genesis_binary_file = f.read()

        #making tuple of the genesis row manually
        res=(phash,pid,bno,genesis_binary_file)

        #giving that tuple as an input to the hash function and generating hash
        crt_hash=hashlib.sha256(str(res).encode('utf-8')).hexdigest()

        #now insert an entire genesis row into the db as 1st row if the db is empty
        mycursor.execute("insert into bill_info (prev_hash,p_id,bill_no,bill_file,c_hash) values(%s,%s,%s,%s,%s)",
                                (
                                    phash,
                                    pid,
                                    bno,
                                    genesis_binary_file,
                                    crt_hash
                                )
                                )
        
        mydb2.commit()
        mydb2.close()

genesisOBj=genesis()
