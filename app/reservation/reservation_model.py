# app/reservation/reservation_model.py

from pymysql.cursors import DictCursor
from app.database import Database


class ReservationModel:
    def __init__(self):
        self.conn = Database.connect()
        if self.conn is None:
            raise Exception("Failed to connect to the database")
        self.cursor = self.conn.cursor(DictCursor)

    def create_reservation(self, room_id, customer_id, check_in, check_out, status, total_amount, created_by):
        # Check for duplicate reservations (same room and overlapping dates)
        overlap_query = """
        SELECT COUNT(*) as count
        FROM reservations
        WHERE roomId = %s AND (
            (checkIn <= %s AND checkOut >= %s) OR
            (checkIn <= %s AND checkOut >= %s)
        )
        """
        self.cursor.execute(overlap_query, (room_id, check_in, check_in, check_out, check_out))
        result = self.cursor.fetchone()
        if result['count'] > 0:
            raise ValueError("Room is already booked for the selected dates.")

        # Insert the reservation
        query = """
        INSERT INTO reservations (roomId, customerId, checkIn, checkOut, status, totalAmount, createdBy)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (room_id, customer_id, check_in, check_out, status, total_amount, created_by))
        self.conn.commit()

    def fetch_all_reservations(self):
        query = """
        SELECT r.id, ro.id as roomId, ro.roomNo, ro.price, r.customerId, c.name as customer, r.checkIn, r.checkOut, r.status, r.totalAmount
        FROM reservations r
        JOIN customers c ON r.customerId = c.id
        JOIN rooms ro ON r.roomId = ro.id
        ORDER BY r.id DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_reservations(self, keyword):
        query = """
        SELECT r.id, r.roomId, c.name as customer, r.checkIn, r.checkOut, r.status, r.totalAmount
        FROM reservations r
        JOIN customers c ON r.customerId = c.id
        WHERE r.roomId LIKE %s OR c.name LIKE %s OR r.status LIKE %s
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(query, (keyword, keyword, keyword))
        return self.cursor.fetchall()

    def update_reservation(self, reservation_id, room_id, customer_id, check_in, check_out, status, total_amount, created_by):
        # Update reservation
        query = """
        UPDATE reservations
        SET roomId = %s, customerId = %s, checkIn = %s, checkOut = %s, status = %s, totalAmount = %s, createdBy = %s
        WHERE id = %s
        """
        self.cursor.execute(query, (room_id, customer_id, check_in, check_out, status, total_amount, created_by, reservation_id))
        self.conn.commit()

    def fetch_rooms(self):
        """
        Fetch all rooms with room number, ID, and price.
        """
        query = "SELECT id, roomNo, price FROM rooms"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_room_by_id(self, room_id):
        """Fetch a single room's details, including the total amount."""
        query = "SELECT id, price FROM rooms WHERE id = %s"
        self.cursor.execute(query, (room_id,))
        return self.cursor.fetchone()

    def fetch_customers(self):
        # Fetch all customers with name and ID
        query = "SELECT id, name, phone FROM customers"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
