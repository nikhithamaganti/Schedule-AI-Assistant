from src.schedule_assistant.qa import _ask_fallback

def test_ask_fallback():
    data = [
        ["Name", "Event", "Time"],
        ["Alice", "Standup", "10:00 AM"],
        ["Bob", "1on1", "1:00 PM"],
        ["Charlie", "Planning", "3:00 PM"]
    ]
    
    # Keyword 'standup' should match Alice
    answer1 = _ask_fallback("When is the standup?", data)
    assert "Alice" in answer1
    assert "Standup" in answer1
    
    # Keyword 'charlie' should match his row
    answer2 = _ask_fallback("What time is charlie meeting?", data)
    assert "Charlie" in answer2
    assert "3:00 PM" in answer2
    
    # Missing keyword
    answer3 = _ask_fallback("Lunch?", data)
    assert "couldn't find a confident answer" in answer3
