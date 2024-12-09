from dataclasses import dataclass
import json
from pathlib import Path
from typing import Optional, Dict

@dataclass
class User:
    username: str
    
    def __str__(self) -> str:
        return f"User: {self.username}"
    

class UserService:
    def __init__(self, storage_file: str = "users.json"):
        # Get the directory where the script is located
        base_dir = Path(__file__).parent.parent
        # Use the same data directory as reminders
        data_dir = base_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        # Set the full path for the storage file
        self.storage_path = data_dir / storage_file
        self.current_user: Optional[User] = None
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        if not self.storage_path.exists():
            self.storage_path.write_text("{}")

    def _serialize_user(self, user: User) -> Dict:
        return {
            "username": user.username
        }

    def _deserialize_user(self, data: Dict) -> User:
        return User(username=data["username"])

    def create_user(self, username: str) -> Optional[User]:
        try:
            with self.storage_path.open('r') as f:
                users = json.load(f)
            
            if username in users:
                print(f"User {username} already exists.")
                return None

            new_user = User(username=username)
            users[username] = self._serialize_user(new_user)

            with self.storage_path.open('w') as f:
                json.dump(users, f, indent=2)

            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user(self, username: str) -> Optional[User]:
        try:
            with self.storage_path.open('r') as f:
                users = json.load(f)
            
            if username not in users:
                return None

            return self._deserialize_user(users[username])
        except Exception as e:
            print(f"Error retrieving user: {e}")
            return None

    def login(self, username: str) -> bool:
        user = self.get_user(username)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self) -> None:
        self.current_user = None

    def get_current_user(self) -> Optional[User]:
        return self.current_user