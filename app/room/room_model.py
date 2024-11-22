# models/room_model.py

import pymysql
from pymysql.cursors import DictCursor
from app.database import Database

class RoomModel:
    def __init__(self):
        self.conn = Database.connect()
        if self.conn is None:
            raise Exception("Failed to connect to the database")
        # Use DictCursor to get results as dictionaries
        self.cursor = self.conn.cursor(DictCursor)

    def create_room(self, room_no, room_type, price, status, airConditioning, created_by=1):
        # Check for duplicate room number
        check_query = "SELECT COUNT(*) as count FROM rooms WHERE roomNo = %s"
        self.cursor.execute(check_query, (room_no,))
        result = self.cursor.fetchone()
        if result['count'] > 0:
            raise ValueError(f"Room number {room_no} already exists.")

        # Insert room if no duplicate
        query = """
        INSERT INTO rooms (roomNo, type, price, status, airConditioning, createdBy)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (room_no, room_type, price, status, airConditioning, created_by))
        self.conn.commit()


    def fetch_all_rooms(self):
        query = "SELECT * FROM rooms"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_rooms(self, keyword):
        query = """
        SELECT * FROM rooms
        WHERE roomNo LIKE %s OR type LIKE %s OR status LIKE %s OR airConditioning LIKE %s
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(query, (keyword, keyword, keyword, keyword))
        return self.cursor.fetchall()

    def update_room(self, room_id, room_no, room_type, price, status, airConditioning):
        query = """
        UPDATE rooms
        SET roomNo = %s, type = %s, price = %s, status = %s, airConditioning = %s
        WHERE roomNo = %s
        """
        self.cursor.execute(query, (room_no, room_type, price, status, airConditioning, room_id))
        self.conn.commit()


    def delete_room(self, room_id):
        query = "DELETE FROM rooms WHERE roomNo = %s"
        self.cursor.execute(query, (room_id,))  # Ensure this is a tuple
        self.conn.commit()


    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
