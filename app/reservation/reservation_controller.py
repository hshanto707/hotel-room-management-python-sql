from app.reservation.reservation_model import ReservationModel
from tkinter import messagebox
from app.session import get_session


class ReservationController:
    def __init__(self, view):
        self.model = ReservationModel()
        self.view = view

    def add_reservation(self, room_id, customer_id, check_in, check_out, status, total_amount):
        # Get userId from session
        session = get_session()
        created_by = session.get("id")

        try:
            self.model.create_reservation(room_id, customer_id, check_in, check_out, status, total_amount, created_by)
            self.refresh_reservation_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def get_all_reservations(self):
        return self.model.fetch_all_reservations()

    def search_reservations(self, keyword):
        return self.model.search_reservations(keyword)

    def update_reservation(self, reservation_id, room_id, customer_id, check_in, check_out, status, total_amount):
        # Get userId from session
        session = get_session()
        created_by = session.get("id")

        self.model.update_reservation(reservation_id, room_id, customer_id, check_in, check_out, status, total_amount, created_by)
        self.refresh_reservation_list()

    def refresh_reservation_list(self):
        reservations = self.model.fetch_all_reservations()
        self.view.update_reservation_list(reservations)

    def get_rooms(self):
        return self.model.fetch_rooms()

    def get_customers(self):
        return self.model.fetch_customers()
