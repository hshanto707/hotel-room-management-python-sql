import bcrypt
from app.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()

    def register_user(self, name, username, password):

        print(name, username, password)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print("password hashed: ", hashed_password)
        connection = self.db.connect()
        print("connection built")
        cursor = connection.cursor()
        print("cursor built")
        query = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"
        print("query: " + query)
        try:
            cursor.execute(query, (name, username, hashed_password))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            self.db.close()

    def authenticate_user(self, username, password):
        connection = self.db.connect()
        cursor = connection.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            return True
        else:
            return False
