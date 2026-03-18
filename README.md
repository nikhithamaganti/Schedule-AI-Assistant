# 📅 Schedule Assistant AI

A smart, easy-to-use AI assistant that reads your schedule from Google Sheets and answers your questions about it. You can ask things like "What's happening tomorrow?" or "Find me all meetings next week", and it'll instantly filter your events and give you a clean overview!

## ✨ Features

- **Connects to Google Sheets:** Automatically pulls your latest schedule data directly from your spreadsheets.
- **Smart AI Chat:** Uses OpenAI to give you natural, helpful answers about your schedule.
- **No-Internet Fallback Engine:** Even without an OpenAI API key, the app can still understand your date and category questions (like "what's my schedule next week") and find the right events.
- **Conflict Detection:** Warns you if you have overlapping events or double-booked time slots.
- **Beautiful Interface:** Built with Streamlit for a clean, user-friendly web dashboard.

## 🚀 Getting Started

### 1. Download the Project
Clone this repository to your computer and navigate into the folder:
```bash
git clone https://github.com/nikhithamaganti/Schedule-AI-Assistant.git
cd schedule-assistant-ai
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Setup Credentials 
Create a file named `.env` in the main folder (you can copy from `.env.example`) and fill in your details:
```ini
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-service-account.json
SPREADSHEET_ID=your_google_sheet_id
SHEET_RANGE=Sheet1!A1:D50
OPENAI_API_KEY=your_openai_api_key (optional)
```

## 🎮 How to Use

To start the web interface, open your terminal and run:
```bash
streamlit run app.py
```
This will open the dashboard in your browser. From the sidebar, click **"Fetch Latest Data"** to pull the newest events from your Google Sheet, and then you're ready to start asking questions!

## 💡 Example Questions

Once the app is running, try asking:
- "What do I have tomorrow?"
- "Do I have any interviews this week?"
- "What are my meetings today?"
- "Show my schedule"
