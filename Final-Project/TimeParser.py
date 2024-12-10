from datetime import datetime, timedelta
import re
from typing import Optional

class TimeParser:
    def __init__(self):
        self.standard_format = "%Y-%m-%d %H:%M"
        
        # Map of common relative time words
        self.relative_time_map = {
            'today': 0,
            'tomorrow': 1,
            'next week': 7,
            'next month': 30,
        }
        
        # Map of common time shortcuts
        self.time_shortcuts = {
            'morning': '09:00',
            'noon': '12:00',
            'afternoon': '14:00',
            'evening': '18:00',
            'night': '20:00',
            'midnight': '00:00',
        }

    def parse(self, time_str: str) -> Optional[datetime]:
        try:
            time_str = time_str.lower().strip()
            
            # Try exact standard format first
            try:
                return datetime.strptime(time_str, self.standard_format)
            except ValueError:
                pass

            # Handle relative dates
            for word, days in self.relative_time_map.items():
                pattern = f"^{word}\\s+at\\s+(.+)$"
                match = re.match(pattern, time_str)
                if match:
                    time_part = match.group(1)
                    base_date = datetime.now() + timedelta(days=days)
                    time_value = self._parse_time_part(time_part)
                    if time_value:
                        return base_date.replace(
                            hour=time_value.hour,
                            minute=time_value.minute,
                            second=0,
                            microsecond=0
                        )

            # Handle date with time shortcuts
            date_with_shortcut = re.match(r"(\d{4}-\d{2}-\d{2})\s+(\w+)", time_str)
            if date_with_shortcut:
                date_str = date_with_shortcut.group(1)
                time_word = date_with_shortcut.group(2)
                if time_word in self.time_shortcuts:
                    return datetime.strptime(f"{date_str} {self.time_shortcuts[time_word]}", "%Y-%m-%d %H:%M")

            # Handle common date formats
            formats_to_try = [
                "%Y-%m-%d %H:%M",
                "%m/%d/%Y %H:%M",
                "%d/%m/%Y %H:%M",
                "%Y/%m/%d %H:%M",
                "%m-%d-%Y %H:%M",
                "%d-%m-%Y %H:%M",
            ]

            for fmt in formats_to_try:
                try:
                    return datetime.strptime(time_str, fmt)
                except ValueError:
                    continue

            return None

        except Exception as e:
            print(f"Error parsing time: {e}")
            return None

    def _parse_time_part(self, time_str: str) -> Optional[datetime]:
        # Check for time shortcuts first
        if time_str in self.time_shortcuts:
            base_date = datetime.now()
            return datetime.strptime(f"{base_date.date()} {self.time_shortcuts[time_str]}", 
                                   "%Y-%m-%d %H:%M")

        time_formats = [
            "%H:%M",
            "%I:%M%p",
            "%I:%M %p",
            "%H.%M",
        ]

        for fmt in time_formats:
            try:
                # Add a dummy date to create a full datetime
                dummy_date = datetime.now().date()
                time_str = time_str.replace(".", ":")
                return datetime.strptime(f"{dummy_date} {time_str}", f"%Y-%m-%d {fmt}")
            except ValueError:
                continue

        return None

    def format_datetime(self, dt: datetime) -> str:
        return dt.strftime(self.standard_format)