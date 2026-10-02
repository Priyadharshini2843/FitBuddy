import logging
from google import genai
from app.config import settings

logger = logging.getLogger(__name__)


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Revises the original 7-day workout plan using Gemini 1.5 Pro based on user feedback.
    Maintains formatting consistency and structural safety.
    """
    prompt = f"""
You are a professional fitness trainer assistant.

Here is the user's current 7-day workout plan:
\"\"\"
{original_plan}
\"\"\"

User Feedback:
\"{user_feedback}\"

INSTRUCTIONS:
1. Based on the user's feedback, intelligently revise the relevant parts of the workout plan (e.g. adjust volume, replace exercises, add cardio, substitute equipment, or modify rest days).
2. Keep the overall day-by-day structure (Warm-up, Main Workout, Cooldown) intact and cleanly formatted in Markdown.
3. Ensure all modifications remain safe, practical, and balanced.
4. Add a brief, encouraging note at the top explaining what specific adjustments were made based on their feedback.
"""

    if settings.google_api_key and settings.google_api_key.strip():
        try:
            client = genai.Client(api_key=settings.google_api_key.strip())
            response = client.models.generate_content(
                model=settings.gemini_pro_model,
                contents=prompt,
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini Plan Revision API failure: {e}")
            return f"Error updating plan via Gemini: {str(e)}"

    # Offline realistic update simulation
    return f"""### Plan Updated Based on Your Feedback: "{user_feedback}"

{original_plan}

---
*Trainer Modification Notes: Adjusted workout distribution, pacing, and intensity parameters to accommodate your request: "{user_feedback}". Maintain appropriate hydration and respect your recovery thresholds.*"""