# 💪 FitBuddy – AI Fitness Plan Generator

FitBuddy is an intelligent, full-stack fitness plan generator powered by Google's Gemini generative AI models, FastAPI, and SQLAlchemy. It generates personalized 7-day workout plans, goal-specific nutrition recommendations, and adaptive workout revisions based on user feedback.
Users can customize recommendations according to their fitness goals and preferences, track their workout completion, monitor their progress, and adapt their plans as their needs change.

## 👥 Project Team Members

The FitBuddy project is developed collaboratively by the following team members.

| S. No. | Name | Student ID |
|---:|---|---|
| 1 | Sana Tasneem Azimudin | 2024503007 |
| 2 | Mahaswetha N | 2024503017 |
| 3 | Monisha G | 2024503043 |
| 4 | Sharmu R | 2024503055 |
| 5 | Priyadharshini M | 2024503501 |

## 🚀 Key Features

1. **AI-Powered 7-Day Workout Generation:** Uses Google's Gemini models to generate structured workout schedules containing warm-ups, primary exercises, sets, repetitions, rest intervals, and cooldowns.

2. **Personalized Nutrition and Recovery Insights:** Generates goal-specific dietary recommendations, hydration guidance, and recovery tips based on user preferences and fitness objectives.

3. **Adaptive Feedback Loop:** Allows users to request workout modifications, such as adding yoga, increasing cardio, or reducing workout intensity, while retaining the original plan for comparison.

4. **Admin / Coach Dashboard:** Provides a dashboard for authorized administrators or coaches to view registered users and compare their original and revised workout plans.

5. **Interactive Swagger API:** Provides interactive API documentation through FastAPI's `/docs` endpoint, making it easier to test and explore REST API endpoints.

6. **📊 Progress Tracking and Fitness Analytics Dashboard (New Feature):** Tracks completed workouts, missed sessions, weekly workout consistency, and progress toward personal fitness goals. Stores workout completion records in the database and presents progress summaries to help users understand their habits and stay motivated.

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Data Validation:** Pydantic v2
- **Database:** SQLite, SQLAlchemy ORM
- **Frontend:** Jinja2 Templates, HTML5, CSS3
- **Generative AI:** Google Gemini models
- **API Documentation:** Swagger UI / OpenAPI
- **Progress Analytics:** Python-based progress calculations and SQLAlchemy database queries

## 📁 Project Structure

The following is an illustrative project structure. Actual filenames and directories may vary depending on your implementation.

```text
FitBuddy/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── team_members.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── progress.html
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   └── ...
├── .gitignore
└── fitbuddy-env/
```

**Note:** The `dashboard.html` and `progress.html` files represent suggested additions for the admin dashboard and user progress-tracking feature. Add them only if your application implements these pages. Do not commit the virtual environment to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd FitBuddy
```

Replace `<repository_url>` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv fitbuddy-env
```

### 3. Activate the Virtual Environment

**Windows — Command Prompt**

```cmd
fitbuddy-env\Scripts\activate.bat
```

**Windows — PowerShell**

```powershell
.\fitbuddy-env\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source fitbuddy-env/bin/activate
```

### 4. Install Dependencies

If the repository contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the primary dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic jinja2 python-multipart google-genai
```

Use the dependencies and Gemini SDK version that match your actual source code.

### 5. Configure the Gemini API Key

Obtain an API key from [Google AI Studio](https://aistudio.google.com/).

**Windows — PowerShell**

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**macOS / Linux**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Replace `your_api_key_here` with your own key.

Never hardcode API keys in your source code or commit secrets to GitHub. Environment variables set this way generally apply only to the current terminal session.

### 6. Run the Application

```bash
uvicorn main:app --reload
```

If your FastAPI application uses a different Python module, replace `main` with the corresponding filename without the `.py` extension.

### 7. Access the Application

Once the server starts, open the following URLs.

| Resource | URL |
|---|---|
| Main Application | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| Swagger API Documentation | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| Alternative API Documentation | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |
| Project Team API | [http://127.0.0.1:8000/team](http://127.0.0.1:8000/team) |
| Admin / Coach Dashboard | [http://127.0.0.1:8000/view-all-users](http://127.0.0.1:8000/view-all-users) |
| Fitness Progress Dashboard | `/progress` — if implemented |

The team API, admin dashboard, and progress dashboard are available only if the corresponding routes have been implemented.

## 🔌 API Endpoints

The following table describes the intended application functionality. Actual routes and HTTP methods depend on your implementation.

| Endpoint | Description |
|---|---|
| `/` | Main application page |
| `/docs` | Interactive Swagger API documentation |
| `/redoc` | Alternative API documentation |
| `/view-all-users` | View registered users and compare workout plans |
| `/team` | Retrieve project team member details |
| `/progress` | View workout completion and fitness progress |
| `/progress/log` | Record a completed workout session |
| `/progress/{user_id}` | Retrieve a user's workout progress |

**Note:** The progress endpoints are proposed examples, not automatically available FastAPI routes. Implement the appropriate database models, schemas, route handlers, and authentication before using them.

## 📊 Progress Tracking and Fitness Analytics

The progress-tracking feature extends FitBuddy beyond workout generation by helping users understand their consistency and activity over time.

### How It Works

1. **Record Workout Completion:** Users mark planned workout sessions as completed, skipped, or not yet completed.
2. **Store Workout History:** SQLAlchemy stores workout records and their associated dates in SQLite.
3. **Calculate Progress Metrics:** The application calculates completed sessions, completion rate, weekly activity, and workout streaks from recorded data.
4. **Display Analytics:** A dashboard displays progress summaries and historical activity.
5. **Encourage Consistency:** Users can review their achievements and adjust their workout schedules based on their progress.

### Example Progress Metrics

| Metric | Description |
|---|---|
| Workouts Completed | Total number of recorded completed sessions |
| Weekly Consistency | Percentage of planned sessions completed during a week |
| Current Streak | Consecutive days with at least one completed workout |
| Goal Progress | Progress toward a user-defined activity target |
| Workout History | Previous sessions with dates and completion status |

These metrics should be calculated from actual workout records rather than generated or assumed by the AI.

## 🔐 Security and Best Practices

- Store API keys in environment variables.
- Never upload `.env` files containing secrets to GitHub.
- Add virtual environments, database files, and Python cache directories to `.gitignore` where appropriate.
- Validate user inputs before generating AI recommendations.
- Protect administrative and user-specific routes with suitable authentication and authorization.
- Ensure users can access only their own progress records unless they have an authorized coach or administrator role.
- Treat AI-generated fitness and nutrition recommendations as general guidance, not a substitute for professional medical advice.
- Avoid presenting estimated fitness metrics as medically validated measurements.

## 🔮 Future Enhancements

- User authentication and profile management.
- Detailed workout history and progress tracking.
- Visual analytics using interactive charts.
- Personalized meal planning based on dietary preferences and restrictions.
- Integration with wearable fitness devices.
- AI-assisted recommendations based on recorded workout feedback.
- Achievement badges, milestones, and consistency challenges.
- Exportable workout schedules and progress reports.
- Mobile-friendly interface and responsive dashboard.

## 📄 License

This project is intended for educational and development purposes. Add an appropriate open-source license, such as the MIT License, if you intend to distribute the project under those terms.

---

**FitBuddy – Your AI-Powered Fitness Companion** 💪

*Plan smarter. Track your progress. Build consistency.*
