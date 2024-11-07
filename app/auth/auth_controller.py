from app.user.user_model import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def login(self, username, password):
        return self.user_model.authenticate_user(username, password)

    def register(self, name, username, password):
        try:
            self.user_model.register_user(name, username, password)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
