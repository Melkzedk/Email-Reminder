from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from plyer import notification
import time

def show_reminder(message):
    notification.notify(
        title="Reminder ⏰",
        message=message,
        timeout=10  # seconds
    )

def main():
    scheduler = BackgroundScheduler()
    scheduler.start()

    print("=== Email/Reminder Scheduler ===")
    reminder = input("Enter your reminder message: ")

    time_str = input("Enter reminder time (HH:MM in 24hr format): ")
    try:
        reminder_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        print("❌ Invalid time format. Use HH:MM (24hr).")
        return

    now = datetime.now()
    run_time = datetime.combine(now.date(), reminder_time)

    # if time already passed today, schedule it for tomorrow
    if run_time < now:
        run_time = run_time.replace(day=now.day + 1)

    scheduler.add_job(show_reminder, 'date', run_date=run_time, args=[reminder])

    print(f"✅ Reminder set for {run_time.strftime('%Y-%m-%d %H:%M')}")

    try:
        # keep the script alive
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\n👋 Scheduler stopped.")

if __name__ == "__main__":
    main()
