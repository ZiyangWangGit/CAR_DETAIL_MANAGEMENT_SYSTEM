# main.py
import tkinter as tk
from tkinter import scrolledtext, ttk, font
from tkinter import messagebox, simpledialog
from pymongo import MongoClient
from bson.objectid import ObjectId
from customer import CustomerFunctions
from appointment import AppointmentFunctions  # Ensure this matches the class name in appointment.py

# Connect to MongoDB
url = 'mongodb://localhost:27017'
client = MongoClient(url)
db = client["CarDetailSystem"]
customers_collection = db["CarDetailCustomer"]
appointments_collection = db["CarDetailAppointment"]

class CarWashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Wash Appointment System")
        window_width = 900
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Setup menu with grey background
        self.menu = tk.Menu(self.root, bg="grey", fg="white")
        self.root.config(menu=self.menu)

        self.customer_menu = tk.Menu(self.menu, tearoff="off", bg="grey", fg="white")
        self.menu.add_cascade(label="Customers", menu=self.customer_menu)
        self.customer_menu.add_command(label="Show All Customers", command=self.show_all_customers)
        self.customer_menu.add_command(label="Search Customer", command=self.search_customer)
        self.customer_menu.add_command(label="Add Customer", command=self.add_customer)
        self.customer_menu.add_command(label="Delete Customer", command=self.delete_customer)

        self.appointment_menu = tk.Menu(self.menu, tearoff="off", bg="grey", fg="white")
        self.menu.add_cascade(label="Appointments", menu=self.appointment_menu)
        self.appointment_menu.add_command(label="Show Past Appointments", command=self.show_history_appointments)
        self.appointment_menu.add_command(label="Show Future Appointments", command=self.show_future_appointments)
        self.appointment_menu.add_command(label="Search Appointment", command=self.search_appointment)
        self.appointment_menu.add_command(label="Add Appointment", command=self.add_appointment)
        self.appointment_menu.add_command(label="Delete Appointment", command=self.delete_appointment)

        # Frame to display customer and appointment information
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(fill=tk.BOTH, expand=True)

        # ScrolledText widget to display customer and appointment information
        self.info_text = scrolledtext.ScrolledText(self.info_frame, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Create a custom font
        self.custom_font = font.Font(family="Helvetica", size=12, weight='bold')
        self.info_text.tag_configure('style', font=self.custom_font)

        # Initialize CustomerFunctions and AppointmentFunctions
        self.customer_functions = CustomerFunctions(self.root, self.info_text)
        self.appointment_functions = AppointmentFunctions(self.root, self.info_text, appointments_collection)

    def show_all_customers(self):
        self.customer_functions.show_customers()

    def search_customer(self):
        self.customer_functions.search_customer()

    def add_customer(self):
        self.customer_functions.add_customer()

    def delete_customer(self):
        self.customer_functions.delete_customer()

    def show_history_appointments(self):
        self.appointment_functions.show_history_appointments()

    def show_future_appointments(self):
        self.appointment_functions.show_appointments()

    def add_appointment(self):
        self.appointment_functions.add_appointment()

    def delete_appointment(self):
        self.appointment_functions.delete_appointment()

    def search_appointment(self):
        self.appointment_functions.search_appointment()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarWashApp(root)
    root.mainloop()
