from tkinter import Tk
from Main import ShoppingWindow

def test_shopping_window():
    # Create a root window
    root = Tk()
    root.withdraw()  # Hide the root window

    # Create an instance of ShoppingWindow
    username = "test_user"
    shopping_window = ShoppingWindow(username)

    # Check if the window title is set correctly
    assert shopping_window.window.title() == "Glow Getter", "Window title is incorrect"

    # Check if the greeting label text is correct
    greeting_text = shopping_window.greeting.cget("text")
    assert greeting_text == f"Welcome, {username}", "Greeting text is incorrect"

    # Close the window after the test
    shopping_window.window.destroy()

if __name__ == "__main__":
    test_shopping_window()
    print("All tests passed!")