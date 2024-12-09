import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from Reminder import Reminder
from RecurrenceRule import RecurrenceRule, RecurrenceType

class StorageService:
    def __init__(self, storage_file: str = "reminders.json"):
        # Get the directory where the script is located
        base_dir = Path(__file__).parent.parent
        # Create a 'data' directory if it doesn't exist
        data_dir = base_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        # Set the full path for the storage file
        self.storage_path = data_dir / storage_file
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        # create storage file if it doesnt exist
        if not self.storage_path.exists():
            self.storage_path.write_text("[]")

    def _serialize_recurrence_rule(self, rule: RecurrenceRule) -> Dict[str, Any]:
        if rule is None:
            return None
        return {
            "type": rule.type.value,  # Store the string value of the enum
            "interval": rule.interval
        }

    def _deserialize_recurrence_rule(self, data: Dict[str, Any]) -> Optional[RecurrenceRule]:
        if data is None:
            return None
        return RecurrenceRule(
            type=RecurrenceType(data["type"]),  # Convert string back to enum
            interval=data["interval"]
        )


    def _serialize_reminder(self, reminder: Reminder) -> Dict[str, Any]:
        # converts Reminder to dictionary
        return {
            "title": reminder.title,
            "datetime": reminder.datetime.isoformat(),
            "description": reminder.description,
            "is_recurring": reminder.is_recurring,
            "recurrence_rule": self._serialize_recurrence_rule(reminder.recurrence_rule),
            "completed": reminder.completed
        }

    def _deserialize_reminder(self, data: Dict[str, Any]) -> Reminder:
        # converts dict to Reminder
        return Reminder(
            title=data["title"],
            datetime=datetime.fromisoformat(data["datetime"]),
            description=data["description"],
            is_recurring=data["is_recurring"],
            recurrence_rule=self._deserialize_recurrence_rule(data.get("recurrence_rule")),
            completed=data["completed"]
        )

    def save_reminders(self, reminders: List[Reminder]) -> bool:
        try:
            reminder_data = [self._serialize_reminder(r) for r in reminders]
            with self.storage_path.open('w') as f:
                json.dump(reminder_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving reminders: {e}")
            return False

    def load_reminders(self) -> List[Reminder]:
        try:
            with self.storage_path.open('r') as f:
                reminder_data = json.load(f)
            return [self._deserialize_reminder(data) for data in reminder_data]
        except Exception as e:
            print(f"Error loading reminders: {e}")
            return []

    def clear_storage(self) -> bool:
        try:
            self.storage_path.write_text("[]")
            return True
        except Exception as e:
            print(f"Error clearing storage: {e}")
            return False