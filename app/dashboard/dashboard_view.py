# app/dashboard/dashboard_view.py

import tkinter as tk
from tkinter import ttk, messagebox, font
from app.config import PRIMARY_COLOR, SECONDARY_COLOR, APP_NAME
from ..room.room_view import RoomsView
from ..customer.customers_view import CustomersView
from ..reservation.reservations_view import ReservationsView
from ..billing.billing_view import BillingView
from app.user.profile_view import ProfileView

class DashboardView:
    def __init__(self, root, switch_to_login):
        self.root = root
        self.switch_to_login = switch_to_login

        # Configure main window
        self.root.title(APP_NAME)
        self.root.geometry("1024x768")

        # Main Frame
        main_frame = tk.Frame(self.root, bg=SECONDARY_COLOR)
        main_frame.pack(fill="both", expand=True)

        # Header
        self.create_header(main_frame)

        # Sidebar
        self.create_sidebar(main_frame)

        # Content Area
        self.content_frame = tk.Frame(main_frame, bg=SECONDARY_COLOR)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Show the home page by default
        self.show_homepage()

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=PRIMARY_COLOR, height=80)
        header_frame.pack(fill="x", side="top")
        
        # Title as a button to return to the homepage
        title_label = tk.Label(
            header_frame, text=APP_NAME, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, 
            font=("Helvetica", 18, "bold"), cursor="hand2"
        )
        title_label.pack(side="left", padx=20, pady=10)
        title_label.bind("<Button-1>", lambda e: self.show_homepage())  # Click to return to homepage
        
        # Greetings
        profile_label = tk.Label(
            header_frame, text="Hello User!", bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, 
            font=("Helvetica", 12)
        )
        profile_label.pack(side="right", padx=20, pady=10)

        # Bottom border for the header
        tk.Frame(parent, height=2, bg=SECONDARY_COLOR).pack(fill="x")

    def create_sidebar(self, parent):
        sidebar_frame = tk.Frame(parent, bg=PRIMARY_COLOR, width=200)
        sidebar_frame.pack(fill="y", side="left")

        # Sidebar options
        options = [
            ("Rooms", self.load_rooms_page),
            ("Customers", self.load_customers_page),
            ("Reservations", self.load_reservations_page),
            ("Billing", self.load_billing_page)
        ]

        for option, command in options:
            button = tk.Button(
                sidebar_frame, text=option, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, 
                font=("Helvetica", 14), relief="flat", cursor="hand2",
                command=command
            )
            button.pack(fill="x", padx=20, pady=5)

            # Divider between options
            tk.Frame(sidebar_frame, height=1, bg=SECONDARY_COLOR).pack(fill="x", padx=5)

        # Space to push profile/logout buttons to the bottom
        sidebar_frame.pack_propagate(False)
        tk.Frame(sidebar_frame, height=300, bg=PRIMARY_COLOR).pack(fill="x")

        # Logout Button at the bottom of the sidebar
        logout_button = tk.Button(
            sidebar_frame, text="Logout", bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, 
            font=("Helvetica", 14), relief="flat", cursor="hand2", 
            command=self.logout
        )
        logout_button.pack(fill="x", padx=20, pady=5, side="bottom")
        
        # Divider between options
        divider = tk.Frame(sidebar_frame, height=1, bg=SECONDARY_COLOR)
        divider.pack(fill="x", padx=20, side="bottom")

        # Profile Button at the bottom of the sidebar
        profile_button = tk.Button(
            sidebar_frame, text="Profile", bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, 
            font=("Helvetica", 14), relief="flat", cursor="hand2", 
            command=self.load_profile_page
        )
        profile_button.pack(fill="x", padx=20, pady=5, side="bottom")

    def show_homepage(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Welcome message on the homepage
        welcome_label = tk.Label(
            self.content_frame, text="Welcome to the Hotel Room Management Dashboard",
            bg=SECONDARY_COLOR, fg=PRIMARY_COLOR, font=("Helvetica", 20, "bold")
        )
        welcome_label.pack(pady=50)

    def load_rooms_page(self):
        self.load_page(RoomsView)

    def load_customers_page(self):
        self.load_page(CustomersView)

    def load_reservations_page(self):
        self.load_page(ReservationsView)

    def load_billing_page(self):
        self.load_page(BillingView)

    def load_profile_page(self):
        self.load_page(ProfileView)
    
    def load_page(self, page_class):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Instantiate the page view in the content frame
        page_class(self.content_frame, PRIMARY_COLOR, SECONDARY_COLOR)


    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            self.switch_to_login()
