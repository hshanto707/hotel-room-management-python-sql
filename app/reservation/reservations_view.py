import tkinter as tk

class ReservationsView:
    def __init__(self, parent, primary_color, secondary_color):
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)
        
        tk.Label(
            self.frame, text="Reservation Management Section", bg=secondary_color, 
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=20)
