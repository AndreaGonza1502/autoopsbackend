from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        "google-credentials.json",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return build("calendar", "v3", credentials=creds)

def create_google_event(summary, description, start_time, end_time):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event["id"]
