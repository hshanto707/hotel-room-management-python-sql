import pymysql

class Database:
  @staticmethod
  def connect():
    try:
      connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel_room_management",
        port=3306
      )
      if connection.open:
        print("Database connection successful!")
      return connection
    except pymysql.MySQLError as err:
      print(f"Database connection failed: {err}")
      return None

  def close(self):
    if self.connection and self.connection.open:
        print("Closing database connection")
        self.connection.close()
