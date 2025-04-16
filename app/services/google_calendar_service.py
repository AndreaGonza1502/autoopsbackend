from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def build_calendar_service(cred_row):
    creds = Credentials(
        token=cred_row.access_token,
        refresh_token=cred_row.refresh_token,
        token_uri=cred_row.token_uri,
        client_id=cred_row.client_id,
        client_secret=cred_row.client_secret,
        scopes=cred_row.scopes.split(",")
    )
    return build("calendar", "v3", credentials=creds)

def create_event_for_user(cred_row, title, description, start_time, end_time):
    service = build_calendar_service(cred_row)

    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
    }

    return service.events().insert(calendarId="primary", body=event).execute()
