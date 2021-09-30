### login.py ###

### LIBRARY YANG DIGUNAKAN ###
from tkinter import *
from tkinter import messagebox
#import db.db
import main
import json
import socket
import hashlib
from PIL import Image, ImageTk  # pip install pillow
import ssl

# Konfigurasi SSL
pemServer = 'server.pem'
keyClient = 'client.key'
pemClient = 'client.pem'

## Konfigurasi Socket
HOST = '192.168.100.8' #'localhost'  # The server's hostname or IP address
PORT = 3456        # The port used by the server

### Class Aplikasi Utama ###
class LoginWindow:

    def __init__(self):
        self.win = Tk()
        self.canvas = Canvas(self.win, width=600, height=500, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)
        ico = Image.open('images/logo4.png')
        photo = ImageTk.PhotoImage(ico)
        self.win.wm_iconphoto(False, photo)

        self.win.resizable(width=False, height=False)

        self.win.title("WELCOME | MANAGEMENT LOGIN | ADMINISTRATOR")

    # fungsi untuk membuat frame di dalam window #
    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        load = Image.open("images/logo1.png")
        resized_load = load.resize((round(load.size[0]*0.25), round(load.size[1]*0.25)))
        
        photo = ImageTk.PhotoImage(resized_load)
        self.background = Label(self.frame, image=photo)
        self.background.place(x=160,y=40)

        self.label = Label(self.frame, text="User Login")
        self.label.config(font=("Courier", 20, 'bold'))
        self.label.place(x=140, y = y + 150)

        self.emlabel = Label(self.frame, text="Enter Username")
        self.emlabel.config(font=("Courier", 12, 'bold'))
        self.emlabel.place(x=50, y= y + 230)

        self.email = Entry(self.frame, font='Courier 12')
        self.email.place(x=200, y= y + 230)

        self.pslabel = Label(self.frame, text="Enter Password")
        self.pslabel.config(font=("Courier", 12, 'bold'))
        self.pslabel.place(x=50, y=y+260)

        self.password = Entry(self.frame,show='*', font='Courier 12')
        self.password.place(x=200, y=y+260)

        self.button = Button(self.frame, text="Login", font='Courier 15 bold',
                             command=self.login, bg='#26a69a', fg='white')
        self.button.place(x=190, y=y+290)

        self.win.mainloop()
    
	# Fungsi untuk login ketika tombol ditekan #
    def login(self):
        email = self.email.get()
        password = self.password.get()
        
        if self.email.get() == "":
            messagebox.showinfo("Alert!","Enter Username First")
        elif self.password.get() == "":
            messagebox.showinfo("Alert!", "Enter Password first")
        else:
            h = hashlib.sha224(bytes(password,'utf-8'))
            send_obj = {
                'request': 'login',
                'username': email,
                'password': h.hexdigest()
            }
            jsonResult = json.dumps(send_obj)
			
			# Membuka log file #
            with open("request_response_history.txt", "a") as f:
                f.write(str(jsonResult) + "\n")
            b = bytes(jsonResult, 'utf-8')
			
			# Koneksi dengan server menggunakan socket SSL #
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                context.verify_mode = ssl.CERT_REQUIRED
                context.load_verify_locations(pemServer)
                context.load_cert_chain(certfile=pemClient, keyfile=keyClient)
                if ssl.HAS_SNI:
                    secure_sock = context.wrap_socket(s, server_side=False, server_hostname=HOST)
                else:
                    secure_sock = context.wrap_socket(s, server_side=False)

                cert = secure_sock.getpeercert()

                if not cert: raise Exception("ERROR")

                secure_sock.send(b)
                response = secure_sock.recv(4096)
                secure_sock.close()
                s.close()
				
			# Membuka log file #
            with open("request_response_history.txt", "a") as f:
                f.write(str(response.decode("utf-8")) + "\n")
            py_obj = json.loads(response.decode("utf-8"))
            if py_obj['status'] == 'berhasil' :
                messagebox.showinfo("Message", "Login Successfully")
                self.win.destroy()
                x = main.restaurantApp()
            else:
                messagebox.showinfo("Alert!", "Wrong username/password")