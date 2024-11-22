# app/room/room_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from app.room.room_controller import RoomController

class RoomsView:
    def __init__(self, parent, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.is_edit_mode = False  # Track whether we're in "edit" mode
        self.current_room_id = None  # Track room being edited

        # Initialize the controller with a reference to self
        self.controller = RoomController(self)

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

        # Initialize data view but do not load data yet
        self.create_data_view()

    def create_form(self):
        # Form Title
        tk.Label(self.form_frame, text="Add Room", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 16)).pack(pady=10)

        # Room Number with validation for 3-digit numbers
        tk.Label(self.form_frame, text="Room No:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.room_no_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.room_no_entry.pack(fill="x", pady=10, ipady=5)
        self.room_no_entry.bind("<FocusOut>", self.validate_room_no)  # Bind validation on focus out

        # Room Type as radio buttons
        tk.Label(self.form_frame, text="Type:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.type_entry = tk.StringVar(value="Single")  # Default selection and assignment to type_entry
        types = ["Single", "Double", "Suite"]
        for room_type in types:
            tk.Radiobutton(
                self.form_frame, text=room_type, variable=self.type_entry, value=room_type,
                bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12), anchor="w"
            ).pack(anchor="w")

        # Room Price
        tk.Label(self.form_frame, text="Price:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.price_entry = tk.Entry(self.form_frame, font=("Helvetica", 14), bd=2, relief="solid")
        self.price_entry.pack(fill="x", pady=10, ipady=5)

        # Room air conditioning as radio buttons
        tk.Label(self.form_frame, text="Air Conditioning:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.airConditioning_entry = tk.StringVar(value="AC")  # Default value set to "AC"
        conditions = ["AC", "Non AC"]
        for condition in conditions:
            tk.Radiobutton(
                self.form_frame, text=condition, variable=self.airConditioning_entry, value=condition,
                bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12), anchor="w"
            ).pack(anchor="w")

        # Room Status as radio buttons
        tk.Label(self.form_frame, text="Status:", bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12)).pack(anchor="w")
        self.status_entry = tk.StringVar(value="Available")  # Default selection and assignment to status_entry
        statuses = ["Available", "Occupied", "Maintenance"]
        for status in statuses:
            tk.Radiobutton(
                self.form_frame, text=status, variable=self.status_entry, value=status,
                bg=self.secondary_color, fg=self.primary_color, font=("Helvetica", 12), anchor="w"
            ).pack(anchor="w")

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

    def validate_room_no(self, event):
        """Validates that the room number is exactly three digits."""
        room_no = self.room_no_entry.get()
        if not room_no.isdigit() or len(room_no) != 3:
            messagebox.showerror("Invalid Room Number", "Room number must be exactly three digits.")
            self.room_no_entry.focus_set()  # Set focus back to room number entry

    def handle_add_or_update(self):
        room_no = self.room_no_entry.get()
        room_type = self.type_entry.get()
        price = self.price_entry.get()
        status = self.status_entry.get()
        airConditioning = self.airConditioning_entry.get()

        # Validate room number (must be exactly 3 digits) and price (must be > 0)
        if not room_no.isdigit() or len(room_no) != 3:
            messagebox.showerror("Invalid Room Number", "Room number must be exactly three digits.")
            self.room_no_entry.focus_set()
            return

        try:
            price_value = float(price)
            if price_value <= 0:
                messagebox.showerror("Invalid Price", "Price must be a positive number.")
                self.price_entry.focus_set()
                return
        except ValueError:
            messagebox.showerror("Invalid Price", "Price must be a valid number.")
            self.price_entry.focus_set()
            return

        # Try to add or update room and handle any errors that occur
        try:
            if self.is_edit_mode:
                # Update room
                self.controller.update_room(self.current_room_id, room_no, room_type, price, status, airConditioning)
            else:
                # Add new room
                self.controller.add_room(room_no, room_type, price, status, airConditioning)

            # Reset form after successful add/update
            self.reset_form()

        except ValueError as e:
            # Show error message if there’s an issue, like a duplicate room number
            messagebox.showerror("Error", str(e))

    def reset_form(self):
        """Resets the form to add mode and clears entries"""
        self.room_no_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

        # Reset the StringVar values for type and status
        self.type_entry.set("Single")  # Reset to default value
        self.status_entry.set("Available")  # Reset to default value
        self.airConditioning_entry.set("AC")  # Reset to default value

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
        self.room_list = ttk.Treeview(self.data_frame, columns=("roomNo", "type", "price", "status", "airConditioning", "actions"), show="headings")
        self.room_list.heading("roomNo", text="Room No")
        self.room_list.heading("type", text="Type")
        self.room_list.heading("price", text="Price")
        self.room_list.heading("status", text="Status")
        self.room_list.heading("airConditioning", text="Air Conditioning")
        self.room_list.heading("actions", text="Actions")

        # Set column widths and center-align
        for col in ("roomNo", "type", "price", "status", "airConditioning"):
            self.room_list.column(col, anchor="center", width=100)
        self.room_list.column("actions", anchor="center", width=150)

        # Bind single-click event for action handling
        self.room_list.bind("<Button-1>", self.on_single_click)

        # Pack room list table
        self.room_list.pack(fill="both", expand=True, pady=10)

        # Apply custom styles for alternating row colors
        self.room_list.tag_configure('evenrow', background=self.secondary_color)
        self.room_list.tag_configure('oddrow', background="white")

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

        # Insert new data into room list with alternating row colors
        for index, room in enumerate(rooms):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.room_list.insert(
                "", "end", values=(room['roomNo'], room['type'], room['price'], room['status'], room['airConditioning'], "Edit | Delete"), tags=(tag,)
            )

    def on_single_click(self, event):
        # Identify the row and column where the click occurred
        item_id = self.room_list.identify_row(event.y)
        column_id = self.room_list.identify_column(event.x)

        if item_id and column_id == '#6':  # '#6' corresponds to the "actions" column
            room_data = self.room_list.item(item_id, "values")
            room_id = room_data[0]  # Assuming room ID is in the first column

            # Get the x-coordinate within the actions column to determine if "Edit" or "Delete" was clicked
            x_offset = event.x - self.room_list.bbox(item_id, column_id)[0]

            # Assuming "Edit" is on the left half and "Delete" on the right half of the actions cell
            if x_offset < 75:  # Approximate midpoint of 150 width
                self.initiate_edit(room_data)
            else:
                self.delete_room(room_data)

    def initiate_edit(self, room_data):
        self.current_room_id = room_data[0]
        self.is_edit_mode = True
        self.add_button.config(text="Update Room")
        self.cancel_button.pack(pady=10, fill="x", ipady=5)

        # Populate form fields
        self.room_no_entry.delete(0, tk.END)
        self.room_no_entry.insert(0, room_data[0])

        # Set the value for type_entry (using set since it's a StringVar)
        self.type_entry.set(room_data[1])

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, room_data[2])

        # Set the value for status_entry (using set since it's a StringVar)
        self.status_entry.set(room_data[3])

        # Set the value for airConditioning_entry (using set since it's a StringVar)
        self.airConditioning_entry.set(room_data[4])

    def delete_room(self, room_data):
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this room?")
        if response:
            self.controller.delete_room(room_data[0])  # Delete by room ID
            self.update_room_list(self.controller.get_all_rooms())
