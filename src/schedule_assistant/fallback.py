import datetime
import re

def ask_fallback(question: str, data: list[dict]) -> str:
    if not data:
        return "No data available in fallback system."
        
    q_lower = question.lower()
    today = datetime.date.today()
    
    # 1. Understand query intent
    # Detect time references
    date_matches = re.findall(r'\d{4}-\d{2}-\d{2}', q_lower)
    time_locators = ["today", "tomorrow", "this week", "next week"]
    has_time_intent = any(t in q_lower for t in time_locators) or bool(date_matches)
    
    # Detect event/category references
    all_categories = {d.get('category', '').lower() for d in data if d.get('category')}
    event_keywords = ["meeting", "interview", "workshop", "lunch"]
    
    detected_category = next((c for c in all_categories if c and (c in q_lower or c + "s" in q_lower)), None)
    detected_evt_type = next((ek for ek in event_keywords if ek in q_lower or ek + "s" in q_lower), None)
    has_event_intent = bool(detected_category or detected_evt_type)
    
    # Detect general schedule questions
    is_general_schedule = "schedule" in q_lower or "what do i have" in q_lower or "show my" in q_lower
    
    # 2. Convert query into filters
    def is_date_match(d_str: str) -> bool:
        if not d_str:
            return False
        try:
            d = datetime.date.fromisoformat(d_str)
        except ValueError:
            return False
            
        if "today" in q_lower:
            return d == today
        elif "tomorrow" in q_lower:
            return d == today + datetime.timedelta(days=1)
        elif "this week" in q_lower:
            start_date = today - datetime.timedelta(days=today.weekday())
            end_date = start_date + datetime.timedelta(days=6)
            return start_date <= d <= end_date
        elif "next week" in q_lower:
            start_date = today + datetime.timedelta(days=7 - today.weekday())
            end_date = start_date + datetime.timedelta(days=6)
            return start_date <= d <= end_date
        elif date_matches:
            return d_str in date_matches
            
        # If no explicit time intent, default to upcoming events for general queries
        return d >= today

    def is_event_match(row: dict) -> bool:
        cat = row.get('category', '').lower()
        evt_text = (str(row.get('event', '')) + " " + str(row.get('notes', ''))).lower()
        
        if detected_category and (detected_category == cat or detected_category in evt_text):
            return True
        if detected_evt_type and (detected_evt_type == cat or detected_evt_type in evt_text):
            return True
            
        return False

    # 3. Return only matching events from the schedule
    results = []
    
    for row in data:
        date_ok = is_date_match(row.get('date', '')) if (has_time_intent or is_general_schedule) else True
        event_ok = is_event_match(row) if has_event_intent else True
        
        # Apply combined filtering logically
        if is_general_schedule and not has_event_intent:
            # e.g., "what is my schedule next week" OR "what is my schedule"
            if date_ok:
                results.append(row)
        elif has_time_intent or has_event_intent:
            # e.g., "what are today meetings", "do I have interviews this week"
            if date_ok and event_ok:
                results.append(row)

    if not results:
        return f"### 📭 Nothing Found\n\nI couldn't find any events matching your request."
        
    results.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))
    
    ans = "### 🔍 Your Schedule\n\n"
    for r in results:
        ans += f"- **{r.get('date', '')} — {r.get('time', 'All Day')}** → {r.get('event', '')} ({r.get('category', '')})\n"
        
    ans += f"\n*Insight: I found {len(results)} events that match your criteria.*"
    return ans
