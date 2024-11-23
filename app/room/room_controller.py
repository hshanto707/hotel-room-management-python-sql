# controllers/room_controller.py

from app.room.room_model import RoomModel
from tkinter import messagebox
from app.session import get_session

class RoomController:
    def __init__(self, view):
        self.model = RoomModel()
        self.view = view

    def add_room(self, room_no, room_type, price, status, airConditioning):
        # Get userId from session
        session = get_session()
        createdBy = session.get("id")
        
        try:
            self.model.create_room(room_no, room_type, price, status, airConditioning, createdBy)
            self.refresh_room_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    def get_all_rooms(self):
        return self.model.fetch_all_rooms()

    def search_rooms(self, keyword):
        return self.model.search_rooms(keyword)

    def update_room(self, room_id, room_no, room_type, price, status, airConditioning):
        # Get userId from session
        session = get_session()
        createdBy = session.get("id")
        
        self.model.update_room(room_id, room_no, room_type, price, status, airConditioning, createdBy)
        self.refresh_room_list()

    def delete_room(self, room_id):
        self.model.delete_room(room_id)
        self.refresh_room_list()

    def refresh_room_list(self):
        rooms = self.model.fetch_all_rooms()
        self.view.update_room_list(rooms)
