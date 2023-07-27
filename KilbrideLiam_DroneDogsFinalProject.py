import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from tkinter import simpledialog

# Function to validate name input (accepts alphabets and spaces)
def validate_name_input(char):
    return char.isalpha() or char.isspace()

# Function to validate card number input (accepts digits with length <= 16)
def validate_card_number_input(char):
    return char.isdigit() and len(char) <= 16

# Function to validate CVV input (accepts digits with length <= 3)
def validate_cvv_input(char):
    return char.isdigit() and len(char) <= 3

# Function to add item to the cart
def add_to_cart(item, price):
    cart_listbox.insert(tk.END, f"{item}: ${price:.2f}")
    calculate_total()

# Function to calculate the total price of the items in the cart
def calculate_total():
    global order_total
    order_total = 0
    for item in cart_listbox.get(0, tk.END):
        price = float(item.split(": $")[1])
        order_total += price
    total_label.config(text=f"Total: ${order_total:.2f}", font=("TT Norms", 12, "bold"))
    total_label_checkout.config(text=f"Total: ${order_total:.2f}", font=("TT Norms", 14, "bold"))

# Function to process the order
def process_order():
    name = name_entry.get()
    card_number = card_number_entry.get()
    expiration_date = expiration_date_var.get()
    cvv = cvv_entry.get()

    # Validate form fields are filled
    if not name or not card_number or not expiration_date or not cvv:
        messagebox.showwarning("Incomplete Form", "Please fill out all fields.")
        return

    # Validate card number length
    if len(card_number) != 16:
        messagebox.showwarning("Invalid Card Number", "Card number must be 16 digits.")
        return

    # Validate card number contains only digits
    if not card_number.isdigit():
        messagebox.showwarning("Invalid Card Number", "Card number must contain only digits.")
        return

    # Validate CVV length
    if len(cvv) != 3:
        messagebox.showwarning("Invalid CVV", "CVV must be 3 digits.")
        return

    # Validate CVV contains only digits
    if not cvv.isdigit():
        messagebox.showwarning("Invalid CVV", "CVV must contain only digits.")
        return

    try:
        date_obj = date.fromisoformat(expiration_date)  # Validate expiration date format

        # Validate if the expiration date is in the future
        if date_obj <= date.today():
            messagebox.showwarning("Invalid Expiration Date", "Expiration date must be in the future.")
            return

    except ValueError:
        messagebox.showwarning("Invalid Expiration Date", "Please enter a valid date in the format YYYY-MM-DD.")
        return

    # Show order confirmation message
    messagebox.showinfo("Order Processed", "Your payment has been processed and your order has been confirmed. "
                        "You will receive text updates on the delivery status. Keep an eye on the sky! "
                        "Thank you for your order!")

