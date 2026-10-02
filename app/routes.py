import os
import logging
from fastapi import APIRouter, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import (
    get_db,
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_plan,
    get_user,
)
from app.models import User, WorkoutPlan
from app.schemas import (
    UserInput,
    WorkoutRequest,
    FeedbackRequest,
    PlanResponse,
    UpdatedPlanResponse,
    NutritionTipResponse,
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

logger = logging.getLogger(__name__)

router = APIRouter()

# Template Engine Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# =====================================================================
# 1. HTML Web Routes
# =====================================================================

# HOME PAGE ROUTE (GET /) -> renders templates/index.html
@router.get("/", response_class=HTMLResponse, summary="Render Home Form Page")
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None}
    )


# WORKOUT GENERATION ROUTE (POST /generate-workout) -> renders templates/result.html
@router.post("/generate-workout", response_class=HTMLResponse, summary="Process Form & Generate Plan")
def generate_workout_html(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    # Validation checks
    if user_id <= 0:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "User ID must be a positive integer."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    if age < 12 or age > 100:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Please enter an age between 12 and 100."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    if weight < 25.0 or weight > 350.0:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Please enter a realistic weight in kg (25 - 350)."},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Save user to DB
        save_user(
            user_id=user_id,
            name=username.strip(),
            age=age,
            weight=weight,
            goal=goal.strip(),
            intensity=intensity.strip()
        )

        # Generate Workout Plan via Gemini 1.5 Pro
        user_input_dict = {
            "goal": goal.strip(),
            "intensity": intensity.strip(),
            "age": age,
            "weight": weight
        }
        plan_text = generate_workout_gemini(user_input_dict)

        # Generate Nutrition Tip via Gemini 1.5 Flash
        nutrition_tip = generate_nutrition_tip_with_flash(goal.strip())

        # Save Plan to DB
        save_plan(user_id=user_id, plan=plan_text, nutrition_tip=nutrition_tip)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": username.strip(),
                "user_id": user_id,
                "age": age,
                "weight": weight,
                "goal": goal.strip(),
                "intensity": intensity.strip(),
                "workout_plan": plan_text,
                "nutrition_tip": nutrition_tip,
                "updated_plan": None,
                "update_success": False
            }
        )
    except Exception as e:
        logger.error(f"Error generating workout HTML: {e}")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": f"An error occurred: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# FEEDBACK SUBMISSION ROUTE (POST /submit-feedback) -> updates plan & re-renders result.html
@router.post("/submit-feedback", response_class=HTMLResponse, summary="Submit Plan Feedback")
def submit_feedback_html(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    feedback_clean = feedback.strip()
    if not feedback_clean:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user(user_id)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": f"User ID {user_id} not found. Please register first."},
            status_code=status.HTTP_404_NOT_FOUND
        )

    original_plan = get_original_plan(user_id)
    if not original_plan:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": f"No workout plan exists for User ID {user_id}."},
            status_code=status.HTTP_404_NOT_FOUND
        )

    try:
        # Call Gemini Pro to update plan
        updated_text = update_workout_plan(original_plan, feedback_clean)

        # Update in database
        update_plan(user_id=user_id, updated_text=updated_text, feedback=feedback_clean)

        # Fetch current plan row for nutrition tip
        plan_record = get_plan(user_id)
        nutrition_tip = plan_record.nutrition_tip if plan_record else ""

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user.name,
                "user_id": user.id,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "workout_plan": original_plan,
                "nutrition_tip": nutrition_tip,
                "updated_plan": updated_text,
                "update_success": True
            }
        )
    except Exception as e:
        logger.error(f"Error submitting feedback HTML: {e}")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": f"Failed to update workout plan: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ADMIN / COACH ROUTE (GET /view-all-users) -> renders templates/all_users.html
@router.get("/view-all-users", response_class=HTMLResponse, summary="Coach/Admin View")
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.asc()).all()
    user_data = []

    for user in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_data.append({
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "original_plan": plan.original_plan if plan and plan.original_plan else "N/A",
            "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated"
        })

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": user_data}
    )


# =====================================================================
# 2. RESTful JSON API Endpoints (FastAPI Swagger Docs)
# =====================================================================

@router.post("/generate-workout/gemini", summary="API: Standalone Workout Generation")
async def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {
            "model": "gemini-1.5-pro",
            "workout_plan": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition-tip", response_model=NutritionTipResponse, summary="API: Generate Nutrition Tip")
def get_flash_tip(goal: str):
    if not goal or not goal.strip():
        raise HTTPException(status_code=400, detail="Fitness goal parameter is required.")
    tip = generate_nutrition_tip_with_flash(goal.strip())
    return {
        "goal": goal.strip(),
        "nutrition_tip": tip
    }


@router.post("/generate-plan", response_model=PlanResponse, summary="API: Save User & Generate Plan")
def generate_plan_api(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )

        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity,
            "age": user_data.age,
            "weight": user_data.weight
        })

        tip = generate_nutrition_tip_with_flash(user_data.goal)
        save_plan(user_data.user_id, plan, tip)

        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan,
            "nutrition_tip": tip
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/update-plan/{user_id}", response_model=UpdatedPlanResponse, summary="API: Update Plan with Feedback")
def update_user_plan_api(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        raise HTTPException(status_code=404, detail="Original plan not found for this user.")

    try:
        updated = update_workout_plan(original, data.feedback)
        update_plan(user_id, updated, data.feedback)
        return {
            "message": "Plan successfully updated with feedback",
            "user_id": user_id,
            "updated_plan": updated
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update plan: {str(e)}")


@router.get("/api/users", summary="API: List All Users and Plans")
def list_all_users_api(db: Session = Depends(get_db)):
    users = db.query(User).all()
    results = []
    for u in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).first()
        results.append({
            "user_id": u.id,
            "name": u.name,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "has_original_plan": plan is not None and bool(plan.original_plan),
            "has_updated_plan": plan is not None and bool(plan.updated_plan),
            "original_plan": plan.original_plan if plan else None,
            "updated_plan": plan.updated_plan if plan else None,
            "nutrition_tip": plan.nutrition_tip if plan else None,
        })
    return {"total_users": len(results), "users": results}