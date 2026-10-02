from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User profile model storing physical stats and fitness goals."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String(200), nullable=False)
    intensity = Column(String(50), nullable=False)
    schedule = Column(Integer, default=7)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to workout plans
    plans = relationship("WorkoutPlan", back_populates="user", cascade="all, delete-orphan")


class WorkoutPlan(Base):
    """Workout plan model storing original and feedback-updated plans."""
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)
    user_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship to user
    user = relationship("User", back_populates="plans")