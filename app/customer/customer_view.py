# app/customer/customer_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from app.customer.customer_controller import CustomerController

class CustomersView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False
        self.current_customer_id = None

        self.controller = CustomerController(self)

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.frame, text="Customer Management Section", bg=secondary_color,
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=10)

        # Left Frame (30%) - Customer Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()

        # Right Frame (70%) - Customer List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)

        self.create_data_view()

    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Add Customer", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        # Name
        tk.Label(self.form_frame, text="Name:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.name_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.name_entry.pack(fill="x", pady=10, ipady=5)

        # Email
        tk.Label(self.form_frame, text="Email:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.email_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.email_entry.pack(fill="x", pady=10, ipady=5)

        # Phone
        tk.Label(self.form_frame, text="Phone:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.phone_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.phone_entry.pack(fill="x", pady=10, ipady=5)

        # Address
        tk.Label(self.form_frame, text="Address:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.address_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.address_entry.pack(fill="x", pady=10, ipady=5)

        # Action Buttons
        self.add_button = tk.Button(
            self.form_frame, text="Add Customer", font=("Helvetica", 14, "bold"),
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

    def handle_add_or_update(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if not name or not email or not phone or not address:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            if self.is_edit_mode:
                self.controller.update_customer(self.current_customer_id, name, email, phone, address)
            else:
                self.controller.add_customer(name, email, phone, address)
            self.reset_form()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reset_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

        self.add_button.config(text="Add Customer")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_customer_id = None

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

        # Customer List Table
        self.customer_list = ttk.Treeview(self.data_frame, columns=("id", "name", "email", "phone", "address", "actions"), show="headings")
        self.customer_list.heading("id", text="ID")
        self.customer_list.heading("name", text="Name")
        self.customer_list.heading("email", text="Email")
        self.customer_list.heading("phone", text="Phone")
        self.customer_list.heading("address", text="Address")
        self.customer_list.heading("actions", text="Actions")

        for col in ("id", "name", "email", "phone", "address"):
            self.customer_list.column(col, anchor="center", width=100)
        self.customer_list.column("actions", anchor="center", width=150)

        self.customer_list.bind("<Button-1>", self.on_single_click)
        self.customer_list.pack(fill="both", expand=True, pady=10)

        self.customer_list.tag_configure('evenrow', background=self.secondary_color)
        self.customer_list.tag_configure('oddrow', background="white")

        self.update_customer_list(self.controller.get_all_customers())

    def handle_search(self):
        keyword = self.search_entry.get()
        customers = self.controller.search_customers(keyword)
        self.update_customer_list(customers)

    def update_customer_list(self, customers):
        for i in self.customer_list.get_children():
            self.customer_list.delete(i)

        for index, customer in enumerate(customers):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.customer_list.insert(
                "", "end", values=(customer['Id'], customer['name'], customer['email'], customer['phone'], customer['address'], "Edit"), tags=(tag,)
            )

    def on_single_click(self, event):
        item_id = self.customer_list.identify_row(event.y)
        column_id = self.customer_list.identify_column(event.x)

        if item_id and column_id == '#6':
            customer_data = self.customer_list.item(item_id, "values")
            self.initiate_edit(customer_data)

    def initiate_edit(self, customer_data):
        self.current_customer_id = customer_data[0]
        self.is_edit_mode = True
        self.add_button.config(text="Update Customer")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, customer_data[1])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, customer_data[2])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, customer_data[3])

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, customer_data[4])