import openai
from .config import Config
from .parser import load_local_data
from .fallback import ask_fallback

def get_answer(question: str) -> str:
    """
    Answers a user's question, preferring OpenAI if configured correctly,
    or dropping back to our keyword fallback system.
    """
    data = load_local_data()
    if not data:
        return "No data available. Please fetch data from Google Sheets first."
        
    if Config.OPENAI_API_KEY:
        data_str = _format_data_for_context(data)
        return _ask_openai(question, data_str)
    else:
        return ask_fallback(question, data)

def _format_data_for_context(data: list[dict]) -> str:
    if not data:
        return ""
    
    headers = list(data[0].keys())
    lines = [" | ".join(headers)]
    for row in data:
        lines.append(" | ".join(str(row.get(h, "")) for h in headers))
    return "\\n".join(lines)

def _ask_openai(question: str, context: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        prompt = (
            f"You are a highly intelligent, human-friendly scheduling assistant.\n"
            f"RULES:\n"
            f"- Use a warm, professional, and conversational tone.\n"
            f"- INTERPRET the data. Don't just list events; explain what they mean for the user's day.\n"
            f"- ALWAYS use Markdown (headers, bullet points, bold text) for easy reading.\n"
            f"- If appropriate, offer a brief concluding thought (e.g., 'Have a great meeting!').\n"
            f"- Keep the output perfectly formatted and visually clean.\n\n"
            f"Schedule Data:\n{context}\n\n"
            f"User Question: {question}"
        )
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {e}"
