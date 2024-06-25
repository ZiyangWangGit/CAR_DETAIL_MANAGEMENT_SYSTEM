# appointment.py
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, font
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# Connect to MongoDB
url = 'mongodb://localhost:27017'
client = MongoClient(url)
db = client["CarDetailSystem"]
appointments_collection = db["CarDetailAppointment"]

class AppointmentFunctions:
    def __init__(self, root, info_text, appointments_collection):
        self.root = root
        self.info_text = info_text
        self.appointments_collection = appointments_collection
        self.custom_font = font.Font(family="Helvetica", size=12, weight='bold')

    def show_history_appointments(self):
        self.info_text.delete('1.0', tk.END)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        appointments = self.appointments_collection.find({})
        for appointment in appointments:
            if appointment.get("appointmentDate") + " " + appointment.get("appointmentTime") <= current_time:
                self.info_text.insert(tk.END, f"Customer: {appointment.get('customerName')}\n", 'style')
                self.info_text.insert(tk.END, f"Phone: {appointment.get('customerPhone')}\n", 'style')
                self.info_text.insert(tk.END, f"Vehicle: {appointment.get('car')}\n", 'style')
                self.info_text.insert(tk.END, f"Appointment: {appointment.get('appointmentDate')} {appointment.get('appointmentTime')}\n\n", 'style')
                
    def show_appointments(self):
        self.info_text.delete('1.0', tk.END)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        appointments = self.appointments_collection.find({})
        for appointment in appointments:
            if appointment.get("appointmentDate") + " " + appointment.get("appointmentTime") > current_time:
                self.info_text.insert(tk.END, f"Customer: {appointment.get('customerName')}\n", 'style')
                self.info_text.insert(tk.END, f"Phone: {appointment.get('customerPhone')}\n", 'style')
                self.info_text.insert(tk.END, f"Vehicle: {appointment.get('car')}\n", 'style')
                self.info_text.insert(tk.END, f"Appointment: {appointment.get('appointmentDate')} {appointment.get('appointmentTime')}\n\n", 'style')

    def add_appointment(self):
        self.info_text.delete('1.0', tk.END)
        top = tk.Toplevel(self.root)
        top.title("Add Appointment")

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
            self.appointments_collection.insert_one(appointment)
            messagebox.showinfo("Success", "Appointment added successfully.")
            top.destroy()

        add_button = tk.Button(top, text="Add", command=add_appointment_to_database)
        add_button.pack()

    def delete_appointment(self):
        self.info_text.delete('1.0', tk.END)
        appointment_id = simpledialog.askstring("Input", "Enter appointment ID to delete:")
        if not appointment_id:
            return

        result = self.appointments_collection.delete_one({"_id": ObjectId(appointment_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Appointment deleted successfully.")
        else:
            messagebox.showinfo("Not Found", "Appointment ID not found.")
   
    def search_appointment(self):
        self.info_text.delete('1.0', tk.END)
        phone_number = simpledialog.askstring("Input", "Enter customer phone number (e.g., xxx-xxx-xxxx):")
        if not phone_number:
            return
        
        appointments = appointments_collection.find({"customerPhone": phone_number})
        found = False
        for appointment in appointments:
            self.info_text.insert(tk.END, f"Customer: {appointment.get('customerName')}\n", 'style')
            self.info_text.insert(tk.END, f"Phone: {appointment.get('customerPhone')}\n", 'style')
            self.info_text.insert(tk.END, f"Vehicle: {appointment.get('car')}\n", 'style')
            self.info_text.insert(tk.END, f"Appointment: {appointment.get('appointmentDate')} {appointment.get('appointmentTime')}\n\n", 'style')
            found = True
        
        if not found:
            messagebox.showinfo("Not Found", "No appointments found for the given phone number.")