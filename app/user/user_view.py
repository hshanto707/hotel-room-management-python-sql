# app/user/profile_view.py

import tkinter as tk
from tkinter import messagebox
import re
from app.session import get_session, clear_session
from app.user.user_controller import UserController
import bcrypt


class ProfileView:
    def __init__(self, parent, primary_color, secondary_color, session_data=None):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.controller = UserController()

        # Fetch user session data or fallback to session handler
        self.session_data = session_data or get_session()
        self.user_id = self.session_data.get("id", None)
        name = self.session_data.get("name", "")
        email = self.session_data.get("email", "")
        phone = self.session_data.get("phone", "")
        address = self.session_data.get("address", "")

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color, padx=40, pady=40)
        self.frame.place(relx=0.2, relwidth=0.6, relheight=1)

        # Title
        tk.Label(
            self.frame,
            text="Update Profile",
            font=("Helvetica", 18),
            bg=secondary_color,
            fg=primary_color,
        ).pack(pady=20)

        # Name
        tk.Label(self.frame, text="Name", font=("Helvetica", 12), bg=secondary_color, fg=primary_color).pack(anchor="w")
        self.name_entry = tk.Entry(self.frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.name_entry.pack(fill="x", pady=10, ipady=5)
        self.name_entry.insert(0, name)

        # Password
        tk.Label(self.frame, text="Password", font=("Helvetica", 12), bg=secondary_color, fg=primary_color).pack(anchor="w")
        self.password_entry = tk.Entry(self.frame, font=("Helvetica", 12), show="*", bd=2, relief="solid")
        self.password_entry.pack(fill="x", pady=10, ipady=5)

        # Email
        tk.Label(self.frame, text="Email", font=("Helvetica", 12), bg=secondary_color, fg=primary_color).pack(anchor="w")
        self.email_entry = tk.Entry(self.frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.email_entry.pack(fill="x", pady=10, ipady=5)
        self.email_entry.insert(0, email)

        # Phone
        tk.Label(self.frame, text="Phone", font=("Helvetica", 12), bg=secondary_color, fg=primary_color).pack(anchor="w")
        self.phone_entry = tk.Entry(self.frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.phone_entry.pack(fill="x", pady=10, ipady=5)
        self.phone_entry.insert(0, phone if phone != "None" else "")

        # Address
        tk.Label(self.frame, text="Address", font=("Helvetica", 12), bg=secondary_color, fg=primary_color).pack(anchor="w")
        self.address_entry = tk.Entry(self.frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.address_entry.pack(fill="x", pady=10, ipady=5)
        self.address_entry.insert(0, address if address != "None" else "")

        # Save Button
        tk.Button(
            self.frame,
            text="Update",
            command=self.save_profile,
            font=("Helvetica", 14, "bold"),
            bg=primary_color,
            fg="white",
            relief="flat",
            cursor="hand2",
        ).pack(pady=20, fill="x", ipady=5)

    def validate_email(self, email):
        """Validate email using regex."""
        email_regex = r"[^@]+@gmail\.com$"
        if re.match(email_regex, email):
            return True
        return False

    def validate_phone(self, phone):
        """Validate phone number."""
        if len(phone) == 11 and phone.startswith("01") and phone[2] in "3456789" and phone[3:].isdigit():
            return True
        return False

    def save_profile(self):
        name = self.name_entry.get().strip()
        oldPassword = self.session_data.get("password", "")
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        
        hashed_password = ""
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Validate inputs
        if not name or not email or not phone or not address:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number format!")
            return

        try:
            self.controller.save_profile(
                self.user_id, name, hashed_password if hashed_password else oldPassword, email, phone, address
            )
            self.session_data.update({"name": name, "email": email, "phone": phone, "address": address})
            messagebox.showinfo("Success", "Profile updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        # Save the profile details to the database and the session
