# app/room/billing_model.py

from pymysql.cursors import DictCursor
from app.database import Database


class BillingModel:
    def __init__(self):
        self.conn = Database.connect()
        if self.conn is None:
            raise Exception("Failed to connect to the database")
        self.cursor = self.conn.cursor(DictCursor)
        
    def fetch_all_billings(self):
        """Fetch all billing records from the database."""
        query = """
        SELECT b.id, b.reservationId, r.totalAmount as reservation, b.amount, b.discount, b.paymentDate, b.status
        FROM payments b
        JOIN reservations r ON b.reservationId = r.id
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_billings(self, keyword):
        """Search billing records based on reservation, amount, discount, payment date, or status."""
        if not keyword:  # Handle empty search case
            return self.fetch_all_billings()

        query = """
        SELECT b.id, b.reservationId, b.amount, b.discount, b.paymentDate, b.status
        FROM payments b
        WHERE CAST(b.reservationId AS CHAR) LIKE %s
        OR CAST(b.amount AS CHAR) LIKE %s
        OR CAST(b.discount AS CHAR) LIKE %s
        OR LOWER(b.paymentDate) LIKE %s
        OR LOWER(b.status) LIKE %s
        """
        keyword = f"%{keyword.lower()}%"  # Convert keyword to lowercase for case-insensitive search
        self.cursor.execute(query, (keyword, keyword, keyword, keyword, keyword))
        return self.cursor.fetchall()


    def fetch_reservations(self):
        query = "SELECT id, totalAmount FROM reservations"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_reservation_by_id(self, reservation_id):
        """Fetch a single reservation's details, including the total amount."""
        query = "SELECT id, totalAmount FROM reservations WHERE id = %s"
        self.cursor.execute(query, (reservation_id,))
        return self.cursor.fetchone()


    def create_billing(self, reservation_id, amount, discount, payment_date, status):
        query = """
        INSERT INTO payments (reservationId, amount, discount, paymentDate, status, createdBy)
        VALUES (%s, %s, %s, %s, %s, 1)
        """
        self.cursor.execute(query, (reservation_id, amount, discount, payment_date, status))
        self.conn.commit()

    def update_billing(self, billing_id, reservation_id, amount, discount, payment_date, status):
        query = """
        UPDATE payments
        SET reservationId = %s, amount = %s, discount = %s, paymentDate = %s, status = %s
        WHERE id = %s
        """
        self.cursor.execute(query, (reservation_id, amount, discount, payment_date, status, billing_id))
        self.conn.commit()
