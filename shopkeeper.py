import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="shopkeeper"
    )

# Insert data into the database
def insert_data():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO products (product_name, cost_price, selling_price) VALUES (%s, %s, %s)"
    values = (entry_product_name.get(), entry_cost_price.get(), entry_selling_price.get())
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Product added successfully")

# Display all data from the database
def display_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    total_profit = 0
    for row in rows:
        tree.insert("", END, values=row)
        profit = row[3] - row[2]
        total_profit += profit

    label_total_profit.config(text=f"Total Profit: {total_profit}")
    cursor.close()
    conn.close()

# GUI setup
root = Tk()
root.title("Shopkeeper Management System")

# Form labels and entries
Label(root, text="Product Name").grid(row=0, column=0)
entry_product_name = Entry(root)
entry_product_name.grid(row=0, column=1)

Label(root, text="Cost Price").grid(row=1, column=0)
entry_cost_price = Entry(root)
entry_cost_price.grid(row=1, column=1)

Label(root, text="Selling Price").grid(row=2, column=0)
entry_selling_price = Entry(root)
entry_selling_price.grid(row=2, column=1)

# Buttons
Button(root, text="Add Product", command=insert_data).grid(row=3, column=0, columnspan=2)
Button(root, text="Display Products", command=display_data).grid(row=4, column=0, columnspan=2)

# Treeview for displaying products
tree = ttk.Treeview(root, columns=("Product No", "Product Name", "Cost Price", "Selling Price"), show='headings')
tree.heading("Product No", text="Product No")
tree.heading("Product Name", text="Product Name")
tree.heading("Cost Price", text="Cost Price")
tree.heading("Selling Price", text="Selling Price")
tree.grid(row=5, column=0, columnspan=2)

# Total profit label
label_total_profit = Label(root, text="Total Profit: 0")
label_total_profit.grid(row=6, column=0, columnspan=2)

root.mainloop()
