# cli/main.py
from ReminderBot import ReminderBot

def pause():
    input("\nPress Enter to continue...")

def main():
    bot = ReminderBot()
    
    while True:
        bot.display_menu()
        current_user = bot.get_current_user()
        
        if not current_user:
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == "1":
                bot.handle_login()
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
            pause()
        else:
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "1":
                bot.handle_add_reminder()
                pause()
            elif choice == "2":
                bot.handle_list_reminders()
                pause()
            elif choice == "3":
                bot.handle_mark_completed()
                pause()
            elif choice == "4":
                bot.handle_remove_reminder()
                pause()
            elif choice == "5":
                bot.logout()
                pause()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                pause()

if __name__ == "__main__":
    main()