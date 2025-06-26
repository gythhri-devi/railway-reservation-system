import pickle as p
import os
import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

try:
    connect = mysql.connector.connect(
        host='localhost',
        user='root',
        password='tiger',
        database='test'
    )
    if connect.is_connected():
        mycursor = connect.cursor()
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Database Error", "Error connecting to the database.")
        exit()
except mysql.connector.Error as err:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Database Error", f"Could not connect to the database: {err}")
    exit()

def writefile(data):
    with open('project.dat', 'ab') as outfile:
        p.dump(data, outfile)

def delete_ticket_from_file(nam):
    flag = False
    temp_file = 'Project.tmp'
    original_file = 'project.dat'

    try:
        with open(original_file, 'rb') as infile, open(temp_file, 'wb') as outfile:
            while True:
                try:
                    ticket = p.load(infile)
                    if ticket['name'].lower() != nam.lower():
                        p.dump(ticket, outfile)
                    else:
                        flag = True
                except EOFError:
                    break
        
        os.remove(original_file)
        os.rename(temp_file, original_file)
        return flag
    except FileNotFoundError:
        messagebox.showinfo("Info", "No tickets booked yet.")
        return False


class RailwayReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Reservation System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TFrame", background="#f0f2f5")
        style.configure("TLabel", background="#f0f2f5", font=("Helvetica", 10, "bold"), foreground="#555")
        style.configure("TButton", font=("Helvetica", 11, "bold"), borderwidth=0)
        style.map("TButton",
                  background=[('active', '#0056b3'), ('!disabled', '#007bff')],
                  foreground=[('!disabled', 'white')])
        style.configure("TEntry",
                        fieldbackground="#e9ecef",
                        font=("Helvetica", 12),
                        padding=10,
                        borderwidth=0)

        start_locations = [
            "trivandrum",
            "chennai",
            "bangalore",
            "hyderabad",
            "panaji"
        ]
        end_locations = [
            "chennai", "bangalore", "bhopal", "bubaneswar", "chandigarh",
            "dehradun", "delhi", "gandhinagar", "hyderabad", "jaipur",
            "jammu", "kolkata", "lucknow", "mumbai", "panaji", "patna",
            "raipur", "ranchi", "shimla", "agartala", "trivandrum"
        ]

        top_frame = ttk.Frame(root, padding="30 20 30 20")
        top_frame.pack(fill="x")

        center_frame = ttk.Frame(top_frame)
        center_frame.pack()
        
        from_frame = ttk.Frame(center_frame)
        from_frame.grid(row=0, column=0, padx=10)
        ttk.Label(from_frame, text="FROM").pack(anchor='w', pady=(0, 5))
        self.from_entry = ttk.Combobox(from_frame, width=28, values=start_locations, state="readonly")
        self.from_entry.pack()

        to_frame = ttk.Frame(center_frame)
        to_frame.grid(row=0, column=1, padx=10)
        ttk.Label(to_frame, text="TO").pack(anchor='w', pady=(0, 5))
        self.to_entry = ttk.Combobox(to_frame, width=28, values=end_locations, state="readonly")
        self.to_entry.pack()

        date_search_frame = ttk.Frame(center_frame)
        date_search_frame.grid(row=0, column=2, padx=10, sticky="s")

        date_frame = ttk.Frame(date_search_frame)
        date_frame.pack(side="left", fill="y")
        ttk.Label(date_frame, text="DATE").pack(anchor='w', pady=(0, 5))
        self.date_entry = ttk.Entry(date_frame, width=15)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.pack()
        
        search_button_frame = ttk.Frame(date_search_frame)
        search_button_frame.pack(side="left", fill="y", padx=(10, 0))
        # Use a spacer label to push the button down
        ttk.Label(search_button_frame, text="").pack()
        search_button = ttk.Button(search_button_frame, text="SEARCH", command=self.search_trains, padding=(20, 8))
        search_button.pack(anchor="s")

        self.results_container = ttk.Frame(root)
        self.results_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        ticket_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Manage Tickets", menu=ticket_menu)
        ticket_menu.add_command(label="View All My Tickets", command=self.display_all_tickets)
        ticket_menu.add_command(label="Delete a Ticket", command=self.delete_ticket_prompt)
        ticket_menu.add_separator()
        ticket_menu.add_command(label="Checkout", command=self.checkout_prompt)

    def clear_results_frame(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()

    def search_trains(self):
        self.clear_results_frame()
        start = self.from_entry.get()
        end = self.to_entry.get()

        if not start or not end:
            messagebox.showerror("Error", "Please enter both 'From' and 'To' locations.")
            return

        sql = "SELECT * FROM schedule WHERE start = %s AND end = %s"
        try:
            mycursor.execute(sql, (start, end))
            trains = mycursor.fetchall()

            if not trains:
                ttk.Label(self.results_container, text="No trains found for this route.", font=("Helvetica", 12)).pack(pady=20)
                return
            
            for train in trains:
                train_frame = ttk.Frame(self.results_container, padding=15, relief="solid", borderwidth=1)
                train_frame.pack(fill="x", pady=5, padx=30)
                
                details_text = f"Train: {train[5]} ({train[6]})    From: {train[0]}    To: {train[1]}    Price: ${train[4]}"
                ttk.Label(train_frame, text=details_text, font=("Helvetica", 11)).pack(side="left", expand=True, fill="x")
                
                book_button = ttk.Button(train_frame, text="Book Now", command=lambda t=train: self.open_booking_window(t))
                book_button.pack(side="right")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to search trains: {err}")

    def open_booking_window(self, train_info):
        date = self.date_entry.get()
        if not date or date == "YYYY-MM-DD":
            messagebox.showerror("Error", "Please enter a valid departure date before booking.")
            return

        booking_window = tk.Toplevel(self.root)
        booking_window.title("Enter Passenger Details")
        booking_window.geometry("350x250")
        booking_window.transient(self.root)
        booking_window.grab_set()

        frame = ttk.Frame(booking_window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w", pady=5)
        age_entry = ttk.Entry(frame)
        age_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Berth:").grid(row=2, column=0, sticky="w", pady=5)
        berth_entry = ttk.Entry(frame)
        berth_entry.grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text="Gender (F/M/O):").grid(row=3, column=0, sticky="w", pady=5)
        gender_entry = ttk.Entry(frame)
        gender_entry.grid(row=3, column=1, sticky="ew")

        frame.columnconfigure(1, weight=1)

        def confirm_booking():
            ticket = {
                'train': train_info[6], 'date': date, 'name': name_entry.get(),
                'age': age_entry.get(), 'berth': berth_entry.get(), 'gen': gender_entry.get()
            }
            if not all(ticket.values()):
                messagebox.showerror("Error", "Please fill all fields.", parent=booking_window)
                return
            
            writefile(ticket)
            messagebox.showinfo("Success", f"Ticket booked for {ticket['name']} on train {ticket['train']}.")
            booking_window.destroy()
            self.display_all_tickets()

        confirm_button = ttk.Button(frame, text="Confirm Booking", command=confirm_booking)
        confirm_button.grid(row=4, columnspan=2, pady=20)
        
    def display_all_tickets(self):
        self.clear_results_frame()
        try:
            with open('project.dat', 'rb') as infile:
                ttk.Label(self.results_container, text="--- YOUR BOOKED TICKETS ---", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
                while True:
                    try:
                        data = p.load(infile)
                        ticket_frame = ttk.Frame(self.results_container, padding=10, relief="solid", borderwidth=1)
                        ticket_frame.pack(fill="x", pady=5, padx=30)
                        
                        info = (f"Name: {data['name']} (Age: {data['age']})    Train: {data['train']}    "
                                f"Date: {data['date']}    Berth: {data['berth']}")
                        ttk.Label(ticket_frame, text=info).pack(anchor="w")

                    except EOFError:
                        break
        except FileNotFoundError:
            ttk.Label(self.results_container, text="No tickets booked yet.", font=("Helvetica", 12)).pack(pady=20)
    
    def delete_ticket_prompt(self):
        name = simpledialog.askstring("Delete Ticket", "Enter the full name on the ticket to delete:", parent=self.root)
        if name:
            if delete_ticket_from_file(name):
                messagebox.showinfo("Success", f"Ticket for '{name}' has been deleted.")
                self.display_all_tickets()
            else:
                messagebox.showerror("Error", f"No ticket found for '{name}'.")

    def checkout_prompt(self):
        train_no = simpledialog.askstring("Checkout", "Enter the Train Number to calculate total price:", parent=self.root)
        if not train_no:
            return

        try:
            count = 0
            with open('project.dat', 'rb') as infile:
                while True:
                    try:
                        ticket = p.load(infile)
                        if str(ticket['train']) == str(train_no):
                            count += 1
                    except EOFError:
                        break
            if count == 0:
                messagebox.showinfo("Info", f"No tickets found for train number {train_no}.")
                return

            sql = 'SELECT price FROM schedule WHERE trainno = %s'
            mycursor.execute(sql, (train_no,))
            price_result = mycursor.fetchone()

            if price_result:
                total_price = count * price_result[0]
                messagebox.showinfo("Checkout", f"Total price for {count} ticket(s) on train {train_no} is: ${total_price}")
            else:
                messagebox.showerror("Error", f"Could not find price for train number {train_no}.")

        except FileNotFoundError:
            messagebox.showinfo("Info", "No tickets have been booked yet.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Checkout failed: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayReservationSystem(root)
    root.mainloop()
    # Close the cursor and connection when the application is closed
    mycursor.close()
    connect.close()
