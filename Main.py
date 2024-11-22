from tkinter import *
from tkinter.messagebox import showinfo, showerror, showwarning
from tkinter import simpledialog
from database import DatabaseHandler
import os

class MainMenu:
    def __init__(self):
        self.window = Tk()
        self.window.title("Glow Getter")
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1024
        window_height = 767
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.window.resizable(False, False)
        
        self.background = PhotoImage(file="assets/background.png")
        self.button_image = PhotoImage(file="assets/login.png")
        self.button1_image = PhotoImage(file="assets/register.png")
        self.button2_image = PhotoImage(file="assets/staff.png")
        
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
        
        self.staff_button = Button(self.window, image=self.button2_image, command=self.staff_entry, border=0)
        self.staff_button.place(x=410, y=600)
        
        self.database_handler = DatabaseHandler()
        self.window.mainloop()

    def staff_entry(self):
        self.window.destroy()
        StaffLoginWindow()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == '' or password == '' and username == ' ' or password == ' ':
            showerror("Error", "Please enter a valid username and password")
        elif password == '':
            showerror("Error", "Please enter a valid password") 
        elif username == '':
            showerror("Error", "Please enter a valid username")
        elif self.database_handler.validate_user(username, password):
            self.window.destroy()
            ShoppingWindow(username)
        else:
            showerror("Error", "Invalid username or password")

class StaffLoginWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Glow Getter : Staff Login")
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1024
        window_height = 767
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.window.resizable(False, False)
        
        self.background2 = PhotoImage(file="assets/background2.png")
        self.button_image = PhotoImage(file="assets/login.png")
        self.return_button = PhotoImage(file="assets/return.png")
        
        self.background_label = Label(self.window, image=self.background2)
        self.background_label.pack()
        
        self.username_entry = Entry(self.window, width=30)
        self.username_entry.place(x=389, y=352)
        self.username_entry.config(font=("Arial"))
        
        self.password_entry = Entry(self.window, width=30, show="*")
        self.password_entry.place(x=389, y=437)
        self.password_entry.config(font=("Arial"))
        
        self.login_button = Button(self.window, image=self.button_image, command=self.login, border=0)
        self.login_button.place(x=440, y=512)
        
        self.exit_button = Button(self.window, image=self.return_button, command=self.exit, border=0, bg='white')
        self.exit_button.place(x=376, y=600)
        
        self.window.mainloop()
    
    def exit(self):
        self.window.destroy()
        MainMenu()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == 'staff1' and password == 'staff123':
            showinfo("Login Successful", "Welcome, staff member!")
            self.window.destroy()
            StaffDashboard(username)
        else:
            showerror("Error", "Invalid username or password")

