from typing import List
from Reminder import Reminder
from StorageService import StorageService

class ReminderManager:
    def __init__(self):
        self.storage = StorageService()
        self.reminders: List[Reminder] = self.storage.load_reminders()
    
    def add_reminder(self, reminder: Reminder) -> None:
        self.reminders.append(reminder)
        self.reminders.sort(key=lambda x: x.datetime)
        self.storage.save_reminders(self.reminders)
    
    def get_all_reminders(self) -> List[Reminder]:
        return self.reminders
    
    def get_pending_reminders(self) -> List[Reminder]:
        return [r for r in self.reminders if not r.completed]
    
    def mark_completed(self, reminder: Reminder) -> None:
        if reminder in self.reminders:
            reminder.completed = True
            self.storage.save_reminders(self.reminders)
    
    def remove_reminder(self, reminder: Reminder) -> None:
        if reminder in self.reminders:
            self.reminders.remove(reminder)
            self.storage.save_reminders(self.reminders)