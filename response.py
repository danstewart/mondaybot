from delorean import Delorean
import datetime

def generate_reply(text, user_id):
    if not is_valid(text):
        reply_text = "Incorrect Format - Should be HH:MM (eg. 09:00 or 16:45)"
        return create_json(reply_text, user_id)

    hours   = text[0:2]
    minutes = text[3:5]

    # Handle timezone
    now = Delorean()
    now.shift("Europe/London")  # Currently only supports UK timezone

    # If today is Monday and before our target time
    if now.datetime.weekday() == 0 and (now.datetime.hour < int(hours) or (now.datetime.hour == int(hours) and now.datetime.minute < int(minutes))):
        monday = now.datetime
    else:
        monday = now.next_monday().datetime

    target = Delorean(datetime.datetime(monday.year, monday.month, monday.day, int(hours), int(minutes)), timezone='Europe/London')

    # Calculate time
    result        = (target - now)
    days_until    = result.days
    hours_until   = result.seconds / 60 / 60
    minutes_until = (result.seconds / 60) - (hours_until * 60)

    # Format message
    days_format    = "day"    if days_until == 1    else "days"
    hours_format   = "hour"   if hours_until == 1   else "hours"
    minutes_format = "minute" if minutes_until == 1 else "minutes"
    reply_text = "{} {}, {} {} and {} {} until Monday at {}:{}.".format(days_until, days_format, hours_until, hours_format, minutes_until, minutes_format, hours, minutes)
    return create_json(reply_text, user_id)

def is_valid(text):
    hours = text[0:2]
    minutes = text[3:5]
    return hours.isdigit() and minutes.isdigit()

def create_json(reply, user_id):
    data = {
        "recipient":{ "id": user_id },
	    "message":{ "text": reply }
    }

    return data
