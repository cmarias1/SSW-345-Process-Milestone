from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from RecurrenceRule import RecurrenceRule

@dataclass
class Reminder:
    title: str
    datetime: datetime
    description: Optional[str] = None
    is_recurring: bool = False
    recurrence_rule: Optional[RecurrenceRule] = None
    completed: bool = False
    
    def __str__(self) -> str:
        status = "[X]" if self.completed else "[]"
        base_str = f"{status} {self.title} - {self.datetime.strftime('%Y-%m-%d %H:%M')}"
        if self.recurrence_rule:
            base_str += f" ({self.recurrence_rule})"
        return base_str