class StaffDashboard:
    def __init__(self, username):
        self.username = username
        self.db_handler = DatabaseHandler()
        self.window = Tk()
        self.window.title("Glow Getter : Staff Dashboard")
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1024
        window_height = 768
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.window.resizable(False, False)
        
        self.background3 = PhotoImage(file="assets/shop_background2.png")
        self.exit_button = PhotoImage(file="assets/exit.png")
        self.background_label = Label(self.window, image=self.background3)
        self.background_label.pack()
        
        self.total_orders_label = Label(self.window, text="Total Orders Made: 0", font=("Arial", 16, "bold"), bg='#939974', fg='white')
        self.total_orders_label.place(x=50, y=15)
        
        self.exit_button1 = Button(self.window, image=self.exit_button, command=self.exit, border=0, bg='white')
        self.exit_button1.place(x=950, y=60)
        
        self.product_quantity_label = Label(self.window, text="Products and Quantities:", font=("Arial", 16, "bold"), bg='#939974', fg='white')
        self.product_quantity_label.place(x=50, y=100)
        
        self.product_quantity_listbox = Listbox(self.window, width=50, height=20, font=("Arial", 12))
        self.product_quantity_listbox.place(x=50, y=150)
        
        self.restock_button = Button(self.window, text="Restock Item", bg='white', fg='black', font=("Arial", 16), command=self.restock_item)
        self.restock_button.place(x=50, y=540)
        
        self.edit_quantity_button = Button(self.window, text="Edit Quantity", bg='white', fg='black', font=("Arial", 16), command=self.edit_quantity)
        self.edit_quantity_button.place(x=200, y=540)
        
        self.remove_product_button = Button(self.window, text="Remove Product", bg='white', fg='black', font=("Arial", 16), command=self.remove_product)
        self.remove_product_button.place(x=350, y=540)
        
        self.add_product_button = Button(self.window, text="Add Product", bg='white', fg='black', font=("Arial", 16), command=self.add_product)
        self.add_product_button.place(x=50, y=600)
        
        self.messages_label = Label(self.window, text="Messages:", font=("Arial", 16, "bold"), bg='#939974', fg='white')
        self.messages_label.place(x=550, y=100)
        
        self.messages_listbox = Listbox(self.window, width=50, height=20, font=("Arial", 12))
        self.messages_listbox.place(x=550, y=150)
        
        self.reply_button = Button(self.window, text="Reply", bg='white', fg='black', font=("Arial", 16), command=self.reply_message)
        self.reply_button.place(x=900, y=540)
        
        self.load_product_quantities()
        self.update_total_orders()
        self.load_messages()
        
        self.window.mainloop()
    
    def load_product_quantities(self):
        self.product_quantity_listbox.delete(0, END)
        products = self.db_handler.get_products()
        for product in products:
            _, name, _, quantity, _, _ = product
            self.product_quantity_listbox.insert(END, f"{name}: {quantity}")
        
    def update_total_orders(self):
        total_orders = self.db_handler.get_total_orders()
        self.total_orders_label.config(text=f"Total Orders Made: {total_orders}")
        
    def load_messages(self):
        self.messages_listbox.delete(0, END)
        messages = self.db_handler.get_messages()
        for message in messages:
            message_id, username, text, timestamp = message
            self.messages_listbox.insert(END, f"{message_id} - {username}: {text} ({timestamp})")
    
    def restock_item(self):
        selected_product = self.product_quantity_listbox.get(ACTIVE)
        if selected_product:
            product_name = selected_product.split(":")[0]
            quantity = simpledialog.askinteger("Restock Item", f"Enter quantity to restock for {product_name}:")
            if quantity is not None:
                if quantity < 0:
                    showerror("Error", "Quantity must be a positive number")
                if quantity > 999:
                    showerror("Error", "Quantity cannot exceed 999")
                    return
                self.db_handler.update_product_quantity(product_name, quantity)
                self.load_product_quantities()
    
    def edit_quantity(self):
        selected_product = self.product_quantity_listbox.get(ACTIVE)
        if selected_product:
            product_name = selected_product.split(":")[0]
            quantity = simpledialog.askinteger("Edit Quantity", f"Enter new quantity for {product_name}:")
            if quantity is not None:
                if quantity < 0:
                    showerror("Error", "Quantity must be a positive number")
                if quantity > 999:
                    showerror("Error", "Quantity cannot exceed 999")
                    return
                self.db_handler.update_product_quantity(product_name, quantity)
                self.load_product_quantities()
    
    def remove_product(self):
        selected_product = self.product_quantity_listbox.get(ACTIVE)
        if selected_product:
            product_name = selected_product.split(":")[0]
            product_id = self.db_handler.get_products(product_name)
            if product_id is not None:
                self.db_handler.remove_product(product_id)
                self.load_product_quantities()
    
    def add_product(self):
        name = simpledialog.askstring("Add Product", "Enter product name:")
        if name:
            price = simpledialog.askfloat("Add Product", "Enter product price:")
            if price is not None:
                quantity = simpledialog.askinteger("Add Product", "Enter product quantity:")
                if quantity is not None:
                    image_path = simpledialog.askstring("Add Product", "Enter image path:")
                    if image_path:
                        self.db_handler.add_product(name, price, quantity, image_path)
                        self.load_product_quantities()
    
    def reply_message(self):
        try:
            selected_message = self.messages_listbox.get(ACTIVE)
            message_id = int(selected_message.split(" - ")[0])
            username = selected_message.split(":")[0].split(" - ")[1]
            response = simpledialog.askstring("Reply", f"Enter your reply to {username}:")
            if response:
                self.db_handler.insert_response(message_id, self.username, response)
                showinfo("Reply Sent", "Your reply has been sent.")
        except IndexError:
            showerror("Error", "Failed to parse the selected message.")

    def exit(self):
        self.window.destroy()
        MainMenu()

