import schedule, time, random
from datetime import datetime, timedelta
from plyer import notification
from core.agent import generate_ping

def start_scheduler():
    # Pick 2–4 random times between 9:00 and 21:00
    num_pings = random.randint(2, 4)
    times = generate_random_times(num_pings)

    print(f"Luna will ping at: {', '.join(times)}")

    for t in times:
        schedule.every().day.at(t).do(send_ping)

    while True:
        schedule.run_pending()
        time.sleep(60)

def generate_random_times(n):
    start = datetime.strptime("09:00", "%H:%M")
    end = datetime.strptime("21:00", "%H:%M")
    total_minutes = int((end - start).total_seconds() / 60)

    chosen = sorted(random.sample(range(total_minutes), n))
    return [(start + timedelta(minutes=m)).strftime("%H:%M") for m in chosen]

def send_ping():
    text = generate_ping()
    notification.notify(
        title="Luna (glitchwitch)",
        message=text,
        timeout=6
    )
