import re

class User:
    def __init__(self, user_id, fullname, email, username, contact=None, address=None, password=None):
        self.user_id = user_id
        self.fullname = fullname
        self.email = email
        self.username = username
        self.contact = contact
        self.address = address
        self.password = password

        self.validate()

    def validate(self):
        if not isinstance(self.user_id, int):
            raise ValueError("User ID must be an integer")
        if not self.fullname:
            raise ValueError("Full name cannot be empty")
        if not self.email or not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.password or len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
    @classmethod
    def get_user_by_id(cls, user_id):
        for user in cls.users:
            if user.user_id == user_id:
                return user
        return None

    def __str__(self):
        return (f"User({self.user_id}, {self.fullname}, {self.email}, {self.username}, "
                f"{self.contact}, {self.address}, {self.password})")
    