class ShoppingWindow:
    def __init__(self, username):
        self.username = username
        self.db_handler = DatabaseHandler()
        self.cart = []  # Initialize an empty cart
        self.total_price = 0.0  # Initialize total price
        self.product_widgets = []  # List to keep track of product widgets
        
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
        self.exit_button = PhotoImage(file="assets/exit.png")
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
        
        self.exit_button1 = Button(self.window, image=self.exit_button, command=self.exit, border=0, bg='#939974')
        self.exit_button1.place(x=85, y=42)
        
        self.selected_item_entry = Text(self.window, width=20, height=38, state='disabled', bg='#f7f7f7')
        self.selected_item_entry.place(x=60, y=200)
        self.selected_item_entry.config(font=("Arial", 12))
        
        self.total_price_label = Label(self.window, text="Total Price: $0.00", font=("Arial", 12, "bold"), bg='#939974', fg='white')
        self.total_price_label.place(x=80, y=900)  
        
        self.order_button = Button(self.window, text="Order", bg='white', fg='black', command=self.place_order)
        self.order_button.place(x=80, y=900) 
        
        self.load_products()
        self.window.mainloop()
    
    def exit(self):
        self.window.destroy()
        MainMenu()
    
    def send_message(self):
        ChatWindow(self.username)
        
    def load_products(self):
        self.clear_product_widgets()  # Clear existing product widgets
        products = self.database_handler.get_products()
        x_position = 320
        y_position = 250
        for product in products:
            product_id, name, price, quantity, image_path, rating = product  # Ensure the correct number of columns are selected
            
            # Log the image_path for debugging
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
            product_label.config(width=150, height=150)  # Increase the size of the product image
            product_label.place(x=x_position, y=y_position)
            self.product_widgets.append(product_label)
            
            product_name_label = Label(self.window, text=name, font=("Arial", 16, "bold"), fg='#939974')  # Increase font size
            product_name_label.place(x=x_position, y=y_position + 160)
            self.product_widgets.append(product_name_label)
            
            product_price_label = Label(self.window, text=f"${price:.2f}", font=("Arial", 16), fg='#939974')  # Increase font size
            product_price_label.place(x=x_position, y=y_position + 190)
            self.product_widgets.append(product_price_label)
            
            quantity_label = Label(self.window, text="Quantity:", font=("Arial", 16), fg='#939974')  # Increase font size
            quantity_label.place(x=x_position, y=y_position + 220)
            self.product_widgets.append(quantity_label)
            
            quantity_spinbox = Spinbox(self.window, from_=1, to=50, width=5, font=("Arial", 16))  # Increase font size
            quantity_spinbox.place(x=x_position + 120, y=y_position + 220)
            self.product_widgets.append(quantity_spinbox)
            
            select_button = Button(self.window, text="Add to Cart", bg='white', fg='black', font=("Arial", 13), command=lambda p_id=product_id, p_name=name, p_price=price, q=quantity_spinbox: self.select_product(p_id, p_name, p_price, q))  # Increase font size
            select_button.place(x=x_position, y=y_position + 260)
            self.product_widgets.append(select_button)
            
            rating_label = Label(self.window, text=f"Rating: {rating:.1f}", font=("Arial", 16), bg='#939974', fg='white')  # Increase font size
            rating_label.place(x=x_position, y=y_position + 300)
            self.product_widgets.append(rating_label)
            
            rate_button = Button(self.window, text="Rate", bg='white', fg='black', font=("Arial", 16), command=lambda p_id=product_id: self.rate_product(p_id))  # Increase font size
            rate_button.place(x=x_position + 120, y=y_position + 290)
            self.product_widgets.append(rate_button)
            
            x_position += 220  # Adjust this value to control the horizontal spacing
            if x_position > 1000:
                x_position = 320  # Reset to the starting position
                y_position += 350  # Move to the next row

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
        self.database_handler.save_order(user_id)  # Save the order to the database
        self.database_handler.clear_cart(user_id)
        self.selected_item_entry.config(state='normal')
        self.selected_item_entry.delete("1.0", END)
        self.selected_item_entry.config(state='disabled')
        self.total_price = 0.0
        self.total_price_label.config(text="Total Price: $0.00")
        self.load_products()  # Reload products to update the UI
        showinfo("Order Placed", "Your order has been placed successfully")
        
    def get_cart_items(self, user_id):
        cart_items = self.database_handler.get_cart_items(user_id)
        if not cart_items:
            showerror("Error", "Your cart is empty")
        return cart_items

    def save_and_clear_order(self, user_id, cart_items):
            self.total_price = 0.0
            self.total_price_label.config(text=f"Total Price: ${self.total_price:.2f}")
            showinfo("Order Placed", "Your order has been placed successfully")
    def reset_order_ui(self):
        self.selected_item_entry.config(state='normal')
        self.selected_item_entry.delete("1.0", END)
        self.selected_item_entry.config(state='disabled')
        self.total_price = 0.0
        self.total_price_label.config(text="Total Price: $0.00")
        showerror("Error", "Invalid price for item")
        return
    
    def rate_product(self, product_id):
        rating = simpledialog.askfloat("Rate Product", "Enter your rating (0-5):", minvalue=0, maxvalue=5)
        if rating is not None:
            self.database_handler.update_product_rating(product_id, rating)
            self.load_products()  # Reload products to update ratings
        
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
        self.send_button.place(x=500, y=120)
        
        self.chat_box = Text(self.window)
        self.chat_box.pack()
        self.chat_box.config(font=("Arial", 12), width=50, height=5)
        self.chat_box.place(x=80, y=10)
        
        self.replies_listbox = Listbox(self.window, width=50, height=10, font=("Arial", 12))
        self.replies_listbox.place(x=80, y=170)
        
        self.offset = 0
        self.load_replies()
        
        self.prev_button = Button(self.window, text="Previous", command=self.prev_page)
        self.prev_button.place(x=80, y=370)
        
        self.next_button = Button(self.window, text="Next", command=self.next_page)
        self.next_button.place(x=500, y=370)
        
        self.window.mainloop() 

    def send_message(self):
        message = self.chat_box.get("1.0", "end-1c")
        if message.strip():
            user_id = self.db_handler.get_user_id(self.username)
            self.db_handler.insert_message(user_id, message)
            showinfo("Message Sent", "Your message has been sent and stored in the database.")
            self.chat_box.delete("1.0", END)
            self.load_replies()  # Reload replies to show the new message
        else:
            showwarning("Empty Message", "Cannot send an empty message.")
    
    def load_replies(self):
            self.replies_listbox.delete(0, END)
            
    def populate_replies_listbox(self, replies):
        for reply in replies:
            for reply in replies:
                response, timestamp, staff_username = reply
                self.replies_listbox.insert(END, f"{staff_username}: {response} ({timestamp})")
            self.update_pagination_buttons()
    
    def update_pagination_buttons(self):
            if self.offset > 0:
                self.prev_button.config(state=NORMAL)
            else:
                self.prev_button.config(state=DISABLED)
            
            if len(self.db_handler.get_responses(self.db_handler.get_user_id(self.username), limit=10, offset=self.offset + 10)) > 0:
                self.next_button.config(state=NORMAL)
            else:
                self.next_button.config(state=DISABLED)
    
    def next_page(self):
            self.offset += 10
            self.load_replies()
    
    def prev_page(self):
            self.offset -= 10
            self.load_replies()
            self.replies_listbox.delete(0, END)

    def populate_replies_listbox(self, replies):
        for reply in replies:
            reply_id, staff_id, text, timestamp = reply
            self.replies_listbox.insert(END, f"{reply_id} - {staff_id}: {text} ({timestamp})")

if __name__ == "__main__":
    ShoppingWindow("test")