# Function to draw diagonal stripes on the canvas
def draw_diagonal_stripes(canvas, width, height):
    colors = ["#FFD700", "#4CBB17"]  # Yellow and green colors
    for i in range(-height, width, 10):
        canvas.create_line(i, 0, i + height, height, width=2, fill=colors[i // 10 % 2])

# Create the main app window
root = tk.Tk()
root.title("Drone Dogs Food Delivery")
root.geometry("400x350")
root.configure(bg="#FFD700")

# Create a notebook to organize different sections
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Configure styles for the notebook tabs
style = ttk.Style()
style.configure("TNotebook", tabposition="n", padding=10)
style.configure("TNotebook.Tab", font=("TT Norms", 14, "bold"))
# ----- Menu Section -----

# Create the menu frame and canvas
menu_frame = ttk.Frame(notebook)
menu_frame.pack(fill=tk.BOTH, expand=True)
menu_canvas = tk.Canvas(menu_frame, bg="#FFD700", highlightthickness=0)
menu_canvas.pack(fill=tk.BOTH, expand=True)
draw_diagonal_stripes(menu_canvas, 400, 350)

# Add the menu label to the canvas
menu_label = tk.Label(menu_canvas, text="Drone Dogs Menu", bg="#FFD700", fg="#4CBB17",
                      font=("TT Norms", 14, "bold"))
menu_label.pack(pady=10)

# Define the menu items and their prices
hotdogs = {
    "Classic Vienna Dog": 1.99,
    "Chili Cheese Dog": 2.99,
    "Kosher Dog": 3.99,
    "Bacon-Wrapped Dog": 5.99,
    "Veggie Dog": 3.99,
}

# Loop through the menu items and create a frame for each with labels and buttons
for hotdog, price in hotdogs.items():
    hotdog_frame = tk.Frame(menu_canvas, bg="#FFD700")
    hotdog_frame.pack(fill=tk.X)

    hotdog_price_label = tk.Label(hotdog_frame, text=f"${price:.2f}", bg="#FFD700", fg="#4CBB17",
                                  font=("TT Norms", 12))
    hotdog_price_label.pack(side=tk.LEFT, padx=5, pady=3)

    hotdog_label = tk.Label(hotdog_frame, text=f"{hotdog}", bg="#FFD700", fg="#4CBB17",
                            font=("TT Norms", 12, "bold"))
    hotdog_label.pack(side=tk.LEFT, padx=10, pady=3)

    add_to_cart_button = tk.Button(hotdog_frame, text="Add to Cart", bg="#4CBB17", fg="#FFD700",
                                   font=("TT Norms", 10, "bold"),
                                   command=lambda hotdog=hotdog, price=price: add_to_cart(hotdog, price))
    add_to_cart_button.pack(side=tk.RIGHT, padx=5, pady=3)

# ----- Cart Section -----

# Create the cart frame and canvas
cart_frame = ttk.Frame(notebook)
cart_frame.pack(fill=tk.BOTH, expand=True)
cart_canvas = tk.Canvas(cart_frame, bg="#FFD700", highlightthickness=0)
cart_canvas.pack(fill=tk.BOTH, expand=True)
draw_diagonal_stripes(cart_canvas, 400, 350)

# Add the cart label to the canvas
cart_label = tk.Label(cart_canvas, text="Cart Items", bg="#FFD700", fg="#4CBB17", font=("TT Norms", 14, "bold"))
cart_label.pack(pady=10)

# Create the cart listbox to display added items
cart_listbox = tk.Listbox(cart_canvas, bg="#FFD700", fg="#4CBB17", font=("TT Norms", 10), selectbackground="#4CBB17")
cart_listbox.pack(fill=tk.BOTH, expand=True)

# Add the total label to the cart canvas
total_label = tk.Label(cart_canvas, text="Total: $0.00", bg="#FFD700", fg="#4CBB17", font=("TT Norms", 12, "bold"))
total_label.pack(pady=5)

# ----- Checkout Section -----

# Create the checkout frame and add it to the notebook
checkout_frame = ttk.Frame(notebook)
checkout_frame.pack(fill=tk.BOTH, expand=True)

# Create the checkout canvas within the checkout frame
checkout_canvas = tk.Canvas(checkout_frame, bg="#FFD700", highlightthickness=0)
checkout_canvas.pack(fill=tk.BOTH, expand=True)

# Draw diagonal stripes on the checkout canvas
draw_diagonal_stripes(checkout_canvas, 400, 350)

# Initialize the order total
order_total = 0

# Create the total label for displaying the total amount in the checkout section
total_label_checkout = tk.Label(checkout_canvas, text="Total: $0.00", bg="#FFD700", fg="#4CBB17",
                                font=("TT Norms", 14, "bold"))
total_label_checkout.pack(pady=10)

# Create the credit card frame within the checkout canvas
credit_card_frame = tk.Frame(checkout_canvas, bg="#FFD700")
credit_card_frame.pack(pady=20)

# Create the name label for the credit card entry in the checkout section
name_label = tk.Label(credit_card_frame, text="Name on Card:", bg="#FFD700", fg="#4CBB17", font=("TT Norms", 11))
name_label.grid(row=0, column=0, pady=3)

# Create a validation command for name entry to accept only valid characters
vcmd_name = (root.register(validate_name_input), '%S')

# Create the name entry widget within the credit card frame
name_entry = tk.Entry(credit_card_frame, bg="#FFD700", fg="#4CBB17", font=("TT Norms", 11), validate="key",
                      validatecommand=vcmd_name)
name_entry.grid(row=0, column=1, pady=3)

# Create the card number label for the credit card entry in the checkout section
card_number_label = tk.Label(credit_card_frame, text="Card Number:", bg="#FFD700", fg="#4CBB17",
                             font=("TT Norms", 11))
card_number_label.grid(row=1, column=0, pady=3)

# Function to restrict card number length and ensure it contains only digits
def on_card_number_change(*args):
    value = card_number_var.get()
    if len(value) > 16:
        card_number_var.set(value[:16])
    if not value.isdigit():
        card_number_var.set(''.join(filter(str.isdigit, value)))

# Variable to store the card number as a string
card_number_var = tk.StringVar()
card_number_var.trace("w", on_card_number_change)

# Create the card number entry widget within the credit card frame
card_number_entry = tk.Entry(credit_card_frame, bg="#FFD700", fg="#4CBB17", font=("TT Norms", 11),
                             textvariable=card_number_var)
card_number_entry.grid(row=1, column=1, pady=3)

# Create the expiration date label for the credit card entry in the checkout section
expiration_date_label = tk.Label(credit_card_frame, text="Expiration Date:", bg="#FFD700", fg="#4CBB17",
                                 font=("TT Norms", 11))
expiration_date_label.grid(row=2, column=0, pady=3)

# Function to handle expiration date entry with a dialog box
def on_expiration_date_click():
    current_date = date.today()
    date_str = simpledialog.askstring("Expiration Date", "Enter Expiration Date (YYYY-MM-DD):",
                                      initialvalue=current_date.strftime("%Y-%m-%d"))
    if date_str:
        if not date_str.strip():
            messagebox.showwarning("Invalid Expiration Date", "Please enter a valid date.")
            return

        try:
            date_obj = date.fromisoformat(date_str)
        except ValueError:
            messagebox.showwarning("Invalid Expiration Date", "Please enter a valid date in the format YYYY-MM-DD.")
            return

        expiration_date_var.set(date_str)

# Variable to store the expiration date as a string
expiration_date_var = tk.StringVar()

# Create the expiration date entry widget within the credit card frame
expiration_date_entry = tk.Entry(credit_card_frame, bg="#FFD700", fg="#4CBB17", font=("TT Norms", 11),
                                 textvariable=expiration_date_var, state="readonly")
expiration_date_entry.grid(row=2, column=1, pady=3)
expiration_date_entry.bind("<Button-1>", lambda event: on_expiration_date_click())

# Create the CVV label for the credit card entry in the checkout section
cvv_label = tk.Label(credit_card_frame, text="CVV:", bg="#FFD700", fg="#4CBB17", font=("TT Norms", 11))
cvv_label.grid(row=3, column=0, pady=3)

# Function to restrict CVV length and ensure it contains only digits
def on_cvv_change(*args):
    value = cvv_var.get()
    if len(value) > 3:
        cvv_var.set(value[:3])
    if not value.isdigit():
        cvv_var.set(''.join(filter(str.isdigit, value)))

# Variable to store the CVV as a string
cvv_var = tk.StringVar()
cvv_var.trace("w", on_cvv_change)

# Create the CVV entry widget within the credit card frame
cvv_entry = tk.Entry(credit_card_frame, bg="#FFD700", fg="#4CBB17", font=("TT Norms", 11), textvariable=cvv_var)
cvv_entry.grid(row=3, column=1, pady=3)

# Create the "Process Order" button in the checkout section
process_button = tk.Button(checkout_canvas, text="Process Order", bg="#4CBB17", fg="#FFD700",
                           font=("TT Norms", 12, "bold"), command=process_order)
process_button.pack(pady=5)

# Add the "Menu," "Cart," and "Checkout" frames to the notebook
notebook.add(menu_frame, text="Menu")
notebook.add(cart_frame, text="Cart")
notebook.add(checkout_frame, text="Checkout")

# Start the main event loop
root.mainloop()
