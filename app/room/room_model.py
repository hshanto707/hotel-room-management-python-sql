# models/room_model.py

import mysql.connector
from app.config import DB_CONFIG

class RoomModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def create_room(self, room_no, room_type, price, status, created_by=1):
        query = "INSERT INTO Room (roomNo, type, price, status, createdBy) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (room_no, room_type, price, status, created_by))
        self.conn.commit()

    def fetch_all_rooms(self):
        query = "SELECT * FROM Room"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_rooms(self, keyword):
        query = """
        SELECT * FROM Room
        WHERE roomNo LIKE %s OR type LIKE %s OR status LIKE %s
        """
        keyword = f"%{keyword}%"
        self.cursor.execute(query, (keyword, keyword, keyword))
        return self.cursor.fetchall()

    def update_room(self, room_id, room_no, room_type, price, status):
        query = "UPDATE Room SET roomNo = %s, type = %s, price = %s, status = %s WHERE Id = %s"
        self.cursor.execute(query, (room_no, room_type, price, status, room_id))
        self.conn.commit()

    def delete_room(self, room_id):
        query = "DELETE FROM Room WHERE Id = %s"
        self.cursor.execute(query, (room_id,))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
