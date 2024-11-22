# app/user/user_model.py

import bcrypt
from app.database import Database


class UserModel:
    def __init__(self):
        self.db = Database()

    def hash_password(self, password):
        """Hash a plaintext password."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def update_user(self, user_id, name, hashed_password, email, phone, address):
        """Update user profile in the database."""
        connection = self.db.connect()
        cursor = connection.cursor()

        try:
            query = """
            UPDATE users
            SET name = %s, password = %s, email = %s, phone = %s, address = %s
            WHERE id = %s
            """
            cursor.execute(query, (name, hashed_password, email, phone, address, user_id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
