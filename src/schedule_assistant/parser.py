import csv
import datetime
from pathlib import Path
from .utils import ensure_data_dir_exists

def detect_category(event: str, notes: str) -> str:
    combined = (event + " " + notes).lower()
    if "meeting" in combined or "sync" in combined:
        return "Meeting"
    if "interview" in combined:
        return "Interview"
    if "doctor" in combined or "health" in combined:
        return "Health"
    if "lunch" in combined or "dinner" in combined:
        return "Personal"
    return "Work"

def parse_date(date_str: str) -> datetime.date:
    """Parses various real-world date formats into a datetime.date object."""
    if not date_str:
        raise ValueError("Empty date string provided")
    
    date_str = date_str.strip()
    
    formats = [
        "%Y-%m-%d",      # 2026-03-01
        "%m-%d-%y",      # 03-01-26
        "%m/%d/%Y",      # 03/01/2026
        "%b %d, %Y",     # Mar 01, 2026
        "%B %d, %Y",     # March 01, 2026
        "%m-%d-%Y",      # 03-01-2026
    ]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
            
    raise ValueError(f"Unable to parse date format: {date_str}")

def parse_time(time_str: str) -> datetime.time:
    """Parses 12-hour and 24-hour time formats into a datetime.time object."""
    if not time_str:
        raise ValueError("Empty time string provided")
        
    time_str = time_str.strip()
    
    formats = [
        "%I:%M %p",  # 08:30 AM
        "%H:%M",     # 14:30
    ]
    
    for fmt in formats:
        try:
            return datetime.datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
            
    raise ValueError(f"Unable to parse time format: {time_str}")

def combine_datetime(date_str: str, time_str: str) -> datetime.datetime:
    """Combines a date string and optionally a time string into a valid datetime object."""
    try:
        parsed_date = parse_date(date_str)
    except ValueError as e:
        raise e
        
    # If no time is provided, default to midnight for the valid date
    if not time_str or not time_str.strip():
        return datetime.datetime.combine(parsed_date, datetime.time.min)
        
    try:
        parsed_time = parse_time(time_str)
        return datetime.datetime.combine(parsed_date, parsed_time)
    except ValueError:
        # If time is totally invalid but date is valid, just use midnight
        return datetime.datetime.combine(parsed_date, datetime.time.min)

def normalize_and_save(raw_data: list[list], filename: str = "whatsdata.tsv") -> Path:
    if not raw_data or len(raw_data) < 2:
        raise ValueError("Not enough data to parse. Dataset empty or no headers.")
        
    data_dir = ensure_data_dir_exists()
    file_path = data_dir / filename
    
    headers = ["date", "time", "event", "notes", "category", "datetime_start", "datetime_end"]
    structured_data = [headers]
    
    for row in raw_data[1:]:
        date_raw = row[0] if len(row) > 0 else ""
        time_raw = row[1] if len(row) > 1 else ""
        event_raw = row[2] if len(row) > 2 else ""
        notes_raw = row[3] if len(row) > 3 else ""
        
        if not date_raw.strip() and not time_raw.strip() and not event_raw.strip() and not notes_raw.strip():
            continue
            
        if not event_raw.strip():
            event_raw = "Unknown Event"
            
        category = detect_category(event_raw, notes_raw)
        
        dt_start_obj = None
        if date_raw:
            try:
                dt_start_obj = combine_datetime(date_raw, time_raw)
            except ValueError:
                dt_start_obj = None
                
        dt_start = dt_start_obj.isoformat() if dt_start_obj else ""
        
        dt_end = ""
        if dt_start_obj:
            dt_end_obj = dt_start_obj + datetime.timedelta(hours=1)
            dt_end = dt_end_obj.isoformat()
            
        clean_row = [
            date_raw.strip(),
            time_raw.strip(),
            event_raw.strip(),
            notes_raw.strip(),
            category,
            dt_start,
            dt_end
        ]
        structured_data.append(clean_row)
        
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(structured_data)
        
    return file_path

def load_local_data(filename: str = "whatsdata.tsv") -> list[dict]:
    """Loads parsed TSV data into a list of dictionaries."""
    data_dir = ensure_data_dir_exists()
    file_path = data_dir / filename
    if not file_path.exists():
        return []
    
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        return list(reader)
