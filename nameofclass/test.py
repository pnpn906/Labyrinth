class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self,username, password):
        super().__init__(username, password)

    def BanUser(self, username):
        print(f"User {username} banned.")

user1 = User("user1", "sdf98fodk")
user2 = Admin("admin1", "099d9f")