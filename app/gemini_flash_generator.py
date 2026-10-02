import logging
from google import genai
from app.config import settings

logger = logging.getLogger(__name__)


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generates a concise, practical nutrition or recovery tip using Gemini 1.5 Flash
    tailored to the user's fitness goal.
    """
    prompt = (
        f"Give one clear, helpful, evidence-based nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand (2 to 3 sentences maximum). "
        "Do not prescribe extreme diets or extreme calorie restrictions."
    )

    if settings.google_api_key and settings.google_api_key.strip():
        try:
            client = genai.Client(api_key=settings.google_api_key.strip())
            response = client.models.generate_content(
                model=settings.gemini_flash_model,
                contents=prompt,
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini Flash API failure: {e}")
            return "Tip: Stay consistent with whole foods, prioritize lean protein, and drink at least 2.5L of water daily."

    # Offline realistic fallback tip
    goal_lower = goal.lower()
    if "loss" in goal_lower or "fat" in goal_lower:
        return "Prioritize protein and fiber in every meal! Pairing lean protein (chicken, tofu, eggs) with high-volume veggies keeps you satisfied in a mild deficit while preventing muscle loss."
    elif "gain" in goal_lower or "muscle" in goal_lower:
        return "Prioritize post-workout nutrition! Consume a meal rich in complete protein (25–35g) paired with complex carbohydrates within 90 minutes of training to optimize muscle protein synthesis."
    else:
        return "Hydration and sleep are the twin pillars of recovery! Aim for 7–8 hours of sound sleep and stay hydrated consistently to facilitate muscle tissue repair and maintain daytime energy."