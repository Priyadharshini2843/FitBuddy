from pydantic import BaseModel, Field
from typing import Optional


class UserInput(BaseModel):
    """Pydantic model for full user details submission."""
    username: str = Field(..., min_length=1, max_length=100, description="User's full name or handle")
    user_id: int = Field(..., gt=0, description="Unique numeric user identification ID")
    age: int = Field(..., ge=12, le=100, description="User's age in years")
    weight: float = Field(..., gt=20.0, le=350.0, description="User's weight in kilograms")
    goal: str = Field(..., min_length=2, max_length=200, description="Fitness goal (e.g. Weight Loss, Muscle Gain)")
    intensity: str = Field(..., description="Workout intensity: Low, Medium, or High")


class WorkoutRequest(BaseModel):
    """Pydantic model for standalone workout generation API."""
    goal: str = Field(..., min_length=2, description="Target fitness objective")
    intensity: str = Field(..., description="Intensity level: Low, Medium, or High")


class FeedbackRequest(BaseModel):
    """Pydantic model for feedback submission and plan revision."""
    feedback: str = Field(..., min_length=3, max_length=1000, description="User feedback or adjustment requests")


class PlanResponse(BaseModel):
    """Pydantic model for workout plan response payload."""
    message: str
    workout_plan: str
    nutrition_tip: Optional[str] = None


class UpdatedPlanResponse(BaseModel):
    """Pydantic response model for updated plan."""
    message: str
    user_id: int
    updated_plan: str


class NutritionTipResponse(BaseModel):
    """Pydantic model for nutrition tip responses."""
    goal: str
    nutrition_tip: str