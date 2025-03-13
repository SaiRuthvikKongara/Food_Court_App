import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

class FoodCourtApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Fullscreen mode
        self.attributes('-fullscreen', True)
        self.title("Food Court App")

        # Data Initialization
        self.menu_items = self.load_menu_items()
        self.selected_items = []  # Store selected items
        self.total_price = 0  # Total price of selected items

        # Layout Frames
        self.create_header()
        self.create_menu_list()
        self.create_order_summary()
        self.create_footer()

    def create_header(self):
        header_frame = tk.Frame(self, bg="orange", bd=2, relief="groove")
        header_frame.pack(fill=tk.X, padx=10, pady=5)

        # Date and Time
        tk.Label(header_frame, text="Bill Date & Time:", bg="orange").grid(row=0, column=0, padx=5, pady=5)
        self.date_time_label = tk.Label(header_frame, text=self.get_current_datetime(), bg="white", width=25)
        self.date_time_label.grid(row=0, column=1, padx=5, pady=5)

    def get_current_datetime(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def create_menu_list(self):
        menu_frame = tk.Frame(self, bg="white", bd=2, relief="groove")
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.listbox_menu = tk.Listbox(menu_frame, width=50, height=15, font=("Arial", 12), bg="#FFF3E0", bd=2, relief="solid", selectmode=tk.MULTIPLE)
        self.listbox_menu.pack(pady=10)

        # Add Menu Item Section
        add_item_frame = tk.Frame(self, bg="orange", bd=2, relief="groove")
        add_item_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(add_item_frame, text="Item:", bg="orange").grid(row=0, column=0, padx=5, pady=5)
        self.entry_item = tk.Entry(add_item_frame, font=("Arial", 12), width=20, bd=2, relief="solid")
        self.entry_item.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_item_frame, text="Price:", bg="orange").grid(row=0, column=2, padx=5, pady=5)
        self.entry_price = tk.Entry(add_item_frame, font=("Arial", 12), width=10, bd=2, relief="solid")
        self.entry_price.grid(row=0, column=3, padx=5, pady=5)

        self.add_button = tk.Button(add_item_frame, text="Add Item", command=self.add_menu_item, font=("Arial", 12), bg="orange", fg="white", relief="solid", width=10)
        self.add_button.grid(row=0, column=4, padx=5)

        self.list_menu()

    def create_order_summary(self):
        summary_frame = tk.Frame(self, bg="orange", bd=2, relief="groove")
        summary_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(summary_frame, text="Total:", bg="orange", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.total_label = tk.Label(summary_frame, text="0", bg="yellow", font=("Arial", 16, "bold"), width=10)
        self.total_label.grid(row=0, column=1, padx=5, pady=5)

    def create_footer(self):
        footer_frame = tk.Frame(self, bg="lightgray", bd=2, relief="groove")
        footer_frame.pack(fill=tk.X, padx=10, pady=5)

        self.place_order_button = tk.Button(footer_frame, text="Place Order", command=self.place_order, font=("Arial", 14, "bold"), bg="orange", fg="white")
        self.place_order_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def load_menu_items(self):
        menu_items = []
        conn = mysql.connector.connect(host="localhost", user="", password="", database="foodcourt")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        items = cursor.fetchall()
        conn.close()

        for item in items:
            menu_items.append((item[1], item[2]))  # item name and price
        return menu_items

    def list_menu(self):
        self.listbox_menu.delete(0, tk.END)
        for item in self.menu_items:
            self.listbox_menu.insert(tk.END, f"{item[0]} - ₹{item[1]}")

    def add_menu_item(self):
        item_name = self.entry_item.get()
        price = self.entry_price.get()

        if item_name and price:
            conn = mysql.connector.connect(host="localhost", user="", password="", database="foodcourt")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO menu (item, price) VALUES (%s, %s)", (item_name, float(price)))
            conn.commit()
            conn.close()
            self.menu_items.append((item_name, float(price)))
            self.list_menu()
        else:
            messagebox.showwarning("Input Error", "Please enter both item and price.")

    def place_order(self):
        selected = self.listbox_menu.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "No items selected!")
            return

        order_items = []
        total = 0

        for i in selected:
            item_text = self.listbox_menu.get(i)
            item_name, price = item_text.split(" - ₹")
            total += float(price)
            order_items.append(item_name)

        self.total_price = total
        self.total_label.config(text=f"₹{total:.2f}")
        messagebox.showinfo("Order Placed", f"Total: ₹{total:.2f}\nItems: {', '.join(order_items)}")

if __name__ == "__main__":
    app = FoodCourtApp()
    app.mainloop()
