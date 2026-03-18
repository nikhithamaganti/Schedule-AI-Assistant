import argparse
import sys
from .config import Config
from .utils import format_error_message
from .sheets_client import SheetsClient
from .parser import normalize_and_save, load_local_data
from .qa import get_answer
from .insights import detect_conflicts, generate_weekly_summary

def main():
    parser = argparse.ArgumentParser(description="Schedule Assistant AI CLI")
    parser.add_argument("--fetch", action="store_true", help="Fetch latest data from Google Sheets")
    parser.add_argument("--skip-fetch", action="store_true", help="Use cached data and skip API fetch")
    parser.add_argument("--ask", type=str, help="Ask a natural-language question about the schedule")
    parser.add_argument("--insights", action="store_true", help="Show smart weekly summary and detected conflicts")
    
    args = parser.parse_args()
    
    if args.fetch and not args.skip_fetch:
        errors = Config.validate_google_config()
        if errors:
            print(format_error_message("Google Sheets Config", errors))
            sys.exit(1)
            
        print("Fetching data from Google Sheets...")
        try:
            client = SheetsClient()
            raw_data = client.fetch_data()
            if not raw_data:
                print("No active rows found in the specified range.")
                sys.exit(0)
                
            path = normalize_and_save(raw_data)
            print(f"Data successfully fetched and saved to {path} (TSV format)")
        except Exception as e:
            print(f"Error fetching data: {e}")
            sys.exit(1)
            
    if args.insights:
        data = load_local_data()
        if not data:
            print("No data available. Run with --fetch first.")
        else:
            summary = generate_weekly_summary(data)
            print("\\n--- Weekly Summary ---")
            print(f"Total Events: {summary['total']}")
            print(f"Busiest Day: {summary['busiest_day']}")
            print(f"Important Items: {summary.get('important', [])}")
            print(f"Categories: {summary['categories']}")
            
            conflicts = detect_conflicts(data)
            print("\\n--- Conflicts ---")
            if conflicts:
                for c in conflicts:
                    print(c)
            else:
                print("No overlapping events detected.")
                
    if args.ask:
        if Config.OPENAI_API_KEY:
            print("Mode: OpenAI Answers API")
        else:
            print("Mode: Fallback Search (No OpenAI API Key found)")
            
        print(f"Q: {args.ask}\\nA: {get_answer(args.ask)}\\n")
        
    if not args.fetch and not args.ask and not args.insights:
        parser.print_help()

if __name__ == "__main__":
    main()
