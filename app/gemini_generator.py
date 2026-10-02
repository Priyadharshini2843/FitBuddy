import logging
from google import genai
from app.config import settings

logger = logging.getLogger(__name__)


def get_gemini_client():
    """Returns an authenticated GenAI Client instance."""
    if settings.google_api_key and settings.google_api_key.strip():
        return genai.Client(api_key=settings.google_api_key.strip())
    return None


def generate_workout_gemini(user_input: dict) -> str:
    """
    Generates a personalized, structured 7-day workout plan using Gemini 1.5 Pro.
    Includes medical/safety guardrails and fallback mock capability.
    """
    goal = user_input.get("goal", "General Fitness")
    intensity = user_input.get("intensity", "Medium")
    age = user_input.get("age", 25)
    weight = user_input.get("weight", 70.0)

    prompt = f"""
You are a certified professional fitness trainer and exercise physiologist.
Create a personalized, structured 7-day workout plan for an individual with:
- Fitness Goal: {goal}
- Preferred Intensity: {intensity}
- Age: {age} years
- Weight: {weight} kg

SAFETY & HEALTH GUIDELINES:
- Provide safe, sustainable exercises. Avoid extreme or dangerous recommendations.
- Emphasize proper form, warm-ups, hydration, and active recovery.
- Include a reminder to consult a medical professional before beginning strenuous training.

FORMAT REQUIREMENT:
Provide clear markdown formatting starting with an introductory overview and disclaimers, followed by Day 1 through Day 7:
## 7-Day {intensity}-Intensity Workout Plan for {goal}

**Day 1: [Target Muscle / Focus]**
* **Warm-up (5-10 mins):** [Specific warm-up exercises with duration/reps]
* **Main Workout:**
  * **[Exercise 1]:** [Sets] sets of [Reps] reps
  * **[Exercise 2]:** [Sets] sets of [Reps] reps
  * **[Exercise 3]:** [Sets] sets of [Reps] reps
  * **[Exercise 4]:** [Sets] sets of [Reps] reps
* **Cooldown:** [Static stretches with target muscles and hold times]

(Repeat identical structured format for Day 2 through Day 7, designating 1 or 2 days for Rest or Active Recovery depending on intensity).

**Important Notes:**
* Progressive Overload guidance
* Proper Form recommendations
* Hydration and Recovery guidance
"""

    client = get_gemini_client()
    if not client:
        logger.warning("GOOGLE_API_KEY not configured. Generating realistic offline fallback plan.")
        return generate_mock_workout_plan(goal, intensity)

    try:
        response = client.models.generate_content(
            model=settings.gemini_pro_model,
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
        return "Error: Gemini returned an empty response. Please try again."
    except Exception as e:
        logger.error(f"Gemini API generation failure: {e}")
        return f"Error communicating with Gemini: {str(e)}"


def generate_mock_workout_plan(goal: str, intensity: str) -> str:
    """Offline mock plan ensuring zero-friction local testing without an active API key."""
    return f"""## 7-Day {intensity.title()} Workout Plan for {goal.title()}

*Fitness Disclaimer: This plan is for informational and educational purposes only. Always consult a healthcare professional before initiating a new exercise program.*

**Day 1: Upper Body Strength**
* **Warm-up (5-10 mins):** Jumping jacks (60 seconds), arm circles (30 seconds each direction), high knees, torso twists.
* **Main Workout:**
  * **Dumbbell / Barbell Bench Press:** 3 sets of 8-12 reps
  * **Lat Pulldowns or Pull-ups:** 3 sets of 8-10 reps
  * **Overhead Shoulder Press:** 3 sets of 10-12 reps
  * **Seated Cable Rows:** 3 sets of 10-12 reps
  * **Bicep Curls superset with Tricep Pushdowns:** 3 sets of 12-15 reps
* **Cooldown:** Static chest and lat stretches, hold each for 30 seconds.

**Day 2: Lower Body & Core**
* **Warm-up (5-10 mins):** Bodyweight squats (15 reps), dynamic hip openers, glute bridges (15 reps).
* **Main Workout:**
  * **Goblet or Barbell Squats:** 3 sets of 8-12 reps
  * **Romanian Deadlifts:** 3 sets of 10-12 reps
  * **Walking Lunges:** 3 sets of 10 steps per leg
  * **Plank Holds:** 3 sets of 45-60 seconds
  * **Hanging Knee / Leg Raises:** 3 sets of 12 reps
* **Cooldown:** Hamstring, quad, and pigeon pose stretches.

**Day 3: HIIT Cardio & Agility**
* **Warm-up (5-10 mins):** Light jogging in place, high knees, dynamic calf stretches.
* **Main Workout:**
  * **Burpees:** 3 sets of 10 reps
  * **Mountain Climbers:** 3 sets of 30-45 seconds
  * **Kettlebell Swings:** 3 sets of 15 reps
  * **Jump Squats:** 3 sets of 12 reps
* **Cooldown:** Light walking for 3 minutes, calf and quad stretches.

**Day 4: Active Recovery & Mobility**
* **Active Recovery:** 30 minutes of brisk walking, gentle swimming, or yoga mobility flows. Prioritize joint mobility and tissue oxygenation.

**Day 5: Full Body Functional Conditioning**
* **Warm-up (5-10 mins):** Inchworms, jumping jacks, shoulder dislocates with light band.
* **Main Workout:**
  * **Push-ups:** 3 sets of 12-15 reps
  * **Dumbbell Deadlifts:** 3 sets of 10 reps
  * **Renegade Rows:** 3 sets of 8 reps per arm
  * **Bodyweight Bulgarian Split Squats:** 3 sets of 10 reps per leg
* **Cooldown:** Full-body static stretching and controlled deep breathing.

**Day 6: Core & Endurance Circuit**
* **Warm-up (5-10 mins):** 5 minutes elliptical or light skipping.
* **Main Workout:**
  * **Russian Twists:** 3 sets of 20 total twists
  * **Bicycle Crunches:** 3 sets of 20 reps
  * **Side Planks:** 3 sets of 30 seconds per side
  * **Incline Treadmill Walk:** 20 minutes at moderate pace
* **Cooldown:** Cobra stretch, child's pose, and hamstring stretches.

**Day 7: Full Rest & Restoration**
* **Rest:** Full rest day. Focus on optimal hydration, high protein distribution across meals, and 8 hours of restorative sleep.

**Important Notes:**
* **Progressive Overload:** Gradually increase weight, repetitions, or tempo over subsequent weeks.
* **Form First:** Maintain strict technique to safeguard joints and maximize muscle recruitment.
* **Hydration:** Consume at least 2.5–3.5 liters of clean water daily, increasing on workout days."""