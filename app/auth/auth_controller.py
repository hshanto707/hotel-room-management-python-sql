# app/auth/auth_controller.py

from app.user.user_model import UserModel
from tkinter import messagebox
import re

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, email, password):
        # Check if email is valid
        if not re.match(r"[^@]+@gmail\.com$", email):
            raise ValueError("Invalid email. Must be a valid @gmail.com address")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        return self.user_model.authenticate_user(email, password)

    def register(self, name, email, password):
        # Check if email is valid and password length is adequate
        if not re.match(r"[^@]+@gmail\.com$", email):
            raise ValueError("Invalid email. Must be a valid @gmail.com address")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        try:
            self.user_model.register_user(name, email, password)
            return True
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
