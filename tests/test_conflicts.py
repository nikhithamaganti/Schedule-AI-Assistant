from src.schedule_assistant.insights import detect_conflicts

def test_detect_conflicts():
    data = [
        {"event": "Meeting A", "date": "2026-03-20", "datetime_start": "2026-03-20T10:00:00", "datetime_end": "2026-03-20T11:00:00"},
        {"event": "Meeting B", "date": "2026-03-20", "datetime_start": "2026-03-20T10:30:00", "datetime_end": "2026-03-20T11:30:00"}
    ]
    conflicts = detect_conflicts(data)
    assert len(conflicts) == 1
    assert "overlaps" in conflicts[0]
    
def test_no_conflicts():
    data = [
        {"event": "Meeting A", "date": "2026-03-20", "datetime_start": "2026-03-20T10:00:00", "datetime_end": "2026-03-20T11:00:00"},
        {"event": "Meeting B", "date": "2026-03-20", "datetime_start": "2026-03-20T11:00:00", "datetime_end": "2026-03-20T12:00:00"}
    ]
    assert len(detect_conflicts(data)) == 0
