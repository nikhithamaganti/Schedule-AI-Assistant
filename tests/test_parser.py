import pytest
import datetime
from src.schedule_assistant.parser import detect_category, parse_date, parse_time, combine_datetime

def test_detect_category():
    assert detect_category("Team Meeting", "Discuss Q3") == "Meeting"
    assert detect_category("Software Engineer Interview", "") == "Interview"
    assert detect_category("Doctor Appointment", "health check") == "Health"
    assert detect_category("Lunch with Bob", "") == "Personal"
    assert detect_category("Code Review", "") == "Work"

def test_parse_date():
    assert parse_date("2026-03-01") == datetime.date(2026, 3, 1)
    assert parse_date("03-01-26") == datetime.date(2026, 3, 1)
    assert parse_date("03/01/2026") == datetime.date(2026, 3, 1)
    assert parse_date("Mar 01, 2026") == datetime.date(2026, 3, 1)
    assert parse_date("March 01, 2026") == datetime.date(2026, 3, 1)

    with pytest.raises(ValueError):
        parse_date("Invalid Date")
    with pytest.raises(ValueError):
        parse_date("")

def test_parse_time():
    assert parse_time("08:30 AM") == datetime.time(8, 30)
    assert parse_time("02:30 PM") == datetime.time(14, 30)
    assert parse_time("14:30") == datetime.time(14, 30)

    with pytest.raises(ValueError):
        parse_time("Invalid Time")

def test_combine_datetime():
    dt = combine_datetime("2026-03-01", "08:30 AM")
    assert dt == datetime.datetime(2026, 3, 1, 8, 30)
    
    # Missing time defaults to midnight
    dt_no_time = combine_datetime("2026-03-01", "")
    assert dt_no_time == datetime.datetime(2026, 3, 1, 0, 0)
    
    # Invalid time but valid date falls back to midnight gracefully
    dt_invalid_time = combine_datetime("2026-03-01", "Nope")
    assert dt_invalid_time == datetime.datetime(2026, 3, 1, 0, 0)
    
    with pytest.raises(ValueError):
        combine_datetime("Not a date", "10:00 AM")
