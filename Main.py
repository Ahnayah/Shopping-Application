from tkinter import *
from tkinter import PhotoImage
from tkinter.messagebox import showinfo, showerror, showwarning
from database import DatabaseHandler

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
        
        self.database_handler = DatabaseHandler()
        self.window.mainloop()

    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == '' or password == '' and username == ' ' or password == ' ':
            showerror("Error", "Please enter a valid username and password")
        elif password == '':
            showerror("Error", "Please enter a valid password") 
        elif username == '':
            showerror("Error", "Please enter a valid username")
        else:
            self.database_handler.add_user(username, password)
            self.window.destroy()
            ShoppingWindow(username)
            
class ShoppingWindow():
    def __init__(self, username):
        self.window = Tk()
        self.window.geometry("1280x960")
        self.window.title("Glow Getter")
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1280
        window_height = 960
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.window.resizable(False, False)
        
        self.shop_background = PhotoImage(file="assets/shop_background.png")
        self.background_label1 = Label(self.window, image=self.shop_background)
        self.background_label1.pack()
        
        message_butt = PhotoImage(file="assets/message.png")
        self.message_button = Button(self.window, image=message_butt, border=0)
        self.message_button.config(bg='#939974', border=0, activebackground='#939974', cursor="hand2", command=self.send_message)
        self.message_button.place(x=1150, y=42)
        
        self.greeting = Label(self.window, text=f"Welcome, {username}")
        self.greeting.place(x=140, y=30, width=1001, height=100)
        self.greeting.config(font=("Arial",35, "bold"), bg='#939974', fg='white')             
        
        self.database_handler = DatabaseHandler() 
        
        self.selected_item_entry = Text(self.window, width=20, state='disabled')
        self.selected_item_entry.place(x=2, y=234)
        self.selected_item_entry.config(font=("Arial", 12), height=35)
        
        self.load_products()
        self.window.mainloop()
    
    def send_message(self):
        ChatWindow()
        
    def load_products(self):
        products = self.database_handler.get_products()
        x_position = 320
        y_position = 260
        for product in products:
            product_id, name, price, image_path = product
            product_image = PhotoImage(file=image_path)
            
            product_label = Label(self.window, image=product_image)
            product_label.image = product_image
            product_label.config(width=100, height=100)
            product_label.place(x=x_position, y=y_position)
            
            product_name_label = Label(self.window, text=name, font=("Arial", 12, "bold"), bg='#939974', fg='white')
            product_name_label.place(x=x_position, y=y_position + 105)
            
            product_price_label = Label(self.window, text=f"${price:.2f}", font=("Arial", 12), bg='#939974', fg='white')
            product_price_label.place(x=x_position, y=y_position + 130)
            
            quanity_label = Label(self.window, text=f"Quantity: ", font=("Arial", 12), bg='#939974', fg='white')
            quanity_label.place(x=x_position, y=y_position + 150)
            
            quantity_spinbox = Spinbox(self.window, from_=1, to=50, width=6)
            quantity_spinbox.place(x=x_position, y=y_position + 170)
            
            select_button = Button(self.window, text="Select", bg='white', fg='black', command=lambda product_id=product_id, name=name, price=price, quantity_spinbox=quantity_spinbox: self.select_product(product_id, name, price, quantity_spinbox))
            select_button.place(x=x_position, y=y_position + 200)
            
            x_position += 320
            if x_position > 1000:
                x_position = 320
                y_position += 260
                
    def select_product(self, product_id, name, price, quantity_spinbox):
        try:
            quantity = int(quantity_spinbox.get())
            if quantity > 50:
                showerror("Error", "Please enter a valid quantity")
                return
            self.add_to_cart(product_id, name, price, quantity)
        except ValueError:
            showerror("Error", "Please enter a valid quantity")
            
    def add_to_cart(self, product_id, name, price, quantity):
        user_id = self.database_handler.get_user_id(self.username)
        self.database_handler.add_to_cart(user_id, product_id, name, price, quantity)
        self.update_selected_item_entry()
        
    def update_selected_item_entry(self):
        user_id = self.database_handler.get_user_id(self.username)
        cart_items = self.database_handler.get_cart_items(user_id)
        self.selected_item_entry.config(state='normal')
        self.selected_item_entry.delete("1.0", END)
        for item in cart_items:
            name, price, quantity = item
            item_details = f"Name: {name}\nPrice: ${price:.2f}\nQuantity: {quantity}\n\n"
            self.selected_item_entry.insert(END, item_details)
        self.selected_item_entry.config(state='disabled')
        
class ChatWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("600x400")
        self.window.title("Glow Getter : Message Staff")
        self.window.resizable(False, False)
        self.window.config(bg="#939974")
        
        self.send_button = Button(self.window, text="Send", bg='white', fg='black')
        self.send_button.place(x=500, y=300)
        
        self.chat_box = Text(self.window)
        self.chat_box.pack()
        self.chat_box.config(font=("Arial", 12), width=50, height=10)
        self.chat_box.place(x=73, y=100)
        message = self.chat_box.get("1.0", "end-1c")
        self.chat_box.insert(END, f'{message}')
        
        self.sender_box = Entry(self.window)
        self.sender_box.pack()
        self.sender_box.config(font=("Arial", 12), width=50, state='readonly')
        self.sender_box.place(x=73, y=70)

if __name__ == "__main__":
    ShoppingWindow("Test")