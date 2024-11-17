# app/user/user_model.py

import bcrypt
from app.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def register_user(self, name, email, password):
        connection = self.db.connect()
        cursor = connection.cursor()

        # Check if email already exists
        check_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(check_query, (email,))
        if cursor.fetchone() is not None:
            cursor.close()
            connection.close()  # Explicitly close connection after check
            raise ValueError("An account with this email already exists")

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        try:
            cursor.execute(insert_query, (name, email, hashed_password))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            raise e  # Raise exception to be handled by controller if needed
        finally:
            cursor.close()
            connection.close()  # Close connection properly

    def authenticate_user(self, email, password):
        connection = self.db.connect()
        cursor = connection.cursor()

        query = "SELECT password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        # Check if a user was found and if the password matches
        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            cursor.close()
            connection.close()  # Close connection properly
            return True
        else:
            cursor.close()
            connection.close()
            return False
