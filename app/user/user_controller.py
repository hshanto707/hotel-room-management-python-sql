# app/user/user_controller.py

from app.user.user_model import UserModel
from tkinter import messagebox
import re


class UserController:
    def __init__(self):
        self.model = UserModel()

    def validate_email(self, email):
        """Validate email format."""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    def validate_phone(self, phone):
        """Validate phone number format."""
        if len(phone) == 11 and phone.startswith("01") and phone[2] in "3456789" and phone[3:].isdigit():
            return True
        return False

    def save_profile(self, user_id, name, password, email, phone, address):
        """Save user profile after validation."""
        if not name or not password or not email or not phone or not address:
            raise ValueError("All fields are required.")

        if not self.validate_email(email):
            raise ValueError("Invalid email format.")

        if not self.validate_phone(phone):
            raise ValueError("Invalid phone number format.")

        # Hash the password (optional, but recommended)
        hashed_password = self.model.hash_password(password)

        # Update the profile in the database
        self.model.update_user(user_id, name, hashed_password, email, phone, address)
        return "Profile updated successfully!"
