from datetime import datetime
from typing import List, Optional
from ReminderManager import ReminderManager
from Reminder import Reminder
from User import User, UserService
from RecurrenceRule import RecurrenceRule, RecurrenceType
from TimeParser import TimeParser
from NotificationService import NotificationService
from Scheduler import Scheduler

class ReminderBot:
    def __init__(self):
        self.reminder_manager = ReminderManager()
        self.user_service = UserService()
        self.time_parser = TimeParser() # integrate
        self.notification_service = NotificationService() # implement
        self.scheduler = Scheduler() # implement

    def handle_login(self) -> None:
        username = input("Enter username: ")
        if self.user_service.login(username):
            print(f"Welcome back, {username}!")
        else:
            create = input("User not found. Would you like to create a new account? (y/n): ")
            if create.lower() == 'y':
                if self.create_user(username):
                    print(f"Account created successfully! Welcome, {username}!")
                    self.user_service.login(username)
                else:
                    print("Failed to create account.")

    def create_user(self, username: str) -> bool:
        user = self.user_service.create_user(username)
        return user is not None
    
    def get_current_user(self) -> Optional[User]:
        return self.user_service.get_current_user()
    
    def logout(self) -> None:
        self.user_service.logout()
        print("Logged out successfully")
    
    def handle_add_reminder(self) -> None:
        title = input("Enter reminder title: ")
        date_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
        description = input("Enter description (optional): ")
        
        recur = input("Should this reminder recur? (y/n): ").lower()
        recurrence_rule = None
        
        if recur == 'y':
            print("\nRecurrence Options:")
            print("1. Daily")
            print("2. Weekly")
            print("3. Monthly")
            print("4. Yearly")
            
            try:
                type_choice = input("Choose recurrence type (1-4): ")
                interval = int(input("Enter interval (e.g., every X days/weeks/etc): "))
                
                type_map = {
                    "1": RecurrenceType.DAILY,
                    "2": RecurrenceType.WEEKLY,
                    "3": RecurrenceType.MONTHLY,
                    "4": RecurrenceType.YEARLY
                }
                
                if type_choice in type_map:
                    recurrence_rule = RecurrenceRule(
                        type=type_map[type_choice],
                        interval=interval
                    )
            except ValueError:
                print("Invalid interval. Creating reminder without recurrence.")
        
        if self.create_reminder(title, date_str, description, recurrence_rule):
            print("Reminder added successfully!")
        else:
            print("Failed to add reminder. Please check the date format.")

    def create_reminder(self, title: str, date_str: str, description: Optional[str] = None, recurrence_rule: Optional[RecurrenceRule] = None) -> bool:
        if not self.get_current_user():
            print("Please log in first.")
            return False
        
        try:
            reminder_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            reminder = Reminder(
                title=title,
                datetime=reminder_datetime,
                description=description,
                recurrence_rule=recurrence_rule
            )
            self.reminder_manager.add_reminder(reminder)
            return True
        except ValueError:
            return False
        
    def handle_list_reminders(self) -> None:
        reminders = self.reminder_manager.get_all_reminders()
        if not reminders:
            print("No reminders found.")
        else:
            for i, reminder in enumerate(reminders, 1):
                print(f"{i}. {reminder}")

    def handle_mark_completed(self) -> None:
        reminders = self.reminder_manager.get_pending_reminders()
        if not reminders:
            print("No pending reminders.")
            return
            
        print("Pending reminders:")
        for i, reminder in enumerate(reminders, 1):
            print(f"{i}. {reminder}")
        
        try:
            idx = int(input("Enter reminder number to mark as completed: ")) - 1
            if 0 <= idx < len(reminders):
                reminder = reminders[idx]
                self.reminder_manager.mark_completed(reminder)
                print("Reminder marked as completed!")
                if reminder.recurrence_rule:
                    next_datetime = reminder.recurrence_rule.get_next_occurrence(reminder.datetime)
                    new_reminder = Reminder(
                        title=reminder.title,
                        datetime=next_datetime,
                        description=reminder.description,
                        recurrence_rule=reminder.recurrence_rule
                    )
                    self.reminder_manager.add_reminder(new_reminder)
                    print(f"Next occurrence scheduled for: {next_datetime.strftime('%Y-%m-%d %H:%M')}")
                
                follow_up = input("\nWould you like to schedule a follow-up task? (y/n): ").lower()
                if follow_up == 'y':
                    print("\nCreating follow-up task...")
                    title = input("Enter follow-up task title: ")
                    date_str = input("Enter date and time (YYYY-MM-DD HH:MM): ")
                    description = input("Enter description (optional): ")
                    
                    if self.create_reminder(title, date_str, description if description else None):
                        print("Follow-up task added successfully!")
                    else:
                        print("Failed to add follow-up task. Please check the date format.")
            else:
                print("Invalid reminder number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def handle_remove_reminder(self) -> None:
        reminders = self.reminder_manager.get_all_reminders()
        if not reminders:
            print("No reminders to remove.")
            return
            
        print("All reminders:")
        for i, reminder in enumerate(reminders, 1):
            print(f"{i}. {reminder}")
        
        try:
            idx = int(input("Enter reminder number to remove: ")) - 1
            if 0 <= idx < len(reminders):
                self.reminder_manager.remove_reminder(reminders[idx])
                print("Reminder removed successfully!")
            else:
                print("Invalid reminder number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def display_menu(self) -> None:
        current_user = self.get_current_user()
        print("\nReminder Bot")
        print(f"Current user: {current_user.username if current_user else 'Not logged in'}")
        
        if not current_user:
            print("\nCommands:")
            print("1. Login")
            print("2. Exit")
        else:
            print("\nCommands:")
            print("1. Add reminder")
            print("2. List all reminders")
            print("3. Mark reminder as completed")
            print("4. Remove reminder")
            print("5. Logout")
            print("6. Exit")