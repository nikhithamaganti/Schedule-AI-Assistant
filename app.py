import streamlit as st
import pandas as pd
from src.schedule_assistant.config import Config
from src.schedule_assistant.sheets_client import SheetsClient
from src.schedule_assistant.parser import normalize_and_save, load_local_data
from src.schedule_assistant.qa import get_answer
from src.schedule_assistant.utils import format_error_message
from src.schedule_assistant.insights import detect_conflicts, generate_weekly_summary, generate_recommendations

st.set_page_config(page_title="Schedule Assistant AI", page_icon="📅", layout="wide")

if 'query' not in st.session_state:
    st.session_state.query = ""

st.title("📅 Schedule Assistant AI")
st.markdown("Your smartest scheduling companion with built-in conflict detection and OpenAI reasoning.")

def refresh_data():
    errors = Config.validate_google_config()
    if errors:
        st.sidebar.error(format_error_message("Config Error", errors))
        return False
    try:
        client = SheetsClient()
        data = client.fetch_data()
        if data:
            normalize_and_save(data)
            return True
        else:
             st.sidebar.warning("No data found in sheet.")
    except Exception as e:
        st.sidebar.error(f"Error connecting/parsing: {e}")
    return False

with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("Fetch Latest Data", use_container_width=True, help="Downloads the newest schedule row data directly from Google Sheets."):
        with st.spinner("Fetching data from Google Sheets..."):
            if refresh_data():
                st.success("Successfully synced!")
                
    mode = "🟢 OpenAI Enabled" if Config.OPENAI_API_KEY else "🟡 Fallback Search Mode"
    st.write(f"**Engine Status:** {mode}")

data = load_local_data()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Ask your Assistant")
    question = st.text_input("Ask a question about your schedule:", value=st.session_state.query, placeholder="e.g. When is my interview tomorrow?", help="Type any natural language query about your schedule context.")
    
    # Trigger if manually clicked OR if a sidebar button injected a query
    if st.button("Ask Assistant", help="Use the AI or offline fallback matching algorithm to fetch your answer.") or st.session_state.query:
        # Clear state after executing so it doesn't auto-execute on next render
        search_q = question if question else st.session_state.query
        st.session_state.query = ""
        
        if not search_q.strip():
            st.warning("Please enter a question.")
        elif not data:
            st.warning("No data found. Please fetch data first.")
        else:
            with st.spinner("Analyzing schedule..."):
                answer = get_answer(search_q)
            st.info(answer)
            
    # New Native Highlight Summary
    if st.button("✨ Schedule Summary", use_container_width=True):
        if not data:
            st.warning("No data loaded yet. Please fetch your schedule first.")
        else:
            summ = generate_weekly_summary(data)
            confs = detect_conflicts(data)
            st.success("### 📋 Schedule Summary\n\n" + 
                        f"You have **{summ['total']}** total events scheduled. "
                        f"The bulk of your time is dedicated to **{summ['top_category']}s**. "
                        f"Your busiest stretch is **{summ['busiest_day']}**, and I've detected **{len(confs)}** overlapping instances to review.")
            
    st.divider()
    
    st.subheader("📅 Your Schedule")
    if data:
        df = pd.DataFrame(data)
        # Hide raw datetime fields for a much cleaner UI
        display_df = df.drop(columns=['datetime_start', 'datetime_end'], errors='ignore')
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No schedule data loaded yet. Click 'Fetch Latest Data' in the sidebar to get started.")

with col2:
    st.subheader("💡 Insights")
    if data:
        summary = generate_weekly_summary(data)
        conflicts = detect_conflicts(data)
        recs = generate_recommendations(data, summary, conflicts)
        
        with st.expander("💡 AI Recommendations", expanded=True):
            for r in recs:
                st.markdown(r)
                
        with st.expander("📊 Weekly Overview", expanded=True):
            mc1, mc2 = st.columns(2)
            mc1.metric("Total Tracked Events", summary['total'])
            mc2.metric("Busiest Calendar Day", summary['busiest_day'])
            
            mc3, mc4 = st.columns(2)
            mc3.metric("Top Category", summary['top_category'])
            mc4.metric("Next Upcoming Event", summary['next_event'].split(' - ')[0] if summary['next_event'] != 'None' else 'None')
            
            if summary['important']:
                 st.markdown("**🚨 High Priority Alerts:**")
                 for im in summary['important']:
                     st.error(im)
                     
            if summary['categories']:
                 st.write("**Activity Breakdown:**")
                 cat_df = pd.DataFrame(list(summary['categories'].items()), columns=["Category", "Count"])
                 if not cat_df.empty:
                    st.bar_chart(cat_df.set_index("Category"))
                 
        with st.expander("🚨 Conflicts Detection", expanded=True):
            if conflicts:
                for c in conflicts:
                    st.error(c)
            else:
                st.success("All clear! No overlapping timeblocks.")
    else:
        st.write("Waiting for data load...")
