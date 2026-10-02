# FitBuddy – AI Fitness Plan Generator

FitBuddy is an intelligent, full-stack fitness plan generator powered by Google Gemini generative AI models, FastAPI, and SQLAlchemy. It generates customized 7-day workout plans, goal-specific nutrition advice, and handles real-time plan revisions through a dynamic feedback loop.

---

## 🚀 Key Features

1. **AI 7-Day Workout Generation**: Uses **Gemini 1.5 Pro** to construct detailed, day-by-day regimens with warm-ups, primary exercises (sets, reps, rest intervals), and cooldowns.
2. **Nutrition & Recovery Insights**: Uses **Gemini 1.5 Flash** for rapid, tailored dietary and recovery tips.
3. **Adaptive Feedback Loop**: Allows users to provide feedback (e.g., adding yoga, requesting more cardio), revising the plan while preserving the original.
4. **Admin / Coach Dashboard (`/view-all-users`)**: View registered athletes, compare original vs. revised plans side-by-side.
5. **Interactive Swagger API (`/docs`)**: All capabilities are exposed via REST API endpoints for testing and third-party integrations.
6. **Graceful Offline Mode**: Contains a built-in mock fallback for testing the application without an active Gemini API key.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2
- **Database**: SQLite, SQLAlchemy ORM
- **Frontend**: Jinja2 Templates, Semantic HTML5, Modular CSS
- **AI Models**: Google Generative AI (`gemini-1.5-pro` & `gemini-1.5-flash`)

---

## ⚙️ Installation & Setup

### 1. Clone & Set Up Virtual Environment

```bash
git clone <repository_url>
cd FitBuddy

# Create virtual environment
python -m venv fitbuddy-env

# Activate virtual environment
# Windows:
fitbuddy-env\Scripts\activate
# macOS/Linux:
source fitbuddy-env/bin/activate