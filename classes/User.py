from datetime import datetime, timezone

class User:
    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        created_at: datetime = None,
        is_active: bool = True,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at or datetime.now(timezone.utc)
        self.is_active = is_active

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def deactivate(self):
        self.is_active = False

    def update_email(self, new_email: str):
        self.email = new_email

    def update_password(self, new_hash: str):
        self.password_hash = new_hash

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
        }

