# app/room/billing_controller.py

from app.billing.billing_model import BillingModel
from tkinter import messagebox


class BillingController:
    def __init__(self, view):
        self.model = BillingModel()
        self.view = view

    def get_all_billings(self):
        """Fetch all billing records."""
        return self.model.fetch_all_billings()

    def search_billings(self, keyword):
        """Search billings based on a keyword."""
        return self.model.search_billings(keyword)

    def get_reservations(self):
        return self.model.fetch_reservations()

    def get_reservation_by_id(self, reservation_id):
        return self.model.fetch_reservation_by_id(reservation_id)

    def add_billing(self, reservation_id, amount, discount, payment_date, status):
        try:
            self.model.create_billing(reservation_id, amount, discount, payment_date, status)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_billing(self, billing_id, reservation_id, amount, discount, payment_date, status):
        try:
            self.model.update_billing(billing_id, reservation_id, amount, discount, payment_date, status)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
