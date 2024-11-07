import tkinter as tk
from tkinter import messagebox

class ProfileView:
    def __init__(self, root, switch_to_dashboard):
        self.root = root
        self.switch_to_dashboard = switch_to_dashboard

        self.root.title("Profile")
        self.root.geometry("400x300")

        # Profile form for updating details
        tk.Label(root, text="Update Profile", font=("Helvetica", 18)).pack(pady=20)

        tk.Label(root, text="Name", font=("Helvetica", 12)).pack(anchor='w', padx=20)
        self.name_entry = tk.Entry(root, font=("Helvetica", 12))
        self.name_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(root, text="Username", font=("Helvetica", 12)).pack(anchor='w', padx=20)
        self.username_entry = tk.Entry(root, font=("Helvetica", 12))
        self.username_entry.pack(fill="x", padx=20, pady=5)

        tk.Label(root, text="Password", font=("Helvetica", 12)).pack(anchor='w', padx=20)
        self.password_entry = tk.Entry(root, font=("Helvetica", 12), show="*")
        self.password_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(root, text="Save Changes", command=self.save_profile, font=("Helvetica", 12, "bold")).pack(pady=20)

        tk.Button(root, text="Back to Dashboard", command=self.switch_to_dashboard, font=("Helvetica", 12)).pack(pady=5)

    def save_profile(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Here, you would add the logic to save the profile details to the database.
        if name and username and password:
            messagebox.showinfo("Success", "Profile updated successfully!")
        else:
            messagebox.showerror("Error", "All fields are required!")
