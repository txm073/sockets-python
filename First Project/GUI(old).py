import time
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import sys
import os
import re

USERNAME = ""

class LoginPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("Login")
        self.geometry("400x500+100+100")
        self.resizable(False,False)
        self.container = tk.Frame(self,height=50,width=50)
        self.container.pack(anchor=tk.N,fill=tk.BOTH,expand=True,side=tk.TOP)
        self.USERNAME = USERNAME

        image_exists = True
        try:
            self.image = ImageTk.PhotoImage(Image.open(os.path.join("Assets","background.png")))
        except FileNotFoundError:
            print("Could not find background image.")
            image_exists = False
        self.background = tk.Frame(self.container,bg="silver")
        self.background.place(x=0,y=0,relwidth=1,relheight=1)
        if image_exists == True:
            self.img_label = tk.Label(self.background,image=self.image)
            self.img_label.pack(anchor=tk.NW)

        self.login_frame = tk.Frame(self.container,bg="silver")
        self.login_frame.place(x=50,y=50,relwidth=0.75,relheight=0.8)

        self.info_btn = tk.Button(self.login_frame,text="i",width=2,
            font=("times new roman",15,"bold"),command=lambda: self.show_frame("info"))
        self.info_btn.pack(padx=5,pady=5,anchor=tk.NW)

        self.separator = tk.Frame(self.login_frame,bg="silver")
        self.separator.pack(side=tk.TOP,anchor=tk.N)
        self.sep_label = tk.Label(self.separator,text="YOU CAN'T SEE ME!",fg="silver",bg="silver",height=1)
        self.sep_label.pack()

        self.title_label = tk.Label(self.login_frame,text="Log In To The Server",fg="black",bg="silver",font=("calibri",18,"bold"))
        self.title_label.pack(padx=30,pady=10,anchor=tk.CENTER)

        self.user_label = tk.Label(self.login_frame,width=15,bg="silver",text="Enter Username:")
        self.user_label.pack(padx=45,anchor=tk.W)
        self.user_entry = tk.Entry(self.login_frame,width=55)
        self.user_entry.pack(padx=50,pady=3)

        self.pass_label = tk.Label(self.login_frame,width=15,bg="silver",text="Enter Password:")
        self.pass_label.pack(padx=45,anchor=tk.W)
        self.pass_entry = tk.Entry(self.login_frame,width=55,show="*")
        self.pass_entry.pack(padx=50,pady=3)

        self.login_btns_frame = tk.Frame(self.login_frame,bg="silver")
        self.login_btns_frame.pack(padx=44,pady=10,fill=tk.X)

        self.login_btn = tk.Button(self.login_btns_frame,text="Login",font=("calibri",10,"bold"),width=12,command=self.show_main)
        self.login_btn.grid(row=0,column=0,padx=6,pady=5,sticky=tk.W)
        self.exit_btn = tk.Button(self.login_btns_frame,text="Exit",font=("calibri",10,"bold"),width=12,command=self.exit)
        self.exit_btn.grid(row=0,column=1,padx=6,pady=5,sticky=tk.E)

        self.text = ("Welcome to the Overhill Drive \n"
                        "Local Area Network Server!\n"
                    "You can request to join the server \n"
                    "by clicking the button below and \n"
                        "filling out the form.")

        self.info_frame = tk.Frame(self.container,bg="silver")
        self.info_frame.place(x=50,y=50,relwidth=0.75,relheight=0.8)
        
        self.return_btn = tk.Button(self.info_frame,text="Back",font=("calibri",10,"bold"),command=self.show_login)
        self.return_btn.pack(anchor=tk.NW,padx=5,pady=5)
        self.info_label = tk.Label(self.info_frame,bg="silver",text=self.text,font=("calibri",14,"bold"))
        self.info_label.pack(anchor=tk.CENTER,padx=10,pady=35)
        self.request_btn = tk.Button(self.info_frame,text="Request To Join",font=("calibri",10,"bold"),width=12,command=lambda: self.show_frame("sign up"))
        self.request_btn.pack(anchor=tk.CENTER,padx=30)

        self.request_frame = tk.Frame(self.container,bg="silver")
        self.request_frame.place(x=50,y=50,relwidth=0.75,relheight=0.8)
        self.return_btn = tk.Button(self.request_frame,text="Back",font=("calibri",10,"bold"),command=lambda:self.show_frame("info"))
        self.return_btn.pack(anchor=tk.NW,padx=5,pady=5)
        self.label = tk.Label(self.request_frame,text="Sign Up",bg="silver",font=("calibri",14,"bold"))
        self.label.pack(padx=50,pady=35,anchor=tk.CENTER)

        self.login_response = tk.Frame(self.container,bg="silver")
        self.login_response.place(x=100,y=320,relwidth=0.5,relheight=0.05)
        self.invalid_label = tk.Label(self.login_response,text="Invalid username or password.",fg="red",bg="silver",font=("calibri",11,"bold"))
        self.invalid_label.pack(anchor=tk.CENTER)
        
        self.frames = {}
        self.frames["login"] = self.login_frame
        self.frames["background"] = self.background
        self.frames["wrong credentials"] = self.login_response
        self.frames["info"] = self.info_frame
        self.frames["sign up"] = self.request_frame

        self.show_login()
        self.mainloop()

    def exit(self):
        self.destroy()
        self.quit()

    def show_login(self):
        self.show_frame("background")
        self.show_frame("login")

    def show_main(self):
        global MainPage
        credentials = self.check_login()
        self.reset_fields()
        if credentials == True:
            print("Username =",self.USERNAME)
            self.exit()
            time.sleep(1)
            self.main = MainPage()
        else:
            self.show_login()
            self.show_frame("wrong credentials")

    def check_login(self):
        user = self.user_entry.get()
        password = self.pass_entry.get()

        with open(os.path.join("Assets","users.txt"),"r") as file:
            users = str(file.read()).split(", ")
        with open(os.path.join("Assets","passwords.txt"),"r") as file:
            passwords = str(file.read()).split(", ")

        if not user in users:
            return False
        if not password in passwords:
            return False

        valid_username = False
        valid_password = False
        user_index = 0
        password_index = 0
        for i, x in enumerate(users):
            if x == user:
                user_index = i
                break
        for i, x in enumerate(passwords):
            if x == password:
                password_index = i
                break
        if user_index == password_index:
            self.USERNAME = user
            return True
        return False

    def show_frame(self,page):
        frame = self.frames[page]
        frame.tkraise()

    def reset_fields(self):
        self.pass_entry.delete(0,tk.END)
        self.user_entry.delete(0,tk.END)

class MainPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
       
        self.title("Send Messages!")
        self.geometry("500x600+40+40")
        self.resizable(False,False)
        self.container = tk.Frame(self,height=50,width=50)
        self.container.pack(anchor=tk.N,fill=tk.BOTH,expand=True,side=tk.TOP)
        self.main = tk.Frame(self.container,bg="#1C1C1C") 
        self.main.pack(fill=tk.BOTH,expand=True)
        self.btns_frame = tk.Frame(self.main,bg="#1C1C1C")
        self.btns_frame.pack(padx=22,pady=15,fill=tk.BOTH,anchor=tk.CENTER)
        
        self.settings_btn = tk.Button(self.btns_frame,bg="black",fg="white",text="   ⚙   ",font=("calibri",12,"bold"),height=2)
        self.settings_btn.grid(row=0,column=0)
        self.priv_btn = tk.Button(self.btns_frame,bg="black",fg="white",text="Private Messages",font=("calibri",12,"bold"),width=19,height=2)
        self.priv_btn.grid(row=0,column=1)
        
        self.log_out_btn = tk.Button(self.btns_frame,bg="black",fg="white",text="Log Out",font=("calibri",12,"bold"),width=14,height=2,command=self.show_login)
        self.log_out_btn.grid(row=0,column=2)
        self.exit_btn = tk.Button(self.btns_frame,bg="black",fg="white",text="Exit",font=("calibri",12,"bold"),width=13,height=2,command=sys.exit)
        self.exit_btn.grid(row=0,column=3)

        self.message_box = tk.Text(self.main,bg="black",fg="white",state=tk.DISABLED,font=("calibri",12,"bold"),width=57,height=20)
        self.message_box.pack(anchor=tk.CENTER,padx=5,pady=12)

        self.message_label = tk.Label(self.main,bg="#1C1C1C",fg="white",font=("calibri",12,"bold"),text="Enter a message:")
        self.message_label.pack(padx=18,pady=5,anchor=tk.W)
        self.message_entry = tk.Text(self.main,bg="black",fg="white",font=("calibri",12,"bold"),width=57,height=2)
        self.message_entry.pack(padx=5,anchor=tk.CENTER)
        
        self.mainloop()

    def show_login(self):
        LoginPage.exit(self)
        LoginPage()


Thread(target=LoginPage).start()






