# app/billing/billing_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry  # Import the calendar widget
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

        # Payment Date (Calendar)
        tk.Label(self.form_frame, text="Payment Date:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.payment_date_calendar = DateEntry(self.form_frame, font=("Helvetica", 12), date_pattern="dd/mm/yyyy")
        self.payment_date_calendar.pack(fill="x", pady=10, ipady=5)

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
        self.reservation_dropdown['values'] = [str(r['id']) for r in reservations]
        self.reservation_dropdown.bind("<<ComboboxSelected>>", self.on_reservation_selected)

    def on_reservation_selected(self, event):
        selected_reservation = self.reservation_var.get()
        if not selected_reservation:
            return

        reservation_id = selected_reservation
        reservation_data = self.controller.get_reservation_by_id(reservation_id)
        if reservation_data and 'totalAmount' in reservation_data:
            self.amount_entry.config(state="normal")
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, reservation_data['totalAmount'])
            self.amount_entry.config(state="readonly")
        else:
            messagebox.showerror("Error", "Failed to fetch the amount for the selected reservation.")

    def handle_add_or_update(self):
        reservation = self.reservation_var.get()
        if not reservation:
            messagebox.showerror("Error", "Please select a reservation.")
            return

        reservation_id = reservation
        amount = self.amount_entry.get().strip()
        discount = self.discount_entry.get().strip()
        payment_date = self.payment_date_calendar.get_date().strftime("%d/%m/%Y")
        status = self.status_var.get()

        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Amount must be a valid positive integer.")
            return

        if not discount.isdigit() or int(discount) < 0:
            messagebox.showerror("Error", "Discount must be a valid non-negative integer.")
            return

        if int(discount) > int(amount):
            messagebox.showerror("Error", "Discount cannot be larger than the amount.")
            return

        try:
            if self.is_edit_mode:
                self.controller.update_billing(self.current_billing_id, reservation_id, amount, discount, payment_date, status)
            else:
                self.controller.add_billing(reservation_id, amount, discount, payment_date, status)
            self.update_billing_list(self.controller.get_all_billings())
            self.reset_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_form(self):
        self.reservation_var.set("")
        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.config(state="readonly")
        self.discount_entry.delete(0, tk.END)
        self.payment_date_calendar.set_date(datetime.today())
        self.status_var.set("Confirmed")
        self.add_button.config(text="Add Payment")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_billing_id = None

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

        self.billing_list = ttk.Treeview(self.data_frame, columns=("id", "reservation", "amount", "discount", "paymentDate", "status"), show="headings")
        self.billing_list.heading("id", text="ID")
        self.billing_list.heading("reservation", text="Reservation")
        self.billing_list.heading("amount", text="Amount")
        self.billing_list.heading("discount", text="Discount")
        self.billing_list.heading("paymentDate", text="Payment Date")
        self.billing_list.heading("status", text="Status")

        for col in ("id", "reservation", "amount", "discount", "paymentDate", "status"):
            self.billing_list.column(col, anchor="center", width=100)

        self.billing_list.bind("<ButtonRelease-1>", self.on_row_click)
        self.billing_list.pack(fill="both", expand=True, pady=10)

        self.billing_list.tag_configure('evenrow', background=self.secondary_color)
        self.billing_list.tag_configure('oddrow', background="white")

        self.update_billing_list(self.controller.get_all_billings())

    def handle_search(self):
        keyword = self.search_entry.get()
        billings = self.controller.search_billings(keyword)
        self.update_billing_list(billings)

    def update_billing_list(self, billings):
        for i in self.billing_list.get_children():
            self.billing_list.delete(i)

        for index, billing in enumerate(billings):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.billing_list.insert(
                "", "end", values=(
                    billing['id'],
                    billing['reservationId'],
                    billing['amount'],
                    billing['discount'],
                    billing['paymentDate'],
                    billing['status']
                ), tags=(tag,)
            )

    def on_row_click(self, event):
        item_id = self.billing_list.selection()
        if item_id:
            billing_data = self.billing_list.item(item_id, "values")
            self.initiate_edit(billing_data)

    def initiate_edit(self, billing_data):
        self.current_billing_id = billing_data[0]
        self.is_edit_mode = True
        self.add_button.config(text="Update Payment")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        self.reservation_var.set(billing_data[1])

        self.amount_entry.config(state="normal")
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, billing_data[2])
        self.amount_entry.config(state="readonly")

        self.discount_entry.delete(0, tk.END)
        self.discount_entry.insert(0, billing_data[3])

        self.payment_date_calendar.set_date(datetime.strptime(billing_data[4], "%d/%m/%Y"))
        self.status_var.set(billing_data[5])
