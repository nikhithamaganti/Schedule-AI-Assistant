from src.schedule_assistant.insights import generate_weekly_summary

def test_generate_weekly_summary():
    data = [
        {"date": "2026-03-20", "event": "Sync", "category": "Meeting"},
        {"date": "2026-03-20", "event": "1on1", "category": "Meeting"},
        {"date": "2026-03-21", "event": "Google Interview", "category": "Interview"}
    ]
    summary = generate_weekly_summary(data)
    
    assert summary["total"] == 3
    assert summary["busiest_day"] == "2026-03-20"
    assert summary["categories"]["Meeting"] == 2
    assert "Google Interview" in summary["important"]
