from tkinter import *
from tkinter import PhotoImage
from tkinter.messagebox import showinfo, showerror, showwarning

class MainMenu:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1024x768")
        self.window.title("Glow Getter")
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1024
        window_height = 768
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        
        self.window.resizable(False, False)
        
        self.background = PhotoImage(file="assets/background.png")
        self.button_image = PhotoImage(file="assets/login.png")
        self.button1_image = PhotoImage(file="assets/register.png")
        
        self.background_label = Label(self.window, image=self.background)
        self.background_label.pack()
        
        self.username_entry = Entry(self.window, width=30)
        self.username_entry.place(x=389, y=352)
        self.username_entry.config(font=("Arial"))
        
        self.password_entry = Entry(self.window, width=30, show="*")
        self.password_entry.place(x=389, y=437)
        self.password_entry.config(font=("Arial"))
        
        self.login_button = Button(self.window, image=self.button_image, command=self.login, border=0)
        self.login_button.place(x=440, y=512)
        
        
        self.window.mainloop()
    
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == '' or password == '':
            showerror("Error", "Please enter a valid username and password")
        else:
            print("Login successful")
            
    def shopping_window(self):
        pass

# Create an instance of MainMenu to run the application
if __name__ == "__main__":
    MainMenu()