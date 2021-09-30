### restaurant_client.py ###

### LIBRARY YANG DIGUNAKAN ###
from tkinter import *
import login
from PIL import Image, ImageTk  # pip install pillow

### Class Aplikasi Utama ###
class WelcomeWindow:

    def __init__(self):
        self.win = Tk()

        self.canvas = Canvas(self.win, width=600, height=400, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 400 / 2)
        str1 = "600x400+"+ str(x) + "+" + str(y)
        self.win.geometry(str1)
        ico = Image.open('images/logo4.png')
        photo = ImageTk.PhotoImage(ico)
        self.win.wm_iconphoto(False, photo)

        self.win.resizable(width=False, height=False)

        self.win.title("WELCOME | DAN RESTAURANT | ADMINISTRATOR")

    # fungsi untuk membuat frame di dalam window #
    def add_frame(self):
        self.frame = Frame(self.win, height=300, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20

        load = Image.open("images/logo1.png")
        resized_load = load.resize((round(load.size[0]*0.25), round(load.size[1]*0.25)))
        
        
        photo = ImageTk.PhotoImage(resized_load)
        self.background = Label(self.frame, image=photo)
        self.background.place(x=160,y=40)

        self.labeltitle = Label(self.frame, text="Welcome to Dan Restaurant")
        self.labeltitle.config(font=("Courier", 16, 'bold'))
        self.labeltitle.place(x=50, y=y+150)

        self.button = Button(self.frame, text="Continue", font=('helvetica', 20, 'underline italic')
                             , bg='#26a69a', fg='white', command=self.login)
        self.button.place(x=x+90, y=y+200)

        self.win.mainloop()

    # Fungsi untuk membuka window baru ketika tombol ditekan #
    def login(self):
        self.win.destroy()

        log = login.LoginWindow()
        log.add_frame()

### MAIN PROGRAM ###
if __name__ == "__main__":
    x = WelcomeWindow()
    x.add_frame()