import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry  # Import the calendar widget
from app.reservation.reservation_controller import ReservationController


class ReservationsView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False
        self.current_reservation_id = None

        self.controller = ReservationController(self)

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.frame, text="Reservation Management Section", bg=secondary_color,
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=10)

        # Left Frame (30%) - Reservation Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()

        # Right Frame (70%) - Reservation List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)

        self.create_data_view()

    def create_form(self):
        tk.Label(self.form_frame, text="Reservations", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        tk.Label(self.form_frame, text="Room:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(self.form_frame, textvariable=self.room_var, state="readonly", font=("Helvetica", 12))
        self.room_dropdown.pack(fill="x", pady=10, ipady=5)
        self.load_rooms()

        tk.Label(self.form_frame, text="Amount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.amount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid", state="readonly")
        self.amount_entry.pack(fill="x", pady=10, ipady=5)

        tk.Label(self.form_frame, text="Customer:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.customer_var = tk.StringVar()
        self.customer_dropdown = ttk.Combobox(self.form_frame, textvariable=self.customer_var, state="readonly", font=("Helvetica", 12))
        self.customer_dropdown.pack(fill="x", pady=10, ipady=5)
        self.load_customers()

        tk.Label(self.form_frame, text="Check-in Date:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.check_in_calendar = DateEntry(self.form_frame, font=("Helvetica", 12), date_pattern="dd/mm/yyyy")
        self.check_in_calendar.pack(fill="x", pady=10, ipady=5)

        tk.Label(self.form_frame, text="Check-out Date:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.check_out_calendar = DateEntry(self.form_frame, font=("Helvetica", 12), date_pattern="dd/mm/yyyy")
        self.check_out_calendar.pack(fill="x", pady=10, ipady=5)

        tk.Label(self.form_frame, text="Status:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.status_var = tk.StringVar(value="Confirmed")
        statuses = ["Confirmed", "Cancelled", "Pending"]
        for status in statuses:
            tk.Radiobutton(
                self.form_frame, text=status, variable=self.status_var, value=status,
                bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12), anchor="w"
            ).pack(anchor="w")

        tk.Label(self.form_frame, text="Total Amount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.total_amount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.total_amount_entry.pack(fill="x", pady=10, ipady=5)

        self.add_button = tk.Button(
            self.form_frame, text="Add Reservation", font=("Helvetica", 14, "bold"),
            bg=self.primary_color, fg="white", relief="flat", command=self.handle_add_or_update, cursor="hand2"
        )
        self.add_button.pack(pady=20, fill="x", ipady=5)

        self.cancel_button = tk.Button(
            self.form_frame, text="Cancel", font=("Helvetica", 12),
            bg="grey", fg="white", relief="flat", command=self.reset_form, cursor="hand2"
        )
        self.cancel_button.pack(pady=10, fill="x", ipady=5)
        self.cancel_button.pack_forget()

    def load_rooms(self):
        rooms = self.controller.get_rooms()
        self.room_dropdown['values'] = [f"{room['roomNo']}" for room in rooms]
        self.room_dropdown.bind("<<ComboboxSelected>>", self.on_room_selected)

    def on_room_selected(self, event):
        selected_room = self.room_var.get()
        if not selected_room:
            return
        room_id = selected_room
        room_data = self.controller.get_room_by_id(room_id)
        if room_data and 'price' in room_data:
            self.amount_entry.config(state="normal")
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, room_data['price'])
            self.amount_entry.config(state="readonly")
        else:
            messagebox.showerror("Error", "Failed to fetch the amount for the selected room.")

    def load_customers(self):
        customers = self.controller.get_customers()
        self.customer_dropdown['values'] = [f"{customer['name']} ({customer['id']})" for customer in customers]

    def handle_add_or_update(self):
        selected_room = self.room_var.get()
        room_id = next((room['id'] for room in self.controller.get_rooms() if f"{room['roomNo']}" == selected_room), None)
        if not room_id:
            messagebox.showerror("Error", "Invalid room selection. Please select a valid room.")
            return

        # Extracting customer ID correctly
        customer_id = None
        if self.customer_var.get():
            customer_id_match = self.customer_var.get().split("(")
            if len(customer_id_match) > 1:
                customer_id = customer_id_match[-1][:-1]  # Extract ID part

        if not customer_id:
            messagebox.showerror("Error", "Invalid customer selection. Please select a valid customer.")
            return

        check_in = self.check_in_calendar.get_date().strftime("%d/%m/%Y")
        check_out = self.check_out_calendar.get_date().strftime("%d/%m/%Y")
        status = self.status_var.get()
        total_amount = self.total_amount_entry.get()

        if not self.validate_dates_logic(check_in, check_out):
            return

        if not total_amount.isdigit():
            messagebox.showerror("Error", "Total Amount must be a valid integer.")
            return

        try:
            if self.is_edit_mode:
                self.controller.update_reservation(self.current_reservation_id, room_id, customer_id, check_in, check_out, status, total_amount)
            else:
                self.controller.add_reservation(room_id, customer_id, check_in, check_out, status, total_amount)
            self.reset_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def validate_dates_logic(self, check_in, check_out):
        check_in_date = datetime.strptime(check_in, "%d/%m/%Y")
        check_out_date = datetime.strptime(check_out, "%d/%m/%Y")
        if check_out_date < check_in_date:
            messagebox.showerror("Error", "Check-out date cannot be earlier than check-in date.")
            return False
        return True

    def reset_form(self):
        self.room_var.set("")
        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.config(state="readonly")
        self.customer_var.set("")
        self.check_in_calendar.set_date(datetime.today())
        self.check_out_calendar.set_date(datetime.today())
        self.status_var.set("Confirmed")
        self.total_amount_entry.delete(0, tk.END)
        self.add_button.config(text="Add Reservation")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_reservation_id = None

    def create_data_view(self):
        search_frame = tk.Frame(self.data_frame, bg="white")
        search_frame.pack(fill="x", pady=10)

        tk.Label(search_frame, text="Search:", bg="white", font=("Helvetica", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)

        self.search_button = tk.Button(
            search_frame, text="Search", command=self.handle_search,
            bg=self.primary_color, fg="white", font=("Helvetica", 12, "bold"), cursor="hand2"
        )
        self.search_button.pack(side="left", padx=5)

        self.reservation_list = ttk.Treeview(self.data_frame, columns=("id", "room", "customer", "checkIn", "checkOut", "status", "totalAmount"), show="headings")
        self.reservation_list.heading("id", text="ID")
        self.reservation_list.heading("room", text="Room")
        self.reservation_list.heading("customer", text="Customer")
        self.reservation_list.heading("checkIn", text="Check-In")
        self.reservation_list.heading("checkOut", text="Check-Out")
        self.reservation_list.heading("status", text="Status")
        self.reservation_list.heading("totalAmount", text="Total Amount")

        for col in ("id", "room", "customer", "checkIn", "checkOut", "status", "totalAmount"):
            self.reservation_list.column(col, anchor="center", width=100)

        self.reservation_list.bind("<ButtonRelease-1>", self.on_row_click)
        self.reservation_list.pack(fill="both", expand=True, pady=10)

        self.reservation_list.tag_configure('evenrow', background=self.secondary_color)
        self.reservation_list.tag_configure('oddrow', background="white")

        self.update_reservation_list(self.controller.get_all_reservations())

    def handle_search(self):
        keyword = self.search_entry.get()
        reservations = self.controller.search_reservations(keyword)
        self.update_reservation_list(reservations)

    def update_reservation_list(self, reservations):
        
        for i in self.reservation_list.get_children():
            self.reservation_list.delete(i)

        for index, reservation in enumerate(reservations):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            room_no = reservation.get('roomNo', 'N/A')
            customer_name = reservation.get('customer', 'Unknown')
            check_in = reservation.get('checkIn', 'N/A')
            check_out = reservation.get('checkOut', 'N/A')
            status = reservation.get('status', 'N/A')
            total_amount = reservation.get('totalAmount', 'N/A')
            self.reservation_list.insert(
                "", "end", values=(
                    reservation['id'], room_no, customer_name, check_in, check_out, status, total_amount
                ), tags=(tag,)
            )

    def on_row_click(self, event):
        item_id = self.reservation_list.selection()
        if item_id:
            reservation_data = self.reservation_list.item(item_id, "values")
            self.initiate_edit(reservation_data)

    def initiate_edit(self, reservation_data):
        self.current_reservation_id = reservation_data[0]
        self.is_edit_mode = True
        self.add_button.config(text="Update Reservation")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)
        self.room_var.set(reservation_data[1])
        self.customer_var.set(reservation_data[2])
        self.check_in_calendar.set_date(datetime.strptime(reservation_data[3], "%d/%m/%Y"))
        self.check_out_calendar.set_date(datetime.strptime(reservation_data[4], "%d/%m/%Y"))
        self.status_var.set(reservation_data[5])
        self.total_amount_entry.delete(0, tk.END)
        self.total_amount_entry.insert(0, reservation_data[6])
