from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# SQLite requires check_same_thread=False for multi-threaded FastAPI execution
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency for yielding a managed SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initializes and auto-creates all database tables."""
    import app.models  # Ensure models are loaded into Base metadata
    Base.metadata.create_all(bind=engine)


# ==========================================
# Database Operation Helper Functions
# ==========================================

def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str) -> None:
    """Creates a new user or updates existing user details."""
    from app.models import User
    db = SessionLocal()
    try:
        existing = db.query(User).filter_by(id=user_id).first()
        if existing:
            existing.name = name
            existing.age = age
            existing.weight = weight
            existing.goal = goal
            existing.intensity = intensity
        else:
            new_user = User(
                id=user_id,
                name=name,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                schedule=7,
            )
            db.add(new_user)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def save_plan(user_id: int, plan: str, nutrition_tip: str = "") -> None:
    """Saves or updates the initial workout plan and nutrition tip for a user."""
    from app.models import WorkoutPlan
    db = SessionLocal()
    try:
        existing = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if existing:
            existing.original_plan = plan
            if nutrition_tip:
                existing.nutrition_tip = nutrition_tip
        else:
            workout = WorkoutPlan(
                user_id=user_id,
                original_plan=plan,
                nutrition_tip=nutrition_tip
            )
            db.add(workout)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def update_plan(user_id: int, updated_text: str, feedback: str = "") -> None:
    """Persists the feedback-updated workout plan without overwriting the original plan."""
    from app.models import WorkoutPlan
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
        if workout:
            workout.updated_plan = updated_text
            if feedback:
                workout.user_feedback = feedback
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_original_plan(user_id: int) -> str | None:
    """Fetches the original workout plan for a given user ID."""
    from app.models import WorkoutPlan
    db = SessionLocal()
    try:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return plan.original_plan if plan else None
    finally:
        db.close()


def get_plan(user_id: int):
    """Fetches the complete WorkoutPlan record for a user."""
    from app.models import WorkoutPlan
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    finally:
        db.close()


def get_user(user_id: int):
    """Fetches a User record by primary key user ID."""
    from app.models import User
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()