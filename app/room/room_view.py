# view/rooms_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from app.room.room_controller import RoomController

class RoomsView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False  # Track whether we're in "edit" mode
        self.current_room_id = None  # Track room being edited
        self.controller = RoomController()

        # Main Frame
        self.frame = tk.Frame(parent, bg=secondary_color)
        self.frame.pack(fill="both", expand=True)

        # Title
        tk.Label(
            self.frame, text="Room Management Section", bg=secondary_color, 
            fg=primary_color, font=("Helvetica", 18)
        ).pack(pady=10)

        # Left Frame (30%) - Room Form
        self.form_frame = tk.Frame(self.frame, bg=secondary_color, padx=40, pady=40)
        self.form_frame.place(relwidth=0.35, relheight=1)
        self.create_form()

        # Right Frame (70%) - Room List and Search
        self.data_frame = tk.Frame(self.frame, bg="white", padx=20, pady=20)
        self.data_frame.place(relx=0.35, relwidth=0.65, relheight=1)
        self.create_data_view()

    def set_controller(self, controller):
        """ Set the controller for this view and load initial data """
        self.controller = controller
        self.update_room_list(self.controller.get_all_rooms())

    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Add Room", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        # Room Number
        tk.Label(self.form_frame, text="Room No:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.room_no_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.room_no_entry.pack(fill="x", pady=10, ipady=5)

        # Room Type
        tk.Label(self.form_frame, text="Type:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.type_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.type_entry.pack(fill="x", pady=10, ipady=5)

        # Room Price
        tk.Label(self.form_frame, text="Price:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.price_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.price_entry.pack(fill="x", pady=10, ipady=5)

        # Room Status
        tk.Label(self.form_frame, text="Status:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.status_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.status_entry.pack(fill="x", pady=10, ipady=5)

        # Action Buttons
        self.add_button = tk.Button(
            self.form_frame, text="Add Room", font=("Helvetica", 14, "bold"), 
            bg=self.primary_color, fg="white", relief="flat", command=self.handle_add_or_update, cursor="hand2"
        )
        self.add_button.pack(pady=20, fill="x", ipady=5)

        # Cancel Button (initially hidden)
        self.cancel_button = tk.Button(
            self.form_frame, text="Cancel", font=("Helvetica", 12),
            bg="grey", fg="white", relief="flat", command=self.reset_form, cursor="hand2"
        )
        self.cancel_button.pack(pady=10, fill="x", ipady=5)
        self.cancel_button.pack_forget()

    def handle_add_or_update(self):
        room_no = self.room_no_entry.get()
        room_type = self.type_entry.get()
        price = self.price_entry.get()
        status = self.status_entry.get()

        if self.is_edit_mode:
            # Update room
            self.controller.update_room(self.current_room_id, room_no, room_type, price, status)
            self.reset_form()
        else:
            # Add new room
            self.controller.add_room(room_no, room_type, price, status)

    def reset_form(self):
        """ Resets the form to add mode and clears entries """
        self.room_no_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.add_button.config(text="Add Room")
        self.cancel_button.pack_forget()
        self.is_edit_mode = False
        self.current_room_id = None

    def create_data_view(self):
        # Search Bar Frame
        search_frame = tk.Frame(self.data_frame, bg="white")
        search_frame.pack(fill="x", pady=10)
        
        # Search Label and Entry
        tk.Label(search_frame, text="Search:", bg="white", font=("Helvetica", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, font=("Helvetica", 12), bd=2, relief="solid")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)
        
        # Search Button
        self.search_button = tk.Button(
            search_frame, text="Search", command=self.handle_search, 
            bg=self.primary_color, fg="white", font=("Helvetica", 12, "bold"), cursor="hand2"
        )
        self.search_button.pack(side="left", padx=5)

        # Room List Table
        self.room_list = ttk.Treeview(self.data_frame, columns=("roomNo", "type", "price", "status", "actions"), show="headings")
        self.room_list.heading("roomNo", text="Room No")
        self.room_list.heading("type", text="Type")
        self.room_list.heading("price", text="Price")
        self.room_list.heading("status", text="Status")
        self.room_list.heading("actions", text="Actions")

        # Set column widths and center-align
        for col in ("roomNo", "type", "price", "status", "actions"):
            self.room_list.column(col, anchor="center", width=100)

        # Pack room list table
        self.room_list.pack(fill="both", expand=True, pady=10)

        # Load all data on page load
        self.update_room_list(self.controller.get_all_rooms())

    def handle_search(self):
        keyword = self.search_entry.get()
        rooms = self.controller.search_rooms(keyword)
        self.update_room_list(rooms)

    def update_room_list(self, rooms):
        # Clear current data in room list
        for i in self.room_list.get_children():
            self.room_list.delete(i)
        
        # Insert new data into room list with Edit and Delete buttons
        for room in rooms:
            room_id = room['Id']
            self.room_list.insert("", "end", values=(room['roomNo'], room['type'], room['price'], room['status'], ""))
            btn_edit = tk.Button(self.room_list, text="Edit", command=lambda r=room: self.initiate_edit(r), cursor="hand2")
            btn_delete = tk.Button(self.room_list, text="Delete", command=lambda r=room: self.delete_room(r), cursor="hand2")
            self.room_list.set("", 'end', btn_edit, btn_delete)

    def initiate_edit(self, room):
        response = messagebox.askyesno("Confirm Edit", "Are you sure you want to edit this room?")
        if response:
            self.current_room_id = room['Id']
            self.is_edit_mode = True
            self.add_button.config(text="Update Room")
            self.cancel_button.pack(pady=10, fill="x", ipady=5)
            self.room_no_entry.delete(0, tk.END)
            self.room_no_entry.insert(0, room['roomNo'])
            self.type_entry.delete(0, tk.END)
            self.type_entry.insert(0, room['type'])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, room['price'])
            self.status_entry.delete(0, tk.END)
            self.status_entry.insert(0, room['status'])

    def delete_room(self, room):
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this room?")
        if response:
            self.controller.delete_room(room['Id'])
