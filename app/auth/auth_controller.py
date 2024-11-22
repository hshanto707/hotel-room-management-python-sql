# app/auth/auth_controller.py

from app.auth.auth_model import AuthModel
from tkinter import messagebox
from app.session import save_session
import re

class AuthController:
    def __init__(self):
        self.model = AuthModel()

    def login(self, email, password):
        # Check if email is valid
        if not re.match(r"[^@]+@gmail\.com$", email):
            raise ValueError("Invalid email. Must be a valid @gmail.com address")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        user_data = self.model.authenticate_user(email, password)
        if user_data:
            # Save user data to session
            save_session(user_data)
            return True
        return False

    def register(self, name, email, password):
        # Check if email is valid and password length is adequate
        if not re.match(r"[^@]+@gmail\.com$", email):
            raise ValueError("Invalid email. Must be a valid @gmail.com address")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        try:
            self.model.register_user(name, email, password)
            return True
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
