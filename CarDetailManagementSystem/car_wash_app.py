import tkinter as tk
from tkinter import messagebox, simpledialog
from pymongo import MongoClient
from bson.objectid import ObjectId  # To handle MongoDB ObjectIDs
from datetime import datetime

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
        screen_width = self.root.winfo_screenwidth()  # Access winfo_screenwidth() from the root widget
        screen_height = self.root.winfo_screenheight()  # Access winfo_screenheight() from the root widget
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set the size and position of the window

        # Setup menu
        self.menu = tk.Menu(self.root)
        #display the menu bar created with self.menu at the top of the root window
        self.root.config(menu=self.menu)

        self.customer_menu = tk.Menu(self.menu,tearoff="off")
        #submenu attached to it is self.customer_menu, which created in the previous line
        self.menu.add_cascade(label="Customers", menu=self.customer_menu) 
        self.customer_menu.add_command(label="Show All Customers", command=self.show_customers)
        self.customer_menu.add_command(label="Search Customer", command=self.search_customer)
        self.customer_menu.add_command(label="Add Customer", command=self.add_customer)
        self.customer_menu.add_command(label="Delete Customer", command=self.delete_customer)

        self.appointment_menu = tk.Menu(self.menu,tearoff="off")
        self.menu.add_cascade(label="Appointments", menu=self.appointment_menu)
        self.appointment_menu.add_command(label="Show Future Appointments", command=self.show_appointment)
        self.appointment_menu.add_command(label="Add Appointment", command=self.add_appointment)
        self.appointment_menu.add_command(label="Delete Appointment", command=self.delete_appointment)

        # Frame to display customer information
        #frame is a container widget that is used to hold other widgets, providing a way to organize and group 
        #them visually. In this case, the frame is created within the main application window (self.root).
        self.customer_frame = tk.Frame(self.root)
        #geometry manager to make the self.customer_frame visible within the main window (self.root).
        self.customer_frame.pack(fill=tk.BOTH, expand=True)

        # Label to display customer information
        #Labels are used to display text or images in a Tkinter GUI. In this case, the label is created within 
        #the self.customer_frame frame, which means it will be contained within that frame visually.
        #tk.Label: This part of the line creates a label widget using Tkinter's Label class. Labels are used to display text or images in a Tkinter GUI.
        #self.customer_frame: This is the parent container for the label widget. By specifying self.customer_frame as the first argument, we indicate that the label widget will be placed inside this frame.
        #text="": This parameter sets the initial text content of the label widget. In this case, the text content is an empty string "". This means that when the label is initially displayed, it will show no text.
        self.customer_info_label = tk.Label(self.customer_frame, text="")
        self.customer_info_label.pack()
        
        self.appointment_frame = tk.Frame(self.root)
        self.appointment_frame.pack(fill=tk.BOTH, expand=True)
        self.appointment_info_label = tk.Label(self.appointment_frame, text="")
        self.appointment_info_label.pack()

    def show_customers(self):
        self.appointment_info_label.config(text="")
        customers = customers_collection.find({})

        customer_info = ""
        for customer in customers:
            customer_info += f"Customer ID: {customer.get('_id')}\n" 
            customer_info += f"Customer Name: {customer.get('name')}\n"
            customer_info += f"Customer Vehicle: {customer.get('car')}\n"
            customer_info += f"Customer Phone: {customer.get('phoneNumber')}\n\n"
        #self.customer_info_label: This is the label widget that was previously created. It's the widget where we want to change the text content.
        #.config(): This method is used to configure properties of a widget.In this case, we're configuring the text property of the label widget.
        self.customer_info_label.config(text=customer_info if customer_info else "No customers found.")

    def search_customer(self):
        self.appointment_info_label.config(text="")
        self.customer_info_label.config(text="")
        information = simpledialog.askstring("Input", "Enter customer name or phone (phone e.g., xxx-xxx-xxxx):")
        if not information:
            return
        
        customers = customers_collection.find({})
        for customer in customers:
            if (information.upper() in customer.get("name", "").upper() or
                information == customer.get("phoneNumber", "")):
                customer_info = f"Name: {customer.get('name')}\nVehicle: {customer.get('car')}\nPhone: {customer.get('phoneNumber')}"
                self.customer_info_label.config(text=customer_info)
                return      
        messagebox.showinfo("Not Found", "Sorry, customer not found.")

    def add_customer(self):
        self.appointment_info_label.config(text="")
        self.customer_info_label.config(text="")
        # Create a new top-level window for input
        top = tk.Toplevel(self.root)
        top.title("Add Customer")

        window_width = 300
        window_height = 200
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        top.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set the size and position of the window

        name_label = tk.Label(top, text="Customer Name:")
        name_label.pack()  #added to the window and displayed according to the layout manager.
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
        self.appointment_info_label.config(text="")
        self.customer_info_label.config(text="")
        customer_id = simpledialog.askstring("Input", "Enter customer ID to delete:")
        if not customer_id:
            return
        
        result = customers_collection.delete_one({"_id": ObjectId(customer_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Customer deleted successfully.")
        else:
            messagebox.showinfo("Not Found", "Customer ID not found.")

    def show_appointment(self):
        self.customer_info_label.config(text="")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        appointments = appointments_collection.find({})
        future_appointments = ""
        for appointment in appointments:
            if appointment.get("appointmentDate") + " " + appointment.get("appointmentTime") > current_time:
                future_appointments += f"Customer: {appointment.get('customerName')}\n"
                future_appointments += f"Phone: {appointment.get('customerPhone')}\n"
                future_appointments += f"Vehicle: {appointment.get('car')}\n"
                future_appointments += f"Appointment: {appointment.get('appointmentDate')} {appointment.get('appointmentTime')}\n\n"
        self.appointment_info_label.config(text=future_appointments if future_appointments else "No customers found.")

    def add_appointment(self):
        self.appointment_info_label.config(text="")
        self.customer_info_label.config(text="")
        customer_name = simpledialog.askstring("Input", "Enter customer name:")
        customer_phone = simpledialog.askstring("Input", "Enter customer phone (e.g., xxx-xxx-xxxx):")
        car = simpledialog.askstring("Input", "Enter customer vehicle:")
        appointment_date = simpledialog.askstring("Input", "Enter appointment date (YYYY-MM-DD):")
        appointment_time = simpledialog.askstring("Input", "Enter appointment time (HH:MM):")
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

    def delete_appointment(self):
        self.appointment_info_label.config(text="")
        self.customer_info_label.config(text="")
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
