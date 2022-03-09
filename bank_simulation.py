from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

con=sql.connect(database="bank.sqlite")
cur=con.cursor()
try:
    cur.execute("create table users(acn integer primary key autoincrement,name text,pass text,bal integer,mob text)")
    con.commit()
except Exception as e:
    print(e)
con.close()


win=Tk()
win.state("zoomed")
win.resizable(width=False,height=False)
win.configure(bg="powder blue")

title=Label(win,text="Bank Account Simulation",font=('Arial',60,'bold','underline'),bg="powder blue")
title.pack()

def login_frame():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def forgot_click():
        frm.destroy()
        forgot_frame()
        
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
        
    def login():
        acn=e_acn.get()
        p=e_pass.get()
        
        if(len(acn)==0 or len(p)==0):
             messagebox.showerror("Validation","Please fill both fields!")
        elif(acn.isdigit()==False):
             messagebox.showerror("Validation","Account No must be Numeric!")
        else:
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from users where acn=? and pass=?",(acn,p))
            global loginrow
            loginrow=cur.fetchone()
            if(loginrow==None):
                messagebox.showerror("Login","Invalid Username/Password")
            else:
                frm.destroy()
                welcome_frame()
            
    def open_click():
        frm.destroy()
        open_frame()
        

    lbl_acn=Label(frm,text="Account No",font=('Arial',20,'bold'),bg="pink")
    lbl_acn.place(relx=.3,rely=.2)
    
    lbl_pass=Label(frm,text="Password",font=('Arial',20,'bold'),bg="pink")
    lbl_pass.place(relx=.3,rely=.3)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.2)
    e_acn.focus()
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_pass.place(relx=.45,rely=.3)
    
    b_login=Button(frm,command=login,text="login",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_login.place(relx=.45,rely=.4)
    
    b_reset=Button(frm,command=reset,text="reset",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_reset.place(relx=.55,rely=.4)
    
    b_fp=Button(frm,command=forgot_click,text="forgot pass",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_fp.place(relx=.4,rely=.55)
    
    b_open=Button(frm,command=open_click,text="open account",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_open.place(relx=.54,rely=.55)

def forgot_frame():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back_click():
        frm.destroy()
        login_frame()
     
    def recover():
        a=e_acn.get()
        m=e_mob.get()
        con=sql.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select pass from users where acn=? and mob=?",(a,m))
        row=cur.fetchone()
        if(row==None):
            messagebox.showerror("Recover","Invalid ACN/MOB!")
        else:
            messagebox.showinfo("recover",f"Your Pass:{row[0]}")
            frm.destroy()
            login_frame()
        
    lbl_acn=Label(frm,text="Account No",font=('Arial',20,'bold'),bg="pink")
    lbl_acn.place(relx=.3,rely=.2)
    
    lbl_mob=Label(frm,text="Mob",font=('Arial',20,'bold'),bg="pink")
    lbl_mob.place(relx=.3,rely=.3)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.2)
    e_acn.focus()
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.3)
    
    b_recover=Button(frm,command=recover,text="recover",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_recover.place(relx=.45,rely=.4)
    
    b_reset=Button(frm,text="reset",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_reset.place(relx=.55,rely=.4)
    
    b_back=Button(frm,command=back_click,text="back",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_back.place(relx=0,rely=0)
  
def welcome_frame():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def logout():
        frm.destroy()
        login_frame()
    
    def checkbal_frame():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.2,relwidth=.6,relheight=.4)
        
        con=sql.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select bal from users where acn=?",(loginrow[0],))
        bal=cur.fetchone()
        lbl_bal=Label(ifrm,text=f"Available Balance:{bal[0]}",font=('Arial',30,'bold'),bg="pink")
        lbl_bal.place(relx=.2,rely=.2)
    
    
    def deposit_frame():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.2,relwidth=.6,relheight=.4)
    
        def submit():
            amt=int(e_amt.get())
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update users set bal=bal+? where acn=?",(amt,loginrow[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Deposit","Amount deposited!")
        lbl_amt=Label(ifrm,text="Amount:",font=('Arial',20,'bold'),bg="pink")
        lbl_amt.place(relx=.2,rely=.1)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.1)
        e_amt.focus()
        
        b_sub=Button(frm,command=submit,text="submit",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
        b_sub.place(relx=.5,rely=.35)
     
    
    def withdraw_frame():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.2,relwidth=.6,relheight=.4)
    
        def submit():
            amt=int(e_amt.get())
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select bal from users where acn=?",(loginrow[0],))
            bal=cur.fetchone()[0]
            con.close()
            if(bal>amt):
                con=sql.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("update users set bal=bal-? where acn=?",(amt,loginrow[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Deposit","Amount withdrawn!")
            else:
                messagebox.showwarning("Deposit","Insufficient Bal!")

        lbl_amt=Label(ifrm,text="Amount:",font=('Arial',20,'bold'),bg="pink")
        lbl_amt.place(relx=.2,rely=.1)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.1)
        e_amt.focus()
        
        b_sub=Button(frm,command=submit,text="submit",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
        b_sub.place(relx=.5,rely=.35)
    
    def transfer_frame():
        ifrm=Frame(frm)
        ifrm.configure(bg="pink")
        ifrm.place(relx=.2,rely=.2,relwidth=.6,relheight=.4)
    
        def submit():
            amt=int(e_amt.get())
            to=int(e_to.get())
            
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select bal from users where acn=?",(loginrow[0],))
            bal=cur.fetchone()[0]
            con.close()
            
            con=sql.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from users where acn=?",(to,))
            to_acn=cur.fetchone()
            con.close()
            if(to_acn==None):
                messagebox.showwarning("Transfer","Invalid To acn!")
            else:
                if(bal>amt):
                    con=sql.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("update users set bal=bal-? where acn=?",(amt,loginrow[0]))
                    cur.execute("update users set bal=bal+? where acn=?",(amt,to))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Deposit","Amount transfered!")
                else:
                    messagebox.showwarning("Deposit","Insufficient Bal!")

        lbl_amt=Label(ifrm,text="Amount:",font=('Arial',20,'bold'),bg="pink")
        lbl_amt.place(relx=.2,rely=.1)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.1)
        e_amt.focus()
        
        lbl_to=Label(ifrm,text="TO:",font=('Arial',20,'bold'),bg="pink")
        lbl_to.place(relx=.2,rely=.3)
        
        e_to=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.3)
                
        
        b_sub=Button(frm,command=submit,text="submit",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
        b_sub.place(relx=.5,rely=.55)
    
    
    
    lbl_wel=Label(frm,text=f"Welcome,{loginrow[1]}",font=('Arial',20,'bold'),bg="pink")
    lbl_wel.place(relx=0,rely=0)
    
    b_back=Button(frm,command=logout,text="logout",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_back.place(relx=.9,rely=0)
    
    b_bal=Button(frm,command=checkbal_frame,text="check bal",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_bal.place(relx=.01,rely=.1)
    
    b_dep=Button(frm,command=deposit_frame,text="deposit",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_dep.place(relx=.01,rely=.3)
    
    b_wd=Button(frm,command=withdraw_frame,text="withdraw",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_wd.place(relx=.01,rely=.5)
    
    b_tr=Button(frm,command=transfer_frame,text="transfer",width=10,font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_tr.place(relx=.01,rely=.7)
    
    
def open_frame():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back_click():
        frm.destroy()
        login_frame()
    
    def register():
        n=e_name.get()
        p=e_pass.get()
        m=e_mob.get()
        b=1000
    
        con=sql.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into users(name,pass,bal,mob) values(?,?,?,?)",(n,p,b,m))
        con.commit()
        
        cur.execute("select max(acn) from users")
        acn=cur.fetchone()[0]
        con.close()
        messagebox.showinfo("Register",f"Account opened with ACN:{acn}")
        frm.destroy()
        login_frame()
    
    lbl_name=Label(frm,text="Name",font=('Arial',20,'bold'),bg="pink")
    lbl_name.place(relx=.3,rely=.2)
    
    lbl_pass=Label(frm,text="Password",font=('Arial',20,'bold'),bg="pink")
    lbl_pass.place(relx=.3,rely=.3)
    
    lbl_mob=Label(frm,text="Mob",font=('Arial',20,'bold'),bg="pink")
    lbl_mob.place(relx=.3,rely=.4)
    
    
    e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_name.place(relx=.45,rely=.2)
    e_name.focus()
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.45,rely=.3)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.4)
    
    b_reg=Button(frm,command=register,text="register",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_reg.place(relx=.45,rely=.5)
    
    b_reset=Button(frm,text="reset",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_reset.place(relx=.55,rely=.5)
    
    b_back=Button(frm,command=back_click,text="back",font=('Arial',20,'bold'),bd=5,bg='powder blue')
    b_back.place(relx=0,rely=0)
  
     
login_frame()
win.mainloop()






