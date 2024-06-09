import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import scrolledtext  # Import scrolledtext for scrollable text
from pymongo import MongoClient
from bson.objectid import ObjectId  # To handle MongoDB ObjectIDs
from datetime import datetime
from tkinter import font

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

        # Setup menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.customer_menu = tk.Menu(self.menu, tearoff="off")
        self.menu.add_cascade(label="Customers", menu=self.customer_menu)
        self.customer_menu.add_command(label="Show All Customers", command=self.show_customers)
        self.customer_menu.add_command(label="Search Customer", command=self.search_customer)
        self.customer_menu.add_command(label="Add Customer", command=self.add_customer)
        self.customer_menu.add_command(label="Delete Customer", command=self.delete_customer)

        self.appointment_menu = tk.Menu(self.menu, tearoff="off")
        self.menu.add_cascade(label="Appointments", menu=self.appointment_menu)
        self.appointment_menu.add_command(label="Show Future Appointments", command=self.show_appointment)
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

    def show_customers(self):
        # Clear previous information
        self.info_text.delete('1.0', tk.END)

        customers = customers_collection.find({})
        for customer in customers:
            self.info_text.insert(tk.END, f"Customer ID: {customer.get('_id')}\n",'style')
            self.info_text.insert(tk.END, f"Customer Name: {customer.get('name')}\n",'style')
            self.info_text.insert(tk.END, f"Customer Vehicle: {customer.get('car')}\n",'style')
            self.info_text.insert(tk.END, f"Customer Phone: {customer.get('phoneNumber')}\n\n",'style')

    def search_customer(self):
        # Clear previous information
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
        # Clear previous information
        self.info_text.delete('1.0', tk.END)
        # Create a new top-level window for input
        top = tk.Toplevel(self.root)
        top.title("Add Customer")

        window_width = 300
        window_height = 200
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        top.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
            # Format the phone number as xxx-xxx-xxxx
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
            top.destroy()  # Close the popup window after successful insertion

        add_button = tk.Button(top, text="Add", command=add_customer_to_database)
        add_button.pack()

    def delete_customer(self):
        # Clear previous information
        self.info_text.delete('1.0', tk.END)
        customer_id = simpledialog.askstring("Input", "Enter customer ID to delete:")
        if not customer_id:
            return

        result = customers_collection.delete_one({"_id": ObjectId(customer_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Customer deleted successfully.")
        else:
            messagebox.showinfo("Not Found", "Customer ID not found.")

    def show_appointment(self):
        # Clear previous information
        self.info_text.delete('1.0', tk.END)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        appointments = appointments_collection.find({})
        future_appointments = ""

        for appointment in appointments:
            if appointment.get("appointmentDate") + " " + appointment.get("appointmentTime") > current_time:
                self.info_text.insert(tk.END, f"Customer: {appointment.get('customerName')}\n",'style')
                self.info_text.insert(tk.END, f"Phone: {appointment.get('customerPhone')}\n",'style')
                self.info_text.insert(tk.END, f"Vehicle: {appointment.get('car')}\n",'style')
                self.info_text.insert(tk.END, f"Appointment: {appointment.get('appointmentDate')} {appointment.get('appointmentTime')}\n\n",'style')

    def add_appointment(self):
        # Clear previous information
        self.info_text.delete('1.0', tk.END)

        # Create a new top-level window for input
        top = tk.Toplevel(self.root)
        top.title("Add Appointment")

        window_width = 300
        window_height = 300
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        top.geometry(f"{window_width}x{window_height}+{x}+{y}")

        customer_name_label = tk.Label(top, text="Customer Name:")
        customer_name_label.pack()
        customer_name_entry = tk.Entry(top)
        customer_name_entry.pack()

        customer_phone_label = tk.Label(top, text="Customer Phone:")
        customer_phone_label.pack()
        customer_phone_entry = tk.Entry(top)
        customer_phone_entry.pack()

        car_label = tk.Label(top, text="Customer Vehicle:")
        car_label.pack()
        car_entry = tk.Entry(top)
        car_entry.pack()

        appointment_date_label = tk.Label(top, text="Appointment Date (YYYY-MM-DD):")
        appointment_date_label.pack()
        appointment_date_entry = tk.Entry(top)
        appointment_date_entry.pack()

        appointment_time_label = tk.Label(top, text="Appointment Time (HH:MM):")
        appointment_time_label.pack()
        appointment_time_entry = tk.Entry(top)
        appointment_time_entry.pack()

        def add_appointment_to_database():
            customer_name = customer_name_entry.get()
            customer_phone = customer_phone_entry.get()
            car = car_entry.get()
            appointment_date = appointment_date_entry.get()
            appointment_time = appointment_time_entry.get()

            if not (customer_name and customer_phone and car and appointment_date and appointment_time):
                messagebox.showwarning("Input Error", "All fields are required!")
                return
            appointment = {
                "customerName": customer_name,
                "customerPhone": customer_phone,
                "car": car,
                "appointmentDate": appointment_date,                    
                "appointmentTime": appointment_time
                }
            appointments_collection.insert_one(appointment)
            messagebox.showinfo("Success", "Appointment added successfully.")
            top.destroy()  # Close the popup window after successful insertion
        add_button = tk.Button(top, text="Add", command=add_appointment_to_database)
        add_button.pack()

    def delete_appointment(self):
        # Clear previous information
        self.info_text.delete('1.0', tk.END)
        appointment_id = simpledialog.askstring("Input", "Enter appointment ID to delete:")
        if not appointment_id:
            return

        result = appointments_collection.delete_one({"_id": ObjectId(appointment_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Appointment deleted successfully.")
        else:
            messagebox.showinfo("Not Found", "Appointment ID not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarWashApp(root)
    root.mainloop()
