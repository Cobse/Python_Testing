import datetime
import win32com, win32com.client
import pytz


def create_meeting(summary, leaders, participants, optionals, hours = 12, minutes = 30, duration = 45):
    outlook = win32com.client.Dispatch("Outlook.Application")
    meeting = outlook.CreateItem(1)

    # Set meeting properties
    meeting.Subject = summary
    meeting.MeetingStatus = 1  # 1 represents a meeting request
    meeting.ResponseRequested = False

    # Set start time
    now = datetime.datetime.now(pytz.timezone('Europe/Oslo'))
    current_weekday = now.weekday()  # Get the current weekday (0 = Monday, 6 = Sunday)

    # Calculate the number of days until the next Wednesday (2 = Wednesday)
    days_until_next_wednesday = (2 - current_weekday + 7) % 7
    next_wednesday = now + datetime.timedelta(days=days_until_next_wednesday)

    # Set Oslo time zone
    oslo_timezone = pytz.timezone('Europe/Oslo')
    print(oslo_timezone)
    # Set start time to 12:30 on the next Wednesday, using Oslo time zone
    start_time = next_wednesday.replace(hour=hours, minute=minutes, second=0, microsecond=0, tzinfo=oslo_timezone)
    print(start_time)
    # Convert the start time to UTC
    #start_time_utc = start_time.astimezone(pytz.UTC)
    #print(start_time_utc)

    # Set the start time of the meeting
    meeting.Start = start_time.strftime("%Y-%m-%d %H:%M")

    # Set duration
    meeting.Duration = duration  # 45 minutes

    # Add leaders as required attendees
    for leader in leaders:
        required_attendee = meeting.Recipients.Add(leader)
        if required_attendee is not None:
            required_attendee.Type = 1  # 1 represents a required attendee

    # Add participants as required attendees
    for participant in participants:
        required_attendee = meeting.Recipients.Add(participant)
        if required_attendee is not None:
            required_attendee.Type = 1  # 1 represents a required attendee

    # Add optionals as optional attendees
    for optional in optionals:
        optional_attendee = meeting.Recipients.Add(optional)
        if optional_attendee is not None:
            optional_attendee.Type = 2  # 2 represents an optional attendee

    meeting.Recipients.ResolveAll()
    meeting.Display()

some_leaders = ["Adolf", "Franco", "Putin", "Benito"]
some_participants = ["Napoleon", "Himmler"]
some_optionals = ["Goering", "Goebbels"]
hours = 12
minutes = 30
duration = 45
create_meeting("Some text", some_leaders, some_participants, some_optionals, hours, minutes, duration)