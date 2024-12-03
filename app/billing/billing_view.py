# app/room/billing_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.billing.billing_controller import BillingController


class BillingView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False
        self.current_billing_id = None

        self.controller = BillingController(self)

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.frame, text="Billing Management Section", bg=secondary_color,
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=10)

        # Left Frame (30%) - Billing Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()

        # Right Frame (70%) - Billing List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)

        self.create_data_view()

    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Payments", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        # Reservation Dropdown
        tk.Label(self.form_frame, text="Reservation:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.reservation_var = tk.StringVar()
        self.reservation_dropdown = ttk.Combobox(self.form_frame, textvariable=self.reservation_var, state="readonly", font=("Helvetica", 12))
        self.reservation_dropdown.pack(fill="x", pady=10, ipady=5)
        self.load_reservations()

        # Amount
        tk.Label(self.form_frame, text="Amount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.amount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid", state="readonly")
        self.amount_entry.pack(fill="x", pady=10, ipady=5)

        # Discount
        tk.Label(self.form_frame, text="Discount:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.discount_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.discount_entry.pack(fill="x", pady=10, ipady=5)

        # Payment Date
        tk.Label(self.form_frame, text="Payment Date (dd/mm/yyyy):", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.payment_date_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.payment_date_entry.pack(fill="x", pady=10, ipady=5)

        # Status Radio Buttons
        tk.Label(self.form_frame, text="Status:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.status_var = tk.StringVar(value="Confirmed")  # Default to "Confirmed"
        statuses = ["Confirmed", "Cancelled", "Pending"]
        for status in statuses:
            tk.Radiobutton(
                self.form_frame, text=status, variable=self.status_var, value=status,
                bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12), anchor="w"
            ).pack(anchor="w")

        # Action Buttons
        self.add_button = tk.Button(
            self.form_frame, text="Add Payment", font=("Helvetica", 14, "bold"),
            bg=self.primary_color, fg="white", relief="flat", command=self.handle_add_or_update, cursor="hand2"
        )
        self.add_button.pack(pady=20, fill="x", ipady=5)

        # Cancel Button (initially hidden)
        self.cancel_button = tk.Button(
            self.form_frame, text="Cancel", font=("Helvetica", 12),
            bg="grey", fg="white", relief="flat", command=self.reset_form, cursor="hand2"
        )
        self.cancel_button.pack(pady=10, fill="x", ipady=5)
        self.cancel_button.pack_forget()

    def load_reservations(self):
        reservations = self.controller.get_reservations()
        self.reservation_dropdown['values'] = [f"{r['id']} - {r['totalAmount']}" for r in reservations]
        self.reservation_dropdown.bind("<<ComboboxSelected>>", self.on_reservation_selected)

    def on_reservation_selected(self, event):
        """
        Fetch and display the amount for the selected reservation in the amount field.
        """
        selected_reservation = self.reservation_var.get()
        
        if not selected_reservation:
            return

        # Extract reservation ID from the dropdown selection
        reservation_id = selected_reservation.split(" - ")[0]

        # Fetch reservation details using the controller
        reservation_data = self.controller.get_reservation_by_id(reservation_id)
        
        if reservation_data and 'totalAmount' in reservation_data:
            # Set the amount field to the reservation's total amount
            self.amount_entry.config(state="normal")  # Enable editing temporarily to set the value
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, reservation_data['totalAmount'])
            self.amount_entry.config(state="readonly")  # Make it readonly again
        else:
            messagebox.showerror("Error", "Failed to fetch the amount for the selected reservation.")

    def handle_add_or_update(self):
        reservation = self.reservation_var.get()
        if not reservation:
            messagebox.showerror("Error", "Please select a reservation.")
            return

        reservation_id = reservation.split(" - ")[0]
        amount = self.amount_entry.get().strip()
        discount = self.discount_entry.get().strip()
        payment_date = self.payment_date_entry.get().strip()
        status = self.status_var.get()

        # Validate amount
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Amount must be a valid positive integer.")
            return

        # Validate discount
        if not discount.isdigit() or int(discount) < 0:
            messagebox.showerror("Error", "Discount must be a valid non-negative integer.")
            return

        if int(discount) > int(amount):
            messagebox.showerror("Error", "Discount cannot be larger than the amount.")
            return

        # Validate payment date
        if not self.validate_date(payment_date):
            messagebox.showerror("Error", "Invalid payment date format. Use dd/mm/yyyy.")
            return

        try:
            # Perform the add or update operation
            if self.is_edit_mode:
                self.controller.update_billing(self.current_billing_id, reservation_id, amount, discount, payment_date, status)
            else:
                self.controller.add_billing(reservation_id, amount, discount, payment_date, status)

            # Refresh the billing list after add/update
            self.update_billing_list(self.controller.get_all_billings())

            # Reset the form
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def validate_date(self, date_string):
        """
        Validates that a date is in dd/mm/yyyy format and within valid ranges:
        - dd: 01-31
        - mm: 01-12
        - yyyy: 2000 or later
        """
        try:
            day, month, year = map(int, date_string.split('/'))
            if not (1 <= day <= 31):
                raise ValueError("Day must be between 01 and 31.")
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 01 and 12.")
            if not (year >= 2000):
                raise ValueError("Year must be 2000 or later.")
            # Check if it's a valid calendar date (e.g., handles leap years)
            datetime(year, month, day)
            return True
        except (ValueError, IndexError):
            return False


    def reset_form(self):
        """Reset all form fields to their default state."""
        self.reservation_var.set("")
        self.amount_entry.config(state="normal")  # Temporarily enable to clear the field
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.config(state="readonly")  # Set it back to readonly
        self.discount_entry.delete(0, tk.END)
        self.payment_date_entry.delete(0, tk.END)
        self.status_var.set("Confirmed")
        self.add_button.config(text="Add Payment")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_billing_id = None


    def create_data_view(self):
        # Search Bar Frame
        search_frame = tk.Frame(self.data_frame, bg="white")
        search_frame.pack(fill="x", pady=10)

        # Search Label and Entry
        tk.Label(search_frame, text="Search:", bg="white", font=("Helvetica", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)

        # Search Button
        self.search_button = tk.Button(
            search_frame, text="Search", command=self.handle_search,
            bg=self.primary_color, fg="white", font=("Helvetica", 12, "bold"), cursor="hand2"
        )
        self.search_button.pack(side="left", padx=5)

        # Billing List Table
        self.billing_list = ttk.Treeview(self.data_frame, columns=("id", "reservation", "amount", "discount", "paymentDate", "status", "actions"), show="headings")
        self.billing_list.heading("id", text="ID")
        self.billing_list.heading("reservation", text="Reservation")
        self.billing_list.heading("amount", text="Amount")
        self.billing_list.heading("discount", text="Discount")
        self.billing_list.heading("paymentDate", text="Payment Date")
        self.billing_list.heading("status", text="Status")
        self.billing_list.heading("actions", text="Actions")

        for col in ("id", "reservation", "amount", "discount", "paymentDate", "status"):
            self.billing_list.column(col, anchor="center", width=100)
        self.billing_list.column("actions", anchor="center", width=150)

        self.billing_list.bind("<Button-1>", self.on_single_click)
        self.billing_list.pack(fill="both", expand=True, pady=10)

        self.billing_list.tag_configure('evenrow', background=self.secondary_color)
        self.billing_list.tag_configure('oddrow', background="white")

        self.update_billing_list(self.controller.get_all_billings())


    def handle_search(self):
        keyword = self.search_entry.get()
        billings = self.controller.search_billings(keyword)
        self.update_billing_list(billings)

    def update_billing_list(self, billings):
        """Update the table view with the provided billing records."""
        # Clear the current data in the billing list
        for i in self.billing_list.get_children():
            self.billing_list.delete(i)

        # Insert new data into the billing list with alternating row colors
        for index, billing in enumerate(billings):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.billing_list.insert(
                "", "end", values=(
                    billing['id'],  # Billing ID
                    billing['reservationId'],  # Reservation ID
                    billing['amount'],  # Amount
                    billing['discount'],  # Discount
                    billing['paymentDate'],  # Payment Date
                    billing['status'],  # Status
                    "Edit"  # Action
                ), tags=(tag,)
            )


    def on_single_click(self, event):
        item_id = self.billing_list.identify_row(event.y)
        column_id = self.billing_list.identify_column(event.x)

        if item_id and column_id == '#7':  # '#7' is the actions column
            billing_data = self.billing_list.item(item_id, "values")
            self.initiate_edit(billing_data)

    def initiate_edit(self, billing_data):
        """Populate the form with the selected billing data for editing."""
        self.current_billing_id = billing_data[0]
        self.is_edit_mode = True
        self.add_button.config(text="Update Payment")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        # Populate form fields
        reservation_display = f"{billing_data[1]} - {billing_data[2]}"  # Assuming 2nd column is reservation ID
        self.reservation_var.set(reservation_display)

        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, billing_data[2])
        self.amount_entry.config(state="readonly")

        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, billing_data[3])

        self.payment_date_entry.delete(0, tk.END)
        self.payment_date_entry.insert(0, billing_data[4])

        self.status_var.set(billing_data[5])


