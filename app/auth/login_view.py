import tkinter as tk
from tkinter import messagebox
from tkinter import font
from app.auth.auth_controller import AuthController

class LoginView:
    def __init__(self, root, switch_to_registration, switch_to_dashboard):
        self.root = root
        self.auth_controller = AuthController()
        self.switch_to_registration = switch_to_registration
        self.switch_to_dashboard = switch_to_dashboard

        self.root.title("Login")
        self.root.geometry("1000x600")
        
        # Main container frame for the split design
        container = tk.Frame(root, bg="white")
        container.pack(fill="both", expand=True)

        # Left frame for the form
        left_frame = tk.Frame(container, bg="white", padx=40, pady=40)
        left_frame.place(relwidth=0.5, relheight=1)

        # Right frame for the welcome message
        right_frame = tk.Frame(container, bg="#ff6e7f", padx=20, pady=20)
        right_frame.place(relx=0.5, relwidth=0.5, relheight=1)

        # Form heading
        tk.Label(left_frame, text="Sign In", font=("Helvetica", 24), bg="white").pack(pady=(0, 30))

        # Username label and entry
        tk.Label(left_frame, text="Username", bg="white", font=("Helvetica", 12)).pack(anchor='w')
        self.username_entry = tk.Entry(left_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.username_entry.pack(fill="x", pady=10, ipady=5)

        # Password label and entry
        tk.Label(left_frame, text="Password", bg="white", font=("Helvetica", 12)).pack(anchor='w')
        self.password_entry = tk.Entry(left_frame, show="*", font=("Helvetica", 14), bd=2, relief="solid")
        self.password_entry.pack(fill="x", pady=10, ipady=5)

        # Login Button
        login_button = tk.Button(left_frame, text="Sign In", bg="#ff6e7f", fg="white", font=("Helvetica", 14, "bold"), command=self.login)
        login_button.pack(pady=20, fill="x", ipady=5)

        # Right Frame Welcome Message
        tk.Label(right_frame, text="Welcome to Login", font=("Helvetica", 24, "bold"), bg="#ff6e7f", fg="white").pack(pady=(40, 10))
        tk.Label(right_frame, text="Don't have an account?", bg="#ff6e7f", fg="white", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(right_frame, text="Sign Up", command=self.switch_to_registration, bg="white", fg="#ff6e7f", font=("Helvetica", 14, "bold"), relief="flat").pack(pady=10, ipadx=20, ipady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.login(username, password):
            self.switch_to_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")
