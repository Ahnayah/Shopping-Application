from tkinter import *
from tkinter.messagebox import showinfo, showerror, showwarning
from tkinter import simpledialog
from database import DatabaseHandler
import os

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
            
class ShoppingWindow:
    def __init__(self, username):
        self.username = username
        self.db_handler = DatabaseHandler()
        self.cart = []  
        self.total_price = 0.0 
        self.product_widgets = []  
        
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
        
        self.selected_item_entry = Text(self.window, width=20, height=38, state='disabled', bg='#f7f7f7')
        self.selected_item_entry.place(x=60, y=200)
        self.selected_item_entry.config(font=("Arial", 12))
        
        self.total_price_label = Label(self.window, text="Total Price: $0.00", font=("Arial", 12, "bold"), bg='#939974', fg='white')
        self.total_price_label.place(x=110, y=900)  
        
        self.order_button = Button(self.window, text="Order", bg='white', fg='black', font=("Arial", 16), command=self.place_order)
        self.order_button.place(x=30, y=890)
        
        self.load_products()
        self.window.mainloop()
    
    def send_message(self):
        ChatWindow(self.username)
        
    def load_products(self):
        self.clear_product_widgets()  
        products = self.database_handler.get_products()
        x_position = 320
        y_position = 250
        for product in products:
            product_id, name, price, quantity, image_path, rating = product  
            
            print(f"Loading product: {name}, Image path: {image_path}")
            
            if not os.path.exists(image_path):
                showerror("Error", f"Image file not found: {image_path}")
                continue
            
            try:
                product_image = PhotoImage(file=image_path)
            except Exception as e:
                showerror("Error", f"Failed to load image: {image_path}\n{e}")
                continue
            
            product_label = Label(self.window, image=product_image)
            product_label.image = product_image
            product_label.config(width=110, height=110)
            product_label.place(x=x_position, y=y_position)
            self.product_widgets.append(product_label)
            
            product_name_label = Label(self.window, text=name, font=("Arial", 16, "bold"), bg='#939974', fg='white')
            product_name_label.place(x=x_position, y=y_position + 130)
            self.product_widgets.append(product_name_label)
            
            product_price_label = Label(self.window, text=f"${price:.2f}", font=("Arial", 16), bg='#939974', fg='white')
            product_price_label.place(x=x_position, y=y_position + 166)
            self.product_widgets.append(product_price_label)
            
            quantity_label = Label(self.window, text="Quantity:", font=("Arial", 16), bg='#939974', fg='white')
            quantity_label.place(x=x_position, y=y_position + 200)
            self.product_widgets.append(quantity_label)
            
            quantity_spinbox = Spinbox(self.window, from_=1, to=50, width=5, font=("Arial", 16))
            quantity_spinbox.place(x=x_position + 105, y=y_position + 200)
            self.product_widgets.append(quantity_spinbox)
            
            select_button = Button(self.window, text="Add to Cart", bg='white', fg='black', font=("Arial", 16), command=lambda p_id=product_id, p_name=name, p_price=price, q=quantity_spinbox: self.select_product(p_id, p_name, p_price, q))
            select_button.place(x=x_position, y=y_position + 235)
            self.product_widgets.append(select_button)
            
            rating_label = Label(self.window, text=f"Rating: {rating:.1f}", font=("Arial", 16), bg='#939974', fg='white')
            rating_label.place(x=x_position, y=y_position + 280)
            self.product_widgets.append(rating_label)
            
            rate_button = Button(self.window, text="Rate", bg='white', fg='black', font=("Arial", 16), command=lambda p_id=product_id: self.rate_product(p_id))
            rate_button.place(x=x_position + 115, y=y_position + 290)
            self.product_widgets.append(rate_button)
            
            x_position += 200  
            if x_position > 1000:
                x_position = 320  
                y_position += 350  

    def clear_product_widgets(self):
        for widget in self.product_widgets:
            widget.destroy()
        self.product_widgets.clear()

    def select_product(self, product_id, name, price, quantity_spinbox):
        try:
            quantity = int(quantity_spinbox.get())
            if quantity > 50:
                showerror("Error", "Quantity cannot exceed 50")
                return
            self.add_to_cart(product_id, name, price, quantity)
        except ValueError:
            showerror("Error", "Please enter a valid quantity")
            
    def add_to_cart(self, product_id, name, price, quantity):
        user_id = self.database_handler.get_user_id(self.username)
        if user_id is None:
            showerror("Error", "User not found")
            return
        self.database_handler.add_to_cart(user_id, product_id, name, price, quantity)
        self.update_selected_item_entry()
        self.update_total_price(price, quantity)
        
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
    
    def update_total_price(self, price, quantity):
        self.total_price += price * quantity
        self.total_price_label.config(text=f"Total Price: ${self.total_price:.2f}")
    
    def place_order(self):
        user_id = self.database_handler.get_user_id(self.username)
        if user_id is None:
            showerror("Error", "User not found")
            return
        cart_items = self.database_handler.get_cart_items(user_id)
        if not cart_items:
            showerror("Error", "Your cart is empty")
            return
        self.database_handler.clear_cart(user_id)
        self.selected_item_entry.config(state='normal')
        self.selected_item_entry.delete("1.0", END)
        self.selected_item_entry.config(state='disabled')
        self.total_price = 0.0
        self.total_price_label.config(text="Total Price: $0.00")
        showinfo("Order Placed", "Your order has been placed successfully")
    
    def rate_product(self, product_id):
        rating = simpledialog.askfloat("Rate Product", "Enter your rating (0-5):", minvalue=0, maxvalue=5)
        if rating is not None:
            self.database_handler.update_product_rating(product_id, rating)
            self.load_products()  
        
class ChatWindow:
    def __init__(self, username):
        self.username = username
        self.db_handler = DatabaseHandler()
        self.window = Tk()
        self.window.geometry("600x400")
        self.window.title("Glow Getter : Message Staff")
        self.window.resizable(False, False)
        self.window.config(bg="#939974")
        
        self.send_button = Button(self.window, text="Send", bg='white', fg='black', command=self.send_message)
        self.send_button.place(x=500, y=300)
        
        self.chat_box = Text(self.window)
        self.chat_box.pack()
        self.chat_box.config(font=("Arial", 12), width=50, height=10)
        self.chat_box.place(x=73, y=100)
        
        self.sender_box = Entry(self.window)
        self.sender_box.pack()
        self.sender_box.config(font=("Arial", 12), width=50, state='readonly')
        self.sender_box.place(x=73, y=70)
        self.sender_box.insert(0, f'{username}')
        
        self.window.mainloop() 

    def send_message(self):
        message = self.chat_box.get("1.0", "end-1c")
        if message.strip():
            user_id = self.db_handler.get_user_id(self.username)
            self.db_handler.insert_message(user_id, message)
            showinfo("Message Sent", "Your message has been sent and stored in the database.")
            self.chat_box.delete("1.0", END)
        else:
            showwarning("Empty Message", "Cannot send an empty message.")

if __name__ == "__main__":
    MainMenu()