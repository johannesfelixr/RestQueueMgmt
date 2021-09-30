### main.py ###

### LIBRARY YANG DIGUNAKAN ###
from tkcalendar import Calendar, DateEntry
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import socket
import json
import datetime
from PIL import Image, ImageTk
import ssl

## Konfigurasi Socket
HOST =  '192.168.100.8'
PORT = 3456

# Konfigurasi SSL
pemServer = 'server.pem'
keyClient = 'client.key'
pemClient = 'client.pem'

### Class Aplikasi Utama ###
class restaurantApp(tk.Tk):
    def __init__(self):

        # Pembuatan Penampilan Layar Utama #
        super().__init__()
        self.title("DAN RESTAURANT | ORDER MANAGEMENT | ADMINISTRATOR")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int(width / 2 - 800 / 2)
        y = int(height / 2 - 650 / 2 -50)
        str1 = "800x650+" + str(x) + "+" + str(y)
        self.geometry(str1)
        ico = Image.open('images/logo4.png')
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)
		
        self.lblTitle = tk.Label(self, text="Order Management System", font=("Helvetica", 16), fg="black")
        self.lblPaket = tk.Label(self, text="Paket:", font=("Helvetica", 10), fg="black")
        self.lblQuan = tk.Label(self, text="Quantity:", font=("Helvetica", 10), fg="black")
        self.lblStatus = tk.Label(self, text="Order Status:", font=("Helvetica", 10), fg="black")
        self.lblDOO = tk.Label(self, text="Date of Order:", font=("Helvetica", 10), fg="black")
        self.lblUser = tk.Label(self, text="User:", font=("Helvetica", 10), fg="black")
        self.lblNotes = tk.Label(self, text="Notes:", font=("Helvetica", 10), fg="black")
        self.lblSelect = tk.Label(self, text="Please select one record below to update or delete", font=("Helvetica", 10), fg="black")
        self.lblSearchDate = tk.Label(self, text="Please Enter Date of Order:",font=("Helvetica", 10), fg="black")
        self.lblSearch = tk.Label(self, text="Please Enter Order No:",font=("Helvetica", 10), fg="black")

        self.entPaket1 = tk.Entry(self)
        self.entPaket2 = tk.Entry(self)
        self.entPaket3 = tk.Entry(self)
        self.entQuan1 = tk.Entry(self)
        self.entQuan2 = tk.Entry(self)
        self.entQuan3 = tk.Entry(self)
        n3 = tk.StringVar()
        self.entStatus = ttk.Combobox(self, textvariable = n3)
        self.entStatus['values'] = ('paid',
                                    'ready',
                                    'selesai')
        self.calDOO = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2021,locale='en_US', date_pattern='y-mm-dd')
        self.entUser = tk.Entry(self)
        self.entNotes = tk.Entry(self)
        self.searchDOO = DateEntry(self, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2021,locale='en_US', date_pattern='y-mm-dd')
        self.entSearch = tk.Entry(self)


        self.btn_topup = tk.Button(self, text="Top-Up", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                   command =self.openNewWindow)
        self.btn_update = tk.Button(self,text="Update",font=("Helvetica",11),bg='#26a69a', fg='white',command=self.update_order_data)
        self.btn_delete = tk.Button(self, text="Delete", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                    command=self.delete_order_data)
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                    command=self.clear_form)
        self.btn_show_all = tk.Button(self, text="Show All", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                   command=self.load_order_data)
        self.btn_search_date = tk.Button(self, text="Search", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                   command=self.show_search_date_record)
        self.btn_search = tk.Button(self, text="Search", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                   command=self.show_search_record)
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 16), bg='#26a69a', fg='white',command=self.exit)

        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8")
        self.tvorder= ttk.Treeview(self,show="headings",height="5", columns=columns)
        self.tvorder.heading('#1', text='orderno', anchor='center')
        self.tvorder.column('#1', width=60, anchor='center', stretch=False)
        self.tvorder.heading('#2', text='Paket', anchor='center')
        self.tvorder.column('#2', width=10, anchor='center', stretch=True)
        self.tvorder.heading('#3', text='Quantity', anchor='center')
        self.tvorder.column('#3',width=10, anchor='center', stretch=True)
        self.tvorder.heading('#4', text='Status', anchor='center')
        self.tvorder.column('#4', width=10, anchor='center', stretch=True)
        self.tvorder.heading('#5', text='Date of Order', anchor='center')
        self.tvorder.column('#5', width=10, anchor='center', stretch=True)
        self.tvorder.heading('#6', text='Harga', anchor='center')
        self.tvorder.column('#6',width=10, anchor='center', stretch=True)
        self.tvorder.heading('#7', text='user', anchor='center')
        self.tvorder.column('#7',width=10, anchor='center', stretch=True)
        self.tvorder.heading('#8', text='notes', anchor='center')
        self.tvorder.column('#8',width=10, anchor='center', stretch=True)

        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvorder.yview)
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)
        self.tvorder.configure(yscroll=vsb.set)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvorder.xview)
        hsb.place(x=40 , y=310+200+1, width=620 + 20)
        self.tvorder.configure(xscroll=hsb.set)
        self.tvorder.bind("<<TreeviewSelect>>", self.show_selected_record)

        self.lblTitle.place(x=200, y=30,  height=27, width=300)
        self.lblPaket.place(x=175, y=70,  height=23, width=100)
        self.lblQuan.place(x=175, y=100,  height=23, width=100)
        self.lblStatus.place(x=171, y=129,  height=23, width=104)
        self.lblDOO.place(x=175, y=158,  height=23, width=104)
        self.lblUser.place(x=175, y=187,  height=23, width=100)
        self.lblNotes.place(x=163, y=217, height=23, width=128)
        self.lblSelect.place(x=150, y=280, height=23, width=400)
        self.lblSearchDate.place(x=147, y=535, height=23, width=160)
        self.lblSearch.place(x=174, y=560, height=23, width=134)

        self.entPaket1.place(x=277, y=72, height=21, width=60)
        self.entPaket2.place(x=339, y=72, height=21, width=60)
        self.entPaket3.place(x=401, y=72, height=21, width=60)
        self.entQuan1.place(x=277, y=100, height=21, width=60)
        self.entQuan2.place(x=339, y=100, height=21, width=60)
        self.entQuan3.place(x=401, y=100, height=21, width=60)
        self.entStatus.place(x=277, y=129, height=21, width=186)
        self.calDOO.place(x=277, y=158, height=21, width=186)
        self.entUser.place(x=278, y=188, height=21, width=186)
        self.entNotes.place(x=278, y=218, height=21, width=186)
        self.searchDOO.place(x=310, y=535, height=21, width=186)
        self.entSearch.place(x=310, y=560, height=21, width=186)
        
        self.btn_topup.place(x=548, y=72, height=25, width=76)
        self.btn_update.place(x=290, y=245, height=25, width=76)
        self.btn_delete.place(x=370, y=245, height=25, width=76)
        self.btn_clear.place(x=460, y=245, height=25, width=76)
        self.btn_show_all.place(x=548, y=245, height=25, width=76)
        self.btn_search_date.place(x=498, y=532, height=26, width=60)
        self.btn_search.place(x=498, y=558, height=26, width=60)
        self.btn_exit.place(x=320, y=610,  height=31, width=60)
        self.tvorder.place(x=40, y=310, height=200, width=640)

        self.load_order_data()

        self.refresh()
        
        self.mainloop()
	
    # Pembuatan Tampilan Layar Top Up #
    def openNewWindow(self):
        self.newWindow = tk.Toplevel(self)
        self.newWindow.title("Top-Up Window")
  
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int(width / 2 - 500 / 2)
        y = int(height / 2 - 300 / 2 -50)
        str1 = "500x300+" + str(x) + "+" + str(y)
        self.newWindow.geometry(str1)
        ico = Image.open('images/logo4.png')
        photo = ImageTk.PhotoImage(ico)
        self.newWindow.wm_iconphoto(False, photo)
  
        self.lblTopUpTitle = tk.Label(self.newWindow, text="Top-Up User Balance", font=("Helvetica", 16), fg="black")
        self.lblSearchUser = tk.Label(self.newWindow, text="Please Enter User:",font=("Helvetica", 10), fg="black")
        self.lblTopUpUser = tk.Label(self.newWindow, text="User:", font=("Helvetica", 10), fg="black")
        self.lblBalance = tk.Label(self.newWindow, text="Balance:", font=("Helvetica", 10), fg="black")
        self.lblTopUp = tk.Label(self.newWindow, text="TopUp:", font=("Helvetica", 10), fg="black")
        
        self.entSearchUser = tk.Entry(self.newWindow)
        self.entTopUpUser = tk.Entry(self.newWindow)
        self.entBalance = tk.Entry(self.newWindow)
        self.entTopUp = tk.Entry(self.newWindow)
		
        self.btn_searchUser = tk.Button(self.newWindow, text="Search", font=("Helvetica", 11), bg='#26a69a', fg='white',
                                   command=self.show_search_username)
        self.btn_topup = tk.Button(self.newWindow,text="TopUp",font=("Helvetica",11),bg='#26a69a', fg='white',
                                   command=self.update_user_balance)
        self.btn_clear_topup = tk.Button(self.newWindow,text="Clear",font=("Helvetica",11),bg='#26a69a', fg='white',
                                   command=self.clear_topup)
        
        self.lblTopUpTitle.place(x=30, y=30,  height=27, width=400)
        self.lblSearchUser.place(x=50, y=70,  height=23, width=200)
        self.lblTopUpUser.place(x=100, y=100,  height=23, width=100)
        self.lblBalance.place(x=100, y=129,  height=23, width=100)
        self.lblTopUp.place(x=100, y=155,  height=23, width=100)
		
        self.entSearchUser.place(x=250, y=72, height=21, width=186)
        self.entTopUpUser.place(x=250, y=100, height=21, width=186)
        self.entBalance.place(x=250, y=129, height=21, width=186)
        self.entTopUp.place(x=250, y=155, height=21, width=186)
        
        self.btn_searchUser.place(x=100, y=201, height=31, width=60)
        self.btn_topup.place(x=180, y=201,  height=31, width=100)
        self.btn_clear_topup.place(x=300, y=201,  height=31, width=60)
    
    # Fungsi Update User Balance #  
    def update_user_balance(self):
        User = self.entTopUpUser.get()
        TopUp = self.entTopUp.get()
        if User == "":
            mb.showinfo('Information', "Please Enter User Name", parent=self.newWindow)
            self.entTopUpUser.focus_set()
            return
        if TopUp == "":
            mb.showinfo('Information', "Please Enter TopUp Amount", parent=self.newWindow)
            self.entTopUp.focus_set()
            return
        send_obj = {
            'request': 'topup',
            'username': User,
            'topup': TopUp
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
            mb.showinfo("Info", "Selected User Balance Updated Successfully", parent=self.newWindow)
            self.entSearchUser.delete(0, tk.END)
            self.entSearchUser.insert(0, User)
            self.show_search_username()
        else:
            mb.showinfo('Information', "Balance update failed!!!", parent=self.newWindow)
        
    # Fungsi melakukan pencarian informasi user balance berdasarkan username #
    def show_search_username(self):
        username_entry = self.entSearchUser.get()
        if username_entry == "":
            mb.showinfo('Information', "Please Enter Username",parent=self.newWindow)
            self.entSearchUser.focus_set()
            return
        self.entTopUpUser.delete(0, tk.END)
        self.entBalance.delete(0, tk.END)
        self.entTopUp.delete(0, tk.END)
        send_obj = {
            'request': 'search',
            'tipe': 'username',
            'username': username_entry
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
            
            self.entTopUpUser.insert(0, username_entry)
            self.entBalance.insert(0, py_obj['isi'])
        else:
            mb.showinfo('Information', "Username Not Found!!!", parent=self.newWindow)

    # Fungsi Untuk Command Clear pada Layar TopUp #
    def clear_topup(self):
      self.entTopUpUser.delete(0, tk.END)
      self.entBalance.delete(0, tk.END)
      self.entSearchUser.delete(0, tk.END)
      self.entTopUp.delete(0, tk.END)

    # Fungsi Untuk Command clear pada layar utama #
    def clear_form(self):
      self.entPaket1.delete(0, tk.END)
      self.entPaket2.delete(0, tk.END)
      self.entPaket3.delete(0, tk.END)
      self.entQuan1.delete(0, tk.END)
      self.entQuan2.delete(0, tk.END)
      self.entQuan3.delete(0, tk.END)
      self.entUser.delete(0, tk.END)
      self.entNotes.delete(0, tk.END)
      self.entStatus.delete(0, tk.END)
      self.calDOO.delete(0, tk.END)

    # Fungsi untuk button exit pada layar utama #
    def exit(self):
      MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
      if MsgBox == 'yes':
        self.destroy()

    # FUngsi untuk mengirimkan request delete suatu pesanan #
    def delete_order_data(self):
        MsgBox = mb.askquestion('Delete Record', 'Are you sure! you want to delete selected ordertable record', icon='warning')
        if MsgBox == 'yes':
            send_obj = {
                'request': 'delete',
                'orderno': order_no 
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
              mb.showinfo("Information", "Order Record Deleted Successfully")
              self.load_order_data()
              self.entPaket1.delete(0, tk.END)
              self.entPaket2.delete(0, tk.END)
              self.entPaket3.delete(0, tk.END)
              self.entQuan1.delete(0, tk.END)
              self.entQuan2.delete(0, tk.END)
              self.entQuan3.delete(0, tk.END)
              self.entUser .delete(0, tk.END)
              self.entNotes.delete(0, tk.END)
              self.entStatus.delete(0, tk.END)
              self.calDOO.delete(0, tk.END)
            else:
              messagebox.showinfo("Alert!", "Cannot Delete Record")

    # Fungsi untuk melakukan pencarian pesanan berdasarkan nomor order #
    def show_search_record(self):
        o_order_no = self.entSearch.get()  # Retrieving entered orderno
        print(o_order_no)
        if  o_order_no == "":
            mb.showinfo('Information', "Please Enter Order No")
            self.entSearch.focus_set()
            return
        self.tvorder.delete(*self.tvorder.get_children())
        send_obj = {
            'request': 'search',
            'tipe': 'orderno',
            'orderno': o_order_no 
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
        rows = py_obj['isi']

        orderno = ""
        Paket = ""
        Quantity = ""
        User = ""
        Status = ""
        Notes = ""
        DOO =""
        Harga =""
        for row in reversed(rows):
            orderno = row[0]
            Paket = row[1]
            Quantity = row[2]
            Status = row[3]
            DOO = row[4]
            Harga = row[5]
            User = row[6]
            Notes = row[7]
            self.tvorder.insert("", 'end', text=orderno, values=(orderno, Paket, Quantity, Status, DOO, Harga, User, Notes))

    # Fungsi untuk melakukan pencarian pesanan berdasarkan tanggal pemesanan #
    def show_search_date_record(self):
        date_of_order = self.searchDOO.get()  # Retrieving entered DOO
        print(date_of_order)
        if  date_of_order == "":
            mb.showinfo('Information', "Please Enter Date of Order")
            self.entSearchDate.focus_set()
            return
        self.tvorder.delete(*self.tvorder.get_children())  # clears the treeview tvorder
        send_obj = {
            'request': 'search',
            'tipe': 'tanggal',
            'tanggal': date_of_order 
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
        rows = py_obj['isi']

        orderno = ""
        Paket = ""
        Quantity = ""
        User = ""
        Status = ""
        Notes = ""
        DOO =""
        Harga =""
        for row in reversed(rows):
            orderno = row[0]
            Paket = row[1]
            Quantity = row[2]
            Status = row[3]
            DOO = row[4]
            Harga = row[5]
            User = row[6]
            Notes = row[7]
            # print( User)
            self.tvorder.insert("", 'end', text=orderno, values=(orderno, Paket, Quantity, Status, DOO, Harga, User, Notes))

    # Fungsi untuk menampilkan atribut dari pesanan yang diselect #
    def show_selected_record(self, event):
        self.clear_form()
        for selection in self.tvorder.selection():
            item = self.tvorder.item(selection)
        global order_no
        order_no,paket,quantity,Status,doo = item["values"][0:5]
        User,Notes = item["values"][6:8]
        paket = paket.split(';')
        if len(paket) == 1:
            self.entPaket1.insert(0, paket[0])
        elif len(paket) == 2:
            self.entPaket1.insert(0, paket[0])
            self.entPaket2.insert(0, paket[1])
        elif len(paket) == 3:
            self.entPaket1.insert(0, paket[0])
            self.entPaket2.insert(0, paket[1])
            self.entPaket3.insert(0, paket[2])
        quantity = str(quantity).split(';')
        if len(quantity) == 1:
            self.entQuan1.insert(0, quantity[0])
        elif len(quantity) == 2:
            self.entQuan1.insert(0, quantity[0])
            self.entQuan2.insert(0, quantity[1])
        elif len(quantity) == 3:
            self.entQuan1.insert(0, quantity[0])
            self.entQuan2.insert(0, quantity[1])
            self.entQuan3.insert(0, quantity[2])
        self.entUser.insert(0, User)
        self.entNotes.insert(0, Notes)
        self.entStatus .insert(0, Status)
        self.calDOO.insert(0, doo)
        return order_no
	
	# Fungsi untuk mengirimkan request update atribut dari suatu pesanan #
    def update_order_data(self):
        print("Updating")
        Paket1 = self.entPaket1.get()
        Paket2 = self.entPaket2.get()  
        Paket3 = self.entPaket3.get()  
        Quan1 = self.entQuan1.get()  
        Quan2 = self.entQuan2.get()  
        Quan3 = self.entQuan3.get()  
        User = self.entUser.get()
        Notes = self.entNotes.get()
        Status = self.entStatus.get()
        DOO = self.calDOO.get()
        print(order_no)
        Harga = 0
        if Paket1 =="A":
            Harga = Harga + int(Quan1)*39000 #harga 1
        elif Paket1 =="B":
            Harga = Harga + int(Quan1)*46000 #harga 2
        elif Paket1 =="C":
            Harga = Harga + int(Quan1)*42000 #harga 3
        if Paket2 !="":
            if Paket2 =="A":
                Harga = Harga + int(Quan2)*39000 #harga 2
            elif Paket2 =="B":
                Harga = Harga + int(Quan2)*46000 #harga 3
            elif Paket2 =="C":
                Harga = Harga + int(Quan2)*42000 #harga 3
        if Paket3 !="":
            if Paket3 =="A":
                Harga = Harga + int(Quan3)*39000 #harga 2
            elif Paket3 =="B":
                Harga = Harga + int(Quan3)*46000 #harga 3
            elif Paket3 =="C":
                Harga = Harga + int(Quan3)*42000 #harga 3 
        if Paket3 !="":        
            Paket = Paket1 + ';' + Paket2 + ';' + Paket3
            Quantity = Quan1 + ';' + Quan2 + ';' + Quan3
        elif Paket2 !="":        
            Paket = Paket1 + ';' + Paket2
            Quantity = Quan1 + ';' + Quan2
        else:        
            Paket = Paket1
            Quantity = Quan1
        send_obj = {
            'request': 'update',
            'orderno': order_no,
            'paket': Paket,
            'quantity': Quantity,
            'status': Status,
            'doo': DOO,
            'username': User,
            'notes': Notes,
			'totalHarga': Harga 
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
            mb.showinfo("Info", "Selected Order Record Updated Successfully ")
            self.load_order_data()
        elif py_obj['status'] == 'saldo kurang' :
            mb.showinfo("Info", "Saldo User Kurang ")
            self.load_order_data()
        else:
            mb.showinfo('Information', "Data update failed!!!")

    # Fungsi untuk merequest daftar semua pesanan yang ada #
    def load_order_data(self):
        self.tvorder.delete(*self.tvorder.get_children())  # clears the treeview tvorder
        send_obj = {
            'request': 'search',
            'tipe': 'all'
        }
        jsonResult = json.dumps(send_obj)
		
		# Membuka log file #
        with open("request_response_history.txt", "a") as f:
            f.write(str(jsonResult) + "\n")
        b = bytes(jsonResult, 'utf-8')
		
        # Koneksi dengan server menggunakan socket SSL #
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            #print('loading')
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

        rows = py_obj['isi']

        orderno = ""
        Paket = ""
        Quantity = ""
        Notes = ""
        Status = ""
        User = ""
        DOO =""
        Harga =""
        for row in reversed(rows):
            orderno = row[0]
            Paket = row[1]
            Quantity = row[2]
            User = row[6]
            Notes = row[7]
            Status = row[3]
            DOO = row[4]
            Harga = row[5]
            self.tvorder.insert("", 'end', text=orderno, values=(orderno, Paket, Quantity,Status,DOO,Harga, User, Notes))
        #print('load complete')

    # Fungsi untuk memanggil load_order_data setiap 10 detik agar data pesanan selalu uptodate #
    def refresh(self):
        print('refresh')
        try:
            self.load_order_data()
            #print('lalala')
        finally:
            self.after(10000, self.refresh) # run itself again after 1000 ms

### MAIN PROGRAM ###
if __name__ == "__main__":
    print('now running')
    app = restaurantApp()
    app.mainloop()