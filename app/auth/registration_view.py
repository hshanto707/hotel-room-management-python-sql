import tkinter as tk
from tkinter import messagebox
from app.auth.auth_controller import AuthController

class RegistrationView:
    def __init__(self, root, switch_to_login):
        self.root = root
        self.auth_controller = AuthController()
        self.switch_to_login = switch_to_login

        self.root.title("Registration")
        self.root.geometry("1000x600")

        # Main container frame for split design
        container = tk.Frame(root, bg="white")
        container.pack(fill="both", expand=True)

        # Left frame for the form
        left_frame = tk.Frame(container, bg="white", padx=40, pady=40)
        left_frame.place(relwidth=0.5, relheight=1)

        # Right frame for the welcome message
        right_frame = tk.Frame(container, bg="#ff6e7f", padx=20, pady=20)
        right_frame.place(relx=0.5, relwidth=0.5, relheight=1)

        # Form heading
        tk.Label(left_frame, text="Sign Up", font=("Helvetica", 24), bg="white").pack(pady=(0, 30))

        # Name label and entry
        tk.Label(left_frame, text="Name", bg="white", font=("Helvetica", 12)).pack(anchor='w')
        self.name_entry = tk.Entry(left_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.name_entry.pack(fill="x", pady=10, ipady=5)

        # Username label and entry
        tk.Label(left_frame, text="Username", bg="white", font=("Helvetica", 12)).pack(anchor='w')
        self.username_entry = tk.Entry(left_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.username_entry.pack(fill="x", pady=10, ipady=5)

        # Password label and entry
        tk.Label(left_frame, text="Password", bg="white", font=("Helvetica", 12)).pack(anchor='w')
        self.password_entry = tk.Entry(left_frame, show="*", font=("Helvetica", 14), bd=2, relief="solid")
        self.password_entry.pack(fill="x", pady=10, ipady=5)

        # Register button
        register_button = tk.Button(left_frame, text="Register", bg="#ff6e7f", fg="white", font=("Helvetica", 14, "bold"), command=self.register)
        register_button.pack(pady=20, fill="x", ipady=5)

        # Right frame welcome message
        tk.Label(right_frame, text="Welcome to Registration", font=("Helvetica", 24, "bold"), bg="#ff6e7f", fg="white").pack(pady=(40, 10))
        tk.Label(right_frame, text="Already have an account?", bg="#ff6e7f", fg="white", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(right_frame, text="Sign In", command=self.switch_to_login, bg="white", fg="#ff6e7f", font=("Helvetica", 14, "bold"), relief="flat").pack(pady=10, ipadx=20, ipady=5)

    def register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if name and username and password:
            if self.auth_controller.register(name, username, password):
                messagebox.showinfo("Success", "Registration successful!")
                self.switch_to_login()
            else:
                messagebox.showerror("Error", "Registration failed")
        else:
            messagebox.showerror("Error", "All fields are required")
