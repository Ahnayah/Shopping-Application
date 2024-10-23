from tkinter import *
from tkinter import PhotoImage

class MainMenu:
    
    def login():
        username = username.get()
        password = password.get()
    window = Tk()
    window.geometry("1024x768")
    window.title("Glow Getter")

    background = PhotoImage(file="assets/background.png")
    button_image = PhotoImage(file="assets/login.png")
    
    background_label = Label(window, image=background)
    background_label.pack()

    username = Entry(window, width=30)
    username.place(x=389, y=352)
    username.config(font=("Arial"))
    
    password = Entry(window, width=30, bg="white", show="*")
    password.place(x=389, y=437)
    password.config(font=("Arial"), fg="black")
    
    login_button = Button(window, border=0, image=button_image, command=login)
    login_button.place(x=420, y=512)
    login_button.config(font=("Arial"), bg="white", )
    
    window.mainloop()