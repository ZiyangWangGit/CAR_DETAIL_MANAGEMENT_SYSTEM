# customer.py
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, font
from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
url = 'mongodb://localhost:27017'
client = MongoClient(url)
db = client["CarDetailSystem"]
customers_collection = db["CarDetailCustomer"]

class CustomerFunctions:
    def __init__(self, root, info_text):
        self.root = root
        self.info_text = info_text
        self.custom_font = font.Font(family="Helvetica", size=12, weight='bold')

    def show_customers(self):
        self.info_text.delete('1.0', tk.END)
        customers = customers_collection.find({})
        for customer in customers:
            self.info_text.insert(tk.END, f"Customer ID: {customer.get('_id')}\n", 'style')
            self.info_text.insert(tk.END, f"Customer Name: {customer.get('name')}\n", 'style')
            self.info_text.insert(tk.END, f"Customer Vehicle: {customer.get('car')}\n", 'style')
            self.info_text.insert(tk.END, f"Customer Phone: {customer.get('phoneNumber')}\n\n", 'style')

    def search_customer(self):
        self.info_text.delete('1.0', tk.END)
        information = simpledialog.askstring("Input", "Enter customer name or phone (phone e.g., xxx-xxx-xxxx):")
        if not information:
            return
        
        customers = customers_collection.find({})
        for customer in customers:
            if (information.upper() in customer.get("name", "").upper() or
                information == customer.get("phoneNumber", "")):
                self.info_text.insert(tk.END, f"Name: {customer.get('name')}\n")
                self.info_text.insert(tk.END, f"Vehicle: {customer.get('car')}\n")
                self.info_text.insert(tk.END, f"Phone: {customer.get('phoneNumber')}\n")
                return      
        messagebox.showinfo("Not Found", "Sorry, customer not found.")

    def add_customer(self):
        self.info_text.delete('1.0', tk.END)
        top = tk.Toplevel(self.root)
        top.title("Add Customer")

        name_label = tk.Label(top, text="Customer Name:")
        name_label.pack()
        name_entry = tk.Entry(top)
        name_entry.pack()

        car_label = tk.Label(top, text="Customer Vehicle:")
        car_label.pack()
        car_entry = tk.Entry(top)
        car_entry.pack()

        phone_label = tk.Label(top, text="Customer Phone:")
        phone_label.pack()
        phone_entry = tk.Entry(top)
        phone_entry.pack()

        def add_customer_to_database():
            name = name_entry.get()
            car = car_entry.get()
            phone = phone_entry.get()
            if not phone.isdigit() or len(phone) != 10:
                messagebox.showwarning("Input Error", "Phone number must contain exactly 10 digits!")
                return
            formatted_phone = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"

            if not (name and car and phone):
                messagebox.showwarning("Input Error", "All fields are required!")
                return

            customer = {
                "name": name,
                "car": car,
                "phoneNumber": formatted_phone
            }
            customers_collection.insert_one(customer)
            messagebox.showinfo("Success", "Customer added successfully.")
            top.destroy()

        add_button = tk.Button(top, text="Add", command=add_customer_to_database)
        add_button.pack()

    def delete_customer(self):
        self.info_text.delete('1.0', tk.END)
        customer_id = simpledialog.askstring("Input", "Enter customer ID to delete:")
        if not customer_id:
            return

        result = customers_collection.delete_one({"_id": ObjectId(customer_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Customer deleted successfully.")
        else:
            messagebox.showinfo("Not Found", "Customer ID not found.")
