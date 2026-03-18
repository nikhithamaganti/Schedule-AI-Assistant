from src.schedule_assistant.fallback import ask_fallback

def test_ask_fallback():
    data = [
        {"date": "2026-03-20", "time": "10:00 AM", "event": "Standup", "category": "Meeting"},
        {"date": "2026-03-21", "time": "02:00 PM", "event": "Candidate Round", "category": "Interview"}
    ]
    
    ans1 = ask_fallback("standup meeting", data)
    assert "Standup" in ans1
    
    ans2 = ask_fallback("interview", data)
    assert "Candidate" in ans2
