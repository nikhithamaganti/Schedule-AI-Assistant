from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from .config import Config

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class SheetsClient:
    """Client for interacting with Google Sheets API."""
    def __init__(self):
        self.creds = None
        if Config.GOOGLE_APPLICATION_CREDENTIALS and os.path.exists(Config.GOOGLE_APPLICATION_CREDENTIALS):
            try:
                self.creds = service_account.Credentials.from_service_account_file(
                    Config.GOOGLE_APPLICATION_CREDENTIALS, scopes=SCOPES)
            except Exception as e:
                print(f"Warning: Could not load GOOGLE_APPLICATION_CREDENTIALS: {e}")
        
        # We only build the service if creds are valid
        self.service = build('sheets', 'v4', credentials=self.creds) if self.creds else None

    def fetch_data(self) -> list[list]:
        """
        Fetches data from the configured Google Sheet via the API.
        Returns a list of lists representing rows and columns.
        """
        if not self.service:
            raise ValueError("Sheets service not initialized. Check credentials.")
        
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=Config.SPREADSHEET_ID,
            range=Config.SHEET_RANGE
        ).execute()
        
        values = result.get('values', [])
        return values
