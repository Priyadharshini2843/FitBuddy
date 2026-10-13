# FitBuddy – AI Fitness Plan Generator

FitBuddy is an intelligent, full-stack fitness plan generator powered by Google's Gemini generative AI models, FastAPI, and SQLAlchemy. It generates personalized 7-day workout plans, goal-specific nutrition recommendations, and adaptive workout revisions based on user feedback.

Users can tailor recommendations to their fitness goals and preferences, then provide feedback to adapt their workout plans as their needs change.

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

1. **AI-Powered 7-Day Workout Generation:** Uses Google Gemini 1.5 Pro to generate detailed workout schedules with warm-ups, primary exercises, sets, repetitions, rest intervals, and cooldowns.
2. **Personalized Nutrition and Recovery Insights:** Uses Google Gemini 1.5 Flash to provide tailored dietary recommendations and recovery tips.
3. **Adaptive Feedback Loop:** Allows users to request modifications, such as adding yoga or increasing cardio, while preserving the original workout plan.
4. **Admin / Coach Dashboard:** The `/view-all-users` dashboard allows administrators or coaches to view registered athletes and compare original and revised workout plans.
5. **Interactive Swagger API:** The `/docs` endpoint provides interactive API documentation for testing REST API endpoints.

## 🛠️ Technology Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **Data Validation:** Pydantic v2
- **Database:** SQLite, SQLAlchemy ORM
- **Frontend:** Jinja2 Templates, HTML5, CSS3
- **Generative AI:** Google Gemini 1.5 Pro and Gemini 1.5 Flash
- **API Documentation:** Swagger UI / OpenAPI

## 📁 Project Structure

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
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css
│   └── ...
└── fitbuddy-env/
```

*Note: The structure above is illustrative. Adjust the filenames and folders to match your actual repository.*

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

**Windows (Command Prompt):**

```cmd
fitbuddy-env\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
.\fitbuddy-env\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source fitbuddy-env/bin/activate
```

### 4. Install Dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the main dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic jinja2 python-multipart google-generativeai
```

### 5. Configure the Gemini API Key

Obtain a Gemini API key from Google AI Studio:

https://aistudio.google.com/

Configure the key using an environment variable rather than hardcoding it in the source code.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**macOS / Linux:**

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Replace `your_api_key_here` with your own API key. Never commit API keys or other secrets to GitHub.

### 6. Run the Application

```bash
uvicorn main:app --reload
```

If your FastAPI application uses a different Python filename, replace `main` with the appropriate module name.

### 7. Access the Application

Once the server starts, open the following URLs:

| Resource | URL |
|---|---|
| Application | http://127.0.0.1:8000 |
| Interactive API Documentation | http://127.0.0.1:8000/docs |
| Alternative API Documentation | http://127.0.0.1:8000/redoc |
| Project Team API | http://127.0.0.1:8000/team |
| Admin / Coach Dashboard | http://127.0.0.1:8000/view-all-users |

*Note: The URLs for the team API and dashboard work only if the corresponding routes are implemented in the application.*

## 🔌 API Endpoints

The following endpoints describe the intended functionality. Actual routes and HTTP methods depend on the implementation in the repository.

| Endpoint | Description |
|---|---|
| `/` | Main application page |
| `/docs` | Interactive Swagger API documentation |
| `/redoc` | Alternative API documentation |
| `/view-all-users` | View registered users and compare workout plans |
| `/team` | Retrieve project team member details |


## 🔐 Security and Best Practices

- Store API keys in environment variables.
- Never upload `.env` files containing secrets to GitHub.
- Add virtual environments, database files, and cache directories to `.gitignore` where appropriate.
- Validate user inputs before generating fitness recommendations.
- Protect administrative routes with suitable authentication and authorization.
- Treat AI-generated fitness and nutrition recommendations as general guidance, not a substitute for professional medical advice.

## 🔮 Future Enhancements

- User authentication and profile management.
- Progress tracking and workout history.
- Personalized meal planning based on dietary preferences.
- Interactive fitness dashboards and visual progress reports.
- Integration with wearable fitness devices.
- Improved recommendation quality through user feedback.

## 📄 License

This project is intended for educational and development purposes. Add an appropriate open-source license, such as the MIT License, if you intend to distribute the project under those terms.

---

**FitBuddy – Your AI-Powered Fitness Companion** 💪
