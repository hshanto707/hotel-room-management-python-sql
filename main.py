from tkinter import Tk
from app.auth.login_view import LoginView
from app.dashboard.dashboard_view import DashboardView
from app.auth.registration_view import RegistrationView

class App:
    def __init__(self, root):
        self.root = root
        # Main Code
        
        # self.show_login()
        
        # Debug Purpose start
        
        self.show_dashboard()
        
        # Debug Purpose end

    def show_login(self):
        # Clear the root frame for new view
        for widget in self.root.winfo_children():
            widget.destroy()
        # Initialize login view and pass the callback to show the dashboard
        LoginView(self.root, self.show_registration, self.show_dashboard)

    def show_dashboard(self):
        # Clear the root frame for new view
        for widget in self.root.winfo_children():
            widget.destroy()
        # Initialize dashboard view and pass the callbacks for logout
        DashboardView(self.root, self.show_login)

    def show_registration(self):
        # Clear the root frame for new view
        for widget in self.root.winfo_children():
            widget.destroy()
        # Initialize registration view (similar to login view)
        RegistrationView(self.root, self.show_login)

    def show_profile(self):
        # Clear the root frame for new view
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
