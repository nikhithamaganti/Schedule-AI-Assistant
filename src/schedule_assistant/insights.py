import datetime
from collections import Counter

def detect_conflicts(data: list[dict]) -> list[str]:
    """Finds overlapping events based on datetime_start and datetime_end."""
    conflicts = []
    valid_events = [d for d in data if d.get('datetime_start') and d.get('datetime_end')]
    valid_events.sort(key=lambda x: x['datetime_start'])
    
    for i in range(len(valid_events) - 1):
        ev1 = valid_events[i]
        ev2 = valid_events[i+1]
        
        if ev2['datetime_start'] < ev1['datetime_end']:
            t1 = ev1.get('time', '')
            t2 = ev2.get('time', '')
            conflicts.append(f"**{ev1.get('date', '')}**: `{t1}` ({ev1.get('event')}) ⚡ overlaps with `{t2}` ({ev2.get('event')})")
            
    return conflicts

def generate_weekly_summary(data: list[dict]) -> dict:
    """Generates statistics for a week of schedule data, pulling out key metrics and grouped alerts."""
    if not data:
        return {"total": 0, "busiest_day": "N/A", "important": [], "categories": {}, "top_category": "N/A", "next_event": "None"}
    
    dates = []
    categories = []
    important_events = []
    now = datetime.datetime.now()
    future_events = []
    
    for d in data:
        date_str = d.get('date', '')
        if date_str:
            dates.append(date_str)
            
        cat = d.get('category', 'Uncategorized')
        if cat:
            categories.append(cat)
        
        if cat.lower() in ['interview', 'meeting']:
            important_events.append(cat)
            
        dt_start_str = d.get('datetime_start')
        if dt_start_str:
            try:
                dt = datetime.datetime.fromisoformat(dt_start_str)
                if dt > now:
                    future_events.append((dt, d))
            except ValueError:
                pass

    date_counts = Counter(dates)
    busiest_day = date_counts.most_common(1)[0][0] if dates else "N/A"
    
    cat_counts = Counter(categories)
    top_cat = cat_counts.most_common(1)[0][0] if categories else "N/A"
    
    # Group important events tightly
    im_counter = Counter(important_events)
    grouped_important = [f"{cat}s ({count} upcoming)" for cat, count in im_counter.items()]
    
    next_ev = "None"
    future_events.sort(key=lambda x: x[0])
    if future_events:
        nxt = future_events[0][1]
        nxt_date = nxt.get('date', '')
        today_str = datetime.datetime.now().date().isoformat()
        tmrw_str = (datetime.datetime.now().date() + datetime.timedelta(days=1)).isoformat()
        
        day_label = nxt_date
        if nxt_date == today_str:
            day_label = "today"
        elif nxt_date == tmrw_str:
            day_label = "tomorrow"
            
        next_ev = f"{day_label} at {nxt.get('time', '')} - {nxt.get('event', '')}"
        
    return {
        "total": len(data),
        "busiest_day": busiest_day,
        "important": grouped_important,
        "categories": dict(cat_counts),
        "top_category": top_cat,
        "next_event": next_ev
    }

def generate_recommendations(data: list[dict], summary: dict, conflicts: list[str]) -> list[str]:
    """Analyzes the schedule to provide intelligent, human-readable advice."""
    recs = []
    
    # 1. Conflict Warning
    if conflicts:
        recs.append(f"⚠️ **Conflict Detected**: You have {len(conflicts)} overlapping events. You might want to reschedule to avoid being double-booked.")
        
    # 2. Burnout Detection
    busiest_day = summary.get('busiest_day')
    if busiest_day != "N/A":
        day_events = [d for d in data if d.get('date') == busiest_day]
        if len(day_events) >= 4:
            recs.append(f"🔋 **Heavy Day**: {busiest_day} is packed with {len(day_events)} events. You might benefit from blocking some focus time to avoid overload.")
            
    # 3. Schedule Trend
    top_cat = summary.get('top_category')
    if top_cat != "N/A":
        recs.append(f"📊 **Focus Area**: The majority of your scheduled time is dedicated to {top_cat}s.")
        
    if not recs:
        recs.append("✨ Your schedule looks nicely balanced! Enjoy your week.")
        
    return recs
