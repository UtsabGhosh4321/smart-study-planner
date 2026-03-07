from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_study_feedback(tasks):
    prompt = f"""
    Analyze these tasks and provide a personalized weekly study strategy:
    {tasks}
    Focus on burnout prevention and efficiency.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    
    return response.choices[0].message.content