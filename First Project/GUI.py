import time
import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import re

USERNAME = ""
light_theme = ["silver","black", "#b3b3b3","white"]
dark_theme = ["#1C1C1C","white","black","black"]
PATH = os.path.join("E:\\","Python","Socket Server","Assets")

FILE = os.path.basename(__file__)
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        CLIENT.connect(ADDR)
        print("connected")
    except ConnectionRefusedError:
        print("The server is not currently online.")
        sys.exit()
    except TimeoutError:
        print("Connection to the server timed out.")
        sys.exit()

def send(msg):
    enc_msg = msg.encode(FORMAT)
    enc_msg_len = str(len(enc_msg)).encode(FORMAT)
    enc_msg_len += b" " * (HEADER - len(enc_msg_len))
    try:
        CLIENT.send(enc_msg_len)
        CLIENT.send(enc_msg)     
    except ConnectionAbortedError:
        pass

def theme(choice):
    if choice == "light":
        theme = light_theme
        background = "light background.png"
    elif choice == "dark":
        theme = dark_theme    
        background = "dark background.png"
    return theme, background

def update():
    with open(os.path.join(PATH,"updates.txt"),"r") as file:
        news = str(file.read())
        if news:
            return news
        return "There are no updates available"

def run_theme():
    with open(os.path.join(PATH,"current theme.txt"),"r") as file:
        current_theme = str(file.read())
        colours, background = theme(current_theme)
        BG = colours[0]
        TEXT = colours[1]
        BTN = colours[2]
        BOX = colours[3]
    return BG,TEXT,BTN,BOX

class LoginPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.updates = update()
        BG,TEXT,BTN,BOX = run_theme()
        if BG == "#1C1C1C":
            background = "dark background.png"
        else:
            background = "light background.png"
        self.title("Login")
        self.geometry("400x500+100+100")
        self.resizable(False,False)
        self.container = tk.Frame(self,height=50,width=50)
        self.container.pack(anchor=tk.N,fill=tk.BOTH,expand=True,side=tk.TOP)
        self.USERNAME = USERNAME

        image_exists = True
        try:
            self.image = ImageTk.PhotoImage(Image.open(os.path.join(PATH,background)))
        except FileNotFoundError:
            print("Could not find background image.")
            image_exists = False
        self.subst_bg = ""
        if BG == "#1C1C1C":
            self.subst_bg = "#3a3b3c"
        else:
            self.subst_bg = "#F0F0F0"
        self.background = tk.Frame(self.container,bg=self.subst_bg)
        self.background.place(x=0,y=0,relwidth=1,relheight=1)
        if image_exists == True:
            self.img_label = tk.Label(self.background,image=self.image)
            self.img_label.pack(anchor=tk.NW)

        self.login_frame = tk.Frame(self.container,bg=BG)
        self.login_frame.place(x=50,y=50,relwidth=0.75,relheight=0.8)

        self.info_btn = tk.Button(self.login_frame,bg=BTN,text="i",width=2,fg=TEXT,
            font=("times new roman",15,"bold"),command=lambda: self.show_frame("info"))
        self.info_btn.pack(padx=5,pady=5,anchor=tk.NW)

        self.separator = tk.Frame(self.login_frame,bg=BG)
        self.separator.pack(side=tk.TOP,anchor=tk.N)
        self.sep_label = tk.Label(self.separator,text="YOU CAN'T SEE ME!",fg=BG,bg=BG,height=1)
        self.sep_label.pack()

        self.title_label = tk.Label(self.login_frame,text="Log In To The Server",fg=TEXT,bg=BG,font=("calibri",18,"bold"))
        self.title_label.pack(padx=30,pady=10,anchor=tk.CENTER)

        self.user_label = tk.Label(self.login_frame,width=15,fg=TEXT,bg=BG,text="Enter Username:")
        self.user_label.pack(padx=45,anchor=tk.W)
        self.user_entry = tk.Entry(self.login_frame,width=55,bg=BOX,fg=TEXT)
        self.user_entry.pack(padx=50,pady=3)

        self.pass_label = tk.Label(self.login_frame,width=15,fg=TEXT,bg=BG,text="Enter Password:")
        self.pass_label.pack(padx=45,anchor=tk.W)
        self.pass_entry = tk.Entry(self.login_frame,width=55,show="*",bg=BOX,fg=TEXT)
        self.pass_entry.pack(padx=50,pady=3)

        self.login_btns_frame = tk.Frame(self.login_frame,bg=BG)
        self.login_btns_frame.pack(padx=44,pady=10,fill=tk.X)

        self.login_btn = tk.Button(self.login_btns_frame,bg=BTN,text="Login",fg=TEXT,font=("calibri",10,"bold"),width=12,command=self.log_in)
        self.login_btn.grid(row=0,column=0,padx=6,pady=5,sticky=tk.W)
        self.exit_btn = tk.Button(self.login_btns_frame,bg=BTN,text="Exit",fg=TEXT,font=("calibri",10,"bold"),width=12,command=self.exit_page)
        self.exit_btn.grid(row=0,column=1,padx=6,pady=5,sticky=tk.E)

        self.text = ("You can request to \njoin the server\n"
                    "by clicking the \nbutton below and\n"
                        "filling out the form.")

        self.info_frame = tk.Frame(self.container,bg=BG)
        self.info_frame.place(x=50,y=50,relwidth=0.75,relheight=0.8)
        
        self.btns_frame = tk.Frame(self.info_frame,bg=BG)
        self.btns_frame.pack(anchor=tk.NW)
        self.return_btn = tk.Button(self.btns_frame,bg=BTN,text="Back",fg=TEXT,font=("calibri",10,"bold"),command=self.show_login)
        self.return_btn.grid(row=0,column=0,padx=5,pady=5)
        self.updates_btn = tk.Button(self.btns_frame,bg=BTN,text="Updates",fg=TEXT,font=("calibri",10,"bold"),command=lambda:self.show_frame("updates"))
        self.updates_btn.grid(row=0,column=1,pady=5)

        self.info_label = tk.Label(self.info_frame,bg=BG,fg=TEXT,text=self.text,font=("calibri",14,"bold"))
        self.info_label.pack(anchor=tk.CENTER,padx=10,pady=20)

        self.request_btn = tk.Button(self.info_frame,bg=BTN,text="Request To Join",fg=TEXT,font=("calibri",10,"bold"),width=12,command=lambda: self.show_frame("sign up"))
        self.request_btn.pack(anchor=tk.CENTER,padx=30)
        self.blank_label = tk.Label(self.info_frame,bg=BG,fg=BG,text="You cant see me",height=4)
        self.blank_label.pack(anchor=tk.CENTER,padx=30,fill=tk.X)
        
        self.updates_frame = tk.Frame(self.container,bg=BG)
        self.updates_frame.place(x=55,y=320)
        self.update_label = tk.Label(self.updates_frame,bg=BG,fg=TEXT,text="[UPDATE]",font=("calibri",12,"bold"))
        self.update_label.pack(anchor=tk.W,padx=10,pady=3)
        self.update_label = tk.Label(self.updates_frame,bg=BG,fg=TEXT,text=self.updates,font=("calibri",12,"bold"))
        self.update_label.pack(anchor=tk.CENTER,padx=10,pady=3)

        self.request_frame = tk.Frame(self.container,bg=BG)
        self.request_frame.place(x=50,y=50,relwidth=0.75,relheight=0.8)
        self.return_btn = tk.Button(self.request_frame,text="Back",bg=BTN,font=("calibri",10,"bold"),fg=TEXT,command=lambda:self.show_frame("info"))
        self.return_btn.pack(anchor=tk.NW,padx=5,pady=5)
        self.label = tk.Label(self.request_frame,text="Sign Up",bg=BG,fg=TEXT,font=("calibri",14,"bold"))
        self.label.pack(padx=50,pady=35,anchor=tk.CENTER)

        self.login_response = tk.Frame(self.container,bg=BG)
        self.login_response.place(x=100,y=320,relwidth=0.5,relheight=0.05)
        self.error_label = tk.Label(self.login_response,text="Invalid username or password.",fg="red",bg=BG,font=("calibri",11,"bold"))
        self.error_label.pack(anchor=tk.CENTER)
        
        self.frames = {}
        self.frames["login"] = self.login_frame
        self.frames["background"] = self.background
        self.frames["wrong credentials"] = self.login_response
        self.frames["info"] = self.info_frame
        self.frames["sign up"] = self.request_frame
        self.frames["updates"] = self.updates_frame

        self.show_login()
        self.mainloop()

    def exit_page(self):
        self.destroy()
        self.quit()

    def log_in(self):
        self.USERNAME = str(self.user_entry.get())
        self.PASSWORD = str(self.pass_entry.get()) 
        global USERNAME
        USERNAME = self.USERNAME
        if self.USERNAME and self.PASSWORD:
            print(self.USERNAME+"   "+self.PASSWORD)
            send(self.USERNAME+"   "+self.PASSWORD)
        self.ans_len = len(CLIENT.recv(HEADER).decode(FORMAT))
        self.ans = CLIENT.recv(self.ans_len).decode(FORMAT)
        self.reset_fields()
        if self.ans[:3] == "YES":
            self.exit_page()
            self.main = MainPage()
        else:
            self.show_frame("wrong credentials")

    def show_login(self):
        self.show_frame("background")
        self.show_frame("login")

    def show_frame(self,page):
        frame = self.frames[page]
        frame.tkraise()

    def reset_fields(self):
        self.pass_entry.delete(0,tk.END)
        self.user_entry.delete(0,tk.END)

class MainPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.pick_up = threading.Thread(target=self.pick_up).start()

        BG,TEXT,BTN,BOX = run_theme()
        self.title("Send Messages!")
        self.geometry("500x600+40+40")
        self.resizable(False,False)
        self.container = tk.Frame(self,height=50,width=50)
        self.container.pack(anchor=tk.N,fill=tk.BOTH,expand=True,side=tk.TOP)

        self.main = tk.Frame(self.container,bg=BG) 
        self.main.pack(fill=tk.BOTH,expand=True)

        self.btns_frame = tk.Frame(self.main,bg=BG)
        self.btns_frame.pack(padx=22,pady=15,fill=tk.BOTH,anchor=tk.CENTER)
        
        self.settings_btn = tk.Button(self.btns_frame,bg=BTN,fg=TEXT,text="   ⚙   ",font=("calibri",12,"bold"),height=2,command=lambda:self.show_frame("settings"))
        self.settings_btn.grid(row=0,column=0)
        
        self.priv_btn = tk.Button(self.btns_frame,bg=BTN,fg=TEXT,text="Private Messages",font=("calibri",12,"bold"),width=19,height=2)
        self.priv_btn.grid(row=0,column=1,padx=5)
        
        self.log_out_btn = tk.Button(self.btns_frame,bg=BTN,fg=TEXT,text="Log Out",font=("calibri",12,"bold"),width=14,height=2,command=self.log_out)
        self.log_out_btn.grid(row=0,column=2)
        
        self.exit_btn = tk.Button(self.btns_frame,bg=BTN,fg=TEXT,text="Exit",font=("calibri",12,"bold"),width=11,height=2,command=sys.exit)
        self.exit_btn.grid(row=0,column=3,padx=5)

        self.message_box = tk.Text(self.main,bg=BOX,fg=TEXT,font=("calibri",12,"bold"),width=57,height=20)
        self.message_box.pack(anchor=tk.CENTER,padx=5,pady=12)
        self.message_label = tk.Label(self.main,bg=BG,fg=TEXT,font=("calibri",12,"bold"),text="Enter a message:")
        self.message_label.pack(padx=18,pady=5,anchor=tk.W)
        self.entry_frame = tk.Frame(self.main,bg=BG)
        self.entry_frame.pack(padx=18,anchor=tk.W)
        self.message_entry = tk.Text(self.entry_frame,bg=BOX,fg=TEXT,font=("calibri",12,"bold"),width=52,height=2)
        self.message_entry.grid(row=0,column=0)
        
        self.send_btn = tk.Button(self.entry_frame,text="⚞",bg=BTN,fg=TEXT,font=("calibri",15,"bold"),command=self.send_msg)
        self.send_btn.grid(row=0,column=1,sticky="nsew",padx=5)

        self.settings = tk.Frame(self.container,bg=BG)
        self.settings.place(x=125,y=150,relwidth=0.5,relheight=0.5)
        self.return_btn = tk.Button(self.settings,bg=BTN,text="Back",fg=TEXT,font=("calibri",10,"bold"),command=lambda:self.show_frame("main"))
        self.return_btn.pack(anchor=tk.NW,padx=5,pady=5)

        self.settings_lbl = tk.Label(self.settings,bg=BG,fg=TEXT,text="Settings",font=("calibri",18,"bold"))
        self.settings_lbl.pack(anchor=tk.CENTER,pady=10)
        self.change_username_btn = tk.Button(self.settings,bg=BTN,text="Change Username",fg=TEXT,font=("calibri",10,"bold"),
            width=20,height=1)
        self.change_username_btn.pack(padx=40,pady=5)

        self.change_password_btn = tk.Button(self.settings,bg=BTN,text="Change Password",fg=TEXT,font=("calibri",10,"bold"),
            width=20,height=1)
        self.change_password_btn.pack(padx=40,pady=5)
        
        self.theme_btn = tk.Button(self.settings,bg=BTN,text="Change Theme",fg=TEXT,font=("calibri",10,"bold"),
            width=20,height=1,command=self.change_theme)
        self.theme_btn.pack(padx=40,pady=5)
        
        self.help_btn = tk.Button(self.settings,bg=BTN,text="Help",fg=TEXT,font=("calibri",10,"bold"),
            width=20,height=1)
        self.help_btn.pack(padx=40,pady=5)
        
        self.frames = {}
        self.frames["main"] = self.main
        self.frames["settings"] = self.settings

        self.show_frame("main")
        self.mainloop()

    def send_msg(self):
        self.msg = str(self.message_entry.get(1.0,tk.END))
        self.msg.strip()
        if len(self.msg) == 1:
            print("Type something!")
        else:
            send(self.msg)
        self.message_entry.delete(1.0,tk.END)

    def change_theme(self):
        with open(os.path.join(PATH,"current theme.txt"),"r") as file:
            current_theme = str(file.read())
            print(current_theme)
        with open(os.path.join(PATH,"current theme.txt"),"w") as file:
            if current_theme == "light":
                file.write("dark")
            else:
                file.write("light")
        with open(os.path.join(PATH,"current theme.txt"),"r") as file:
            LoginPage.exit_page(self)
            current_theme = str(file.read())
            print("The theme is now",current_theme)
            colours, background = theme(current_theme)
            BG = colours[0]
            TEXT = colours[1]
            BTN = colours[2]
            BOX = colours[3]
            MainPage()
    
    def write(self,msg):
        self.message_box.configure(state=tk.NORMAL)
        self.message_box.insert(tk.END,msg)
        self.message_box.insert(tk.END,"")
        self.message_box.configure(state=tk.DISABLED)

    def show_login(self):
        LoginPage.exit_page()
        LoginPage()

    def log_out(self):    
        self.exit_page()
        

    def exit_page(self):
        self.destroy()
        self.quit()

    def show_frame(self,page):
        frame = self.frames[page]
        frame.tkraise()

    def pick_up(self):
        time.sleep(1)
        self.write("")
        while True:
            try:
                time.sleep(1)
                self.msg_len = len(CLIENT.recv(HEADER).decode(FORMAT))
                self.msg = CLIENT.recv(self.msg_len).decode(FORMAT)
                self.priv_msg = re.search("\+from:.*",self.msg)
                if self.priv_msg:
                    self.message = self.msg[:self.priv_msg.span()[0]]
                    self.sender = self.msg[self.priv_msg.span()[0]+6:]
                    print(f"Message from {self.sender}: {self.message}")
                if self.msg:
                    if not self.priv_msg:
                        print(self.msg)
                        self.write(self.msg)
            except ConnectionResetError:
                self.write("[SERVER] The server has closed.")
                time.sleep(1)
                self.show_login()
                break

connect()
with open(os.path.join(PATH,"current theme.txt"),"r") as file:
    current_theme = str(file.read())
    colours, background = theme(current_theme)
    BG = colours[0]
    TEXT = colours[1]
    BTN = colours[2]
    BOX = colours[3]

gui = threading.Thread(target=LoginPage).start()




