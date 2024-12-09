from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

class RecurrenceType(Enum):
    DAILY = "day"
    WEEKLY = "week"
    MONTHLY = "month"
    YEARLY = "year"

@dataclass
class RecurrenceRule:
    type: RecurrenceType
    interval: int = 1  # e.g., every 2 days, every 3 weeks
    
    def get_next_occurrence(self, from_date: datetime) -> datetime:
        if self.type == RecurrenceType.DAILY:
            return from_date + timedelta(days=self.interval)
        elif self.type == RecurrenceType.WEEKLY:
            return from_date + timedelta(weeks=self.interval)
        elif self.type == RecurrenceType.MONTHLY:
            # Add months by manipulating the month component
            year = from_date.year + ((from_date.month + self.interval - 1) // 12)
            month = ((from_date.month + self.interval - 1) % 12) + 1
            return from_date.replace(year=year, month=month)
        elif self.type == RecurrenceType.YEARLY:
            return from_date.replace(year=from_date.year + self.interval)
            
    def __str__(self) -> str:
        if self.interval == 1:
            return f"Every {self.type.value}"
        return f"Every {self.interval} {self.type.value}s"