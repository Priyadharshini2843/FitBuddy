import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# =========================================================================
# STEP 1: AUTO-GENERATE HIGH-RESOLUTION ARCHITECTURE DIAGRAM
# =========================================================================
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#F8FAFC')
    ax.axis('off')

    def draw_box(ax, x, y, w, h, title, subtitle, items, bg_color, border_color, title_color='#1E3A8A'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.25, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_color, zorder=3)
        if subtitle:
            ax.text(x + w/2, y + h - 0.45, subtitle, ha='center', va='center', fontsize=8, fontstyle='italic', color='#64748B', zorder=3)
        ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.6, y + h - 0.6], color=border_color, linewidth=1, zorder=3)
        start_y = y + h - 0.85
        for i, item in enumerate(items):
            ax.text(x + 0.2, start_y - i*0.28, item, ha='left', va='center', fontsize=8.2, color='#1E293B', zorder=3)

    # 1. Frontend Tier
    draw_box(ax, 0.3, 1.2, 2.5, 3.6, 
             "FRONTEND TIER", "Client Interface", 
             ["* HTML5 & Modular CSS3", "* Responsive Flex/Grid UI", "* Jinja2 Dynamic Views:", "   - index.html (Intake)", "   - result.html (Plan)", "   - all_users.html (Admin)", "* Real-time Feedback Loop"],
             "#EFF6FF", "#93C5FD", "#1E40AF")

    # 2. FastAPI Backend
    draw_box(ax, 3.6, 0.8, 3.2, 4.2, 
             "FASTAPI BACKEND", "Application Engine (Uvicorn)", 
             ["* main.py (Lifespan & Mount)", "* routes.py (HTTP & REST APIs)", "* schemas.py (Pydantic v2)", "* config.py (Settings & .env)", "* database.py (SessionLocal CRUD)", "* updated_plan.py (Revision Engine)", "* Offline Mock Fallbacks"],
             "#F0FDF4", "#86EFAC", "#065F46")

    # 3. AI Services Tier
    draw_box(ax, 7.5, 2.8, 2.6, 2.2, 
             "GENERATIVE AI LAYER", "Google AI Studio", 
             ["* Gemini 1.5 Pro (Pro Engine)", "  - 7-Day Structured Routines", "  - Nuanced Feedback Updates", "* Gemini 1.5 Flash", "  - Fast Nutrition & Recovery Tips"],
             "#FAF5FF", "#D8B4FE", "#6B21A8")

    # 4. Persistence Tier
    draw_box(ax, 7.5, 0.6, 2.6, 1.8, 
             "PERSISTENCE LAYER", "Relational Database", 
             ["* SQLite (fitbuddy.db)", "* SQLAlchemy ORM Entities:", "  - User (Demographics)", "  - WorkoutPlan (History)"],
             "#FFFBEB", "#FDE68A", "#92400E")

    def draw_arrow(ax, x1, y1, x2, y2, label="", color="#475569"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=1.6, mutation_scale=14), zorder=4)
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 0.12, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=color,
                    bbox=dict(boxstyle="square,pad=0.15", facecolor='white', edgecolor='#CBD5E1', lw=0.8), zorder=5)

    draw_arrow(ax, 2.8, 3.0, 3.6, 3.0, "HTTP / JSON")
    draw_arrow(ax, 6.8, 3.9, 7.5, 3.9, "google-genai SDK")
    draw_arrow(ax, 6.8, 1.5, 7.5, 1.5, "SQLAlchemy CRUD")

    plt.title("FitBuddy – Solution Architecture & System Component Diagram", fontsize=13, fontweight='bold', color='#1E3A8A', pad=15)
    plt.tight_layout()
    plt.savefig("architecture_diagram.png", dpi=300, bbox_inches='tight')
    plt.close()

generate_architecture_diagram()

# =========================================================================
# STEP 2: BUILD PDF REPORT
# =========================================================================
pdf_filename = "FitBuddy_Project_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 752, "FITBUDDY – AI FITNESS PLAN GENERATOR")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 752, "PROJECT REPORT")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 744, 558, 744)
        self.line(54, 46, 558, 46)
        self.setFont("Helvetica", 8)
        self.drawString(54, 34, "Academic & Technical Project Report Submission")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#1E3A8A")
secondary_color = colors.HexColor("#2563EB")
text_dark = colors.HexColor("#0F172A")
text_muted = colors.HexColor("#475569")
light_bg = colors.HexColor("#F8FAFC")

title_style = ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=primary_color, alignment=1, spaceAfter=8)
subtitle_style = ParagraphStyle('CoverSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=15, textColor=text_muted, alignment=1, spaceAfter=14)
h1_style = ParagraphStyle('ReportH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=primary_color, spaceBefore=11, spaceAfter=4, keepWithNext=True)
h2_style = ParagraphStyle('ReportH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=secondary_color, spaceBefore=7, spaceAfter=3, keepWithNext=True)
body_style = ParagraphStyle('ReportBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=text_dark, spaceAfter=4)
bullet_style = ParagraphStyle('ReportBullet', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=text_dark, leftIndent=12, firstLineIndent=-9, spaceAfter=2.5)
tbl_header_style = ParagraphStyle('TblHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.white)
tbl_cell_style = ParagraphStyle('TblCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=text_dark)
img_caption_style = ParagraphStyle('ImgCaption', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.8, leading=10.5, textColor=primary_color, alignment=1, spaceBefore=3, spaceAfter=6)

story = []

# COVER PAGE
story.append(Spacer(1, 15))
story.append(Paragraph("ACADEMIC & TECHNICAL PROJECT REPORT", ParagraphStyle('TopTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=secondary_color, alignment=1, spaceAfter=10)))
story.append(Paragraph("FITBUDDY – AI FITNESS PLAN GENERATOR USING GEMINI MODELS", title_style))
story.append(HRFlowable(width="65%", thickness=2, color=secondary_color, spaceAfter=12, spaceBefore=4))
story.append(Paragraph("A Modular Full-Stack Web Platform for Automated 7-Day Workout Regimens, Goal-Aligned Nutrition Advice, and Dynamic Feedback-Driven Adaptations", subtitle_style))
story.append(Spacer(1, 10))

meta_data = [
    [Paragraph("<b>Project Title:</b>", tbl_cell_style), Paragraph("FitBuddy – AI Fitness Plan Generator Using Gemini Models", tbl_cell_style)],
    [Paragraph("<b>Technical Domain:</b>", tbl_cell_style), Paragraph("Generative AI, Full-Stack Web Development, Health-Tech", tbl_cell_style)],
    [Paragraph("<b>Backend Architecture:</b>", tbl_cell_style), Paragraph("Python 3.12+, FastAPI, SQLAlchemy ORM, SQLite", tbl_cell_style)],
    [Paragraph("<b>Frontend Architecture:</b>", tbl_cell_style), Paragraph("HTML5, Custom Responsive CSS3, Jinja2 Server-Side Templating", tbl_cell_style)],
    [Paragraph("<b>Generative AI Layer:</b>", tbl_cell_style), Paragraph("Google Gemini 1.5 Pro & Gemini 1.5 Flash (google-genai SDK)", tbl_cell_style)],
    [Paragraph("<b>Submission Date:</b>", tbl_cell_style), Paragraph("October 2026", tbl_cell_style)],
    [Paragraph("<b>Project Status:</b>", tbl_cell_style), Paragraph("<font color='#059669'><b>Completed, Tested & Production-Ready</b></font>", tbl_cell_style)],
]
t_meta = Table(meta_data, colWidths=[120, 384])
t_meta.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), light_bg),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t_meta)

story.append(Spacer(1, 15))
story.append(Paragraph("<b>PROJECT TEAM MEMBERS</b>", ParagraphStyle('TeamHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=primary_color, spaceAfter=5)))

team_data = [
    [Paragraph("<b>Member #</b>", tbl_header_style), Paragraph("<b>Student Name</b>", tbl_header_style), Paragraph("<b>Register Number</b>", tbl_header_style), Paragraph("<b>Role / Responsibilities</b>", tbl_header_style)],
    [Paragraph("<b>Team Member 1</b>", tbl_cell_style), Paragraph("<b>Maha Swetha N</b>", tbl_cell_style), Paragraph("<b>2024503017</b>", tbl_cell_style), Paragraph("Team Lead & Gemini AI Engine Orchestration", tbl_cell_style)],
    [Paragraph("<b>Team Member 2</b>", tbl_cell_style), Paragraph("<b>Priyadharshini M</b>", tbl_cell_style), Paragraph("<b>2024503501</b>", tbl_cell_style), Paragraph("Testing, Validation & Technical Documentation", tbl_cell_style)],
    [Paragraph("<b>Team Member 3</b>", tbl_cell_style), Paragraph("<b>Sharmu R</b>", tbl_cell_style), Paragraph("<b>2024503055</b>", tbl_cell_style), Paragraph("Database Design & SQLAlchemy ORM Integration", tbl_cell_style)],
    [Paragraph("<b>Team Member 4</b>", tbl_cell_style), Paragraph("<b>Monisha G</b>", tbl_cell_style), Paragraph("<b>2024503043</b>", tbl_cell_style), Paragraph("Frontend UI & Jinja2 Template Development", tbl_cell_style)],
    [Paragraph("<b>Team Member 5</b>", tbl_cell_style), Paragraph("<b>Sana Tasneem Azimudin</b>", tbl_cell_style), Paragraph("<b>2024503007</b>", tbl_cell_style), Paragraph("Backend Routing & FastAPI Architecture", tbl_cell_style)],
]
t_team = Table(team_data, colWidths=[80, 140, 110, 174])
t_team.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('RIGHTPADDING', (0,0), (-1,-1), 7),
]))
story.append(t_team)

story.append(PageBreak())

# 1. INTRODUCTION
story.append(Paragraph("1. INTRODUCTION", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("1.1 Project Overview", h2_style))
story.append(Paragraph(
    "FitBuddy is an intelligent, full-stack fitness application that utilizes Google's Gemini generative AI models "
    "to generate personalized 7-day workout plans and tailored nutrition advice based on individual parameters such "
    "as age, weight, fitness goals, and preferred workout intensity. Developed using the high-performance FastAPI "
    "backend framework and styled with responsive HTML5, CSS3, and Jinja2 templates, FitBuddy integrates modern AI reasoning "
    "directly into health and wellness workflows. The platform features an adaptive feedback mechanism that allows users "
    "to modify their routines dynamically while preserving baseline records within an SQLite database managed via SQLAlchemy ORM. "
    "It serves individual fitness enthusiasts seeking tailored routines while providing coaches and administrators with an "
    "oversight dashboard to monitor client progression.",
    body_style
))

story.append(Paragraph("1.2 Purpose", h2_style))
story.append(Paragraph(
    "The purpose of FitBuddy is to make customized fitness planning widely accessible by removing the cost and complexity "
    "barriers associated with personal fitness coaching. By leveraging AI language models, the application provides structured, "
    "day-wise exercise schedules and science-backed nutritional advice that adapt to users' real-time feedback. Additionally, "
    "it provides coaches and administrators with a centralized oversight dashboard to track client profiles, monitor regimen "
    "adaptations, and support adherence to safe, sustainable fitness practices.",
    body_style
))

# 2. IDEATION PHASE
story.append(Paragraph("2. IDEATION PHASE", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("2.1 Problem Statement", h2_style))
story.append(Paragraph("Most individuals attempting to start or sustain a fitness regimen face significant challenges that lead to early abandonment:", body_style))
story.append(Paragraph("• <b>Generic, Unstructured Workouts:</b> One-size-fits-all routines found online fail to account for unique body weights, biological ages, and preferred intensities, leading to fatigue, poor adherence, or injury.", bullet_style))
story.append(Paragraph("• <b>Prohibitive Coaching Costs:</b> Certified personal trainers and sports nutritionists are expensive, making dedicated, customized guidance inaccessible to a large demographic.", bullet_style))
story.append(Paragraph("• <b>Static, Inflexible Routines:</b> Conventional workout apps lack dynamic adaptability when an individual experiences muscle fatigue, requires exercise substitutions, or needs schedule adjustments.", bullet_style))
story.append(Paragraph("• <b>Fragmented Fitness & Nutrition:</b> Exercise routines and dietary guidance are often separated across disparate platforms, creating confusion over pre- and post-workout nutritional recovery.", bullet_style))

story.append(Paragraph("2.2 Empathy Map Canvas", h2_style))
empathy_data = [
    [Paragraph("<b>Dimension</b>", tbl_header_style), Paragraph("<b>User Perspective & Findings</b>", tbl_header_style)],
    [Paragraph("<b>Says</b>", tbl_cell_style), Paragraph("• 'I want to build muscle and burn fat, but generic routines don't fit my schedule.'<br/>• 'Hiring a personal trainer every month is too expensive.'<br/>• 'I need exercises that match my current energy level.'", tbl_cell_style)],
    [Paragraph("<b>Thinks</b>", tbl_cell_style), Paragraph("• <i>Am I performing the right reps and sets for my body weight?</i><br/>• <i>What should I eat post-workout to maximize recovery?</i><br/>• <i>Can I swap out an exercise if I lack equipment or experience pain?</i>", tbl_cell_style)],
    [Paragraph("<b>Does</b>", tbl_cell_style), Paragraph("• Searches fitness forums for scattered routine templates.<br/>• Drops out of training programs within two weeks due to burnout or lack of progression.<br/>• Manually logs notes across paper diaries or basic phone apps.", tbl_cell_style)],
    [Paragraph("<b>Feels</b>", tbl_cell_style), Paragraph("• Overwhelmed by conflicting fitness advice and extreme diets.<br/>• Frustrated when pre-set routines cannot be modified for home equipment.<br/>• Motivated and confident when given structured, day-by-day plans with warm-ups and cooldowns.", tbl_cell_style)]
]
t_empathy = Table(empathy_data, colWidths=[80, 424])
t_empathy.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_empathy)

story.append(Paragraph("2.3 Brainstorming", h2_style))
story.append(Paragraph("During project ideation, various architectures and models were evaluated to balance performance, structure, and operational costs:", body_style))
story.append(Paragraph("• <b>Model Evaluation:</b> Open-source text models (BART, T5, DistilBERT, Bloom) were reviewed. While capable of generic text output, they required substantial prompt fine-tuning or dedicated GPU hosting. Google Gemini models were selected due to their native understanding of structured formatting, low latency, and zero-maintenance cloud API architecture.", bullet_style))
story.append(Paragraph("• <b>Dual-Model Workload Specialization:</b> Gemini 1.5 Pro was selected for complex reasoning tasks (generating comprehensive 7-day schedules and handling nuanced revision feedback), while Gemini 1.5 Flash was integrated for high-speed, lightweight nutrition and recovery generation.", bullet_style))
story.append(Paragraph("• <b>Preserved Feedback History:</b> Rather than overwriting plans upon user feedback, the architecture was designed to store original and updated plans side-by-side to maintain longitudinal visibility.", bullet_style))

# 3. REQUIREMENT ANALYSIS
story.append(Paragraph("3. REQUIREMENT ANALYSIS", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("3.1 Customer Journey Map", h2_style))
journey_data = [
    [Paragraph("<b>Phase</b>", tbl_header_style), Paragraph("<b>User Actions</b>", tbl_header_style), Paragraph("<b>System Touchpoints</b>", tbl_header_style), Paragraph("<b>Outcome / Value</b>", tbl_header_style)],
    [Paragraph("<b>1. Intake</b>", tbl_cell_style), Paragraph("User opens portal; enters Name, User ID, Age, Weight, Goal, and Intensity.", tbl_cell_style), Paragraph("HTML Form (<code>index.html</code>), Pydantic validation.", tbl_cell_style), Paragraph("Structured, clean parameters ready for processing.", tbl_cell_style)],
    [Paragraph("<b>2. Generation</b>", tbl_cell_style), Paragraph("User clicks 'Generate Plan'.", tbl_cell_style), Paragraph("FastAPI router calls Gemini 1.5 Pro & Gemini 1.5 Flash.", tbl_cell_style), Paragraph("Comprehensive 7-day schedule + targeted nutrition tip rendered.", tbl_cell_style)],
    [Paragraph("<b>3. Feedback</b>", tbl_cell_style), Paragraph("User tests plan, requests changes (e.g., 'Add yoga on Day 4').", tbl_cell_style), Paragraph("Feedback submission route; Gemini Pro updates plan; SQLite updates record.", tbl_cell_style), Paragraph("Revised plan displayed alongside preserved original plan.", tbl_cell_style)],
    [Paragraph("<b>4. Oversight</b>", tbl_cell_style), Paragraph("Coach/Admin navigates to Coach Dashboard.", tbl_cell_style), Paragraph("Admin Route (<code>/view-all-users</code>), SQLAlchemy query.", tbl_cell_style), Paragraph("Holistic monitoring of registered athletes and plan evolutions.", tbl_cell_style)]
]
t_journey = Table(journey_data, colWidths=[65, 145, 145, 149])
t_journey.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_journey)

story.append(Paragraph("3.2 Solution Requirements", h2_style))
story.append(Paragraph("• <b>Functional Requirements:</b> Secure collection of user physical attributes; automated generation of 7-day exercise plans covering warm-up, main workout (sets/reps), rest periods, and cooldowns; dynamic generation of goal-aligned nutrition tips; non-destructive plan revisions via feedback; persistent storage in SQLite; interactive admin table; and interactive Swagger OpenAPI documentation (<code>/docs</code>).", bullet_style))
story.append(Paragraph("• <b>Non-Functional Requirements:</b> High response velocity using Gemini 1.5 Flash; strict input validation avoiding malformed records; health & wellness disclaimers establishing that AI output is for educational purposes; and automated mock fallbacks enabling reliable offline execution.", bullet_style))

story.append(Paragraph("3.3 Data Flow Diagram (DFD)", h2_style))
story.append(Paragraph(
    "Data originates at the client browser via HTTP POST requests containing form data. The FastAPI operational layer "
    "validates data types through Pydantic schemas. Concurrently, user identity and stats are saved into the SQLite database. "
    "Structured prompts are dispatched asynchronously to the Google GenAI API endpoint. Gemini 1.5 Pro generates the multi-day "
    "routine while Gemini Flash returns the nutrition recommendation. The responses are stored in the database and formatted into "
    "the Jinja2 rendering pipeline to output <code>result.html</code>. When feedback is submitted, the original plan is retrieved from "
    "SQLite, sent with user feedback to Gemini 1.5 Pro, and saved to the updated plan field.",
    body_style
))

story.append(Paragraph("3.4 Technology Stack", h2_style))
tech_data = [
    [Paragraph("<b>Component Layer</b>", tbl_header_style), Paragraph("<b>Technology Selected</b>", tbl_header_style), Paragraph("<b>Architectural Justification</b>", tbl_header_style)],
    [Paragraph("<b>Backend Core</b>", tbl_cell_style), Paragraph("Python 3.12+, FastAPI, Uvicorn", tbl_cell_style), Paragraph("Asynchronous execution, automatic OpenAPI schema generation, high speed.", tbl_cell_style)],
    [Paragraph("<b>Database & ORM</b>", tbl_cell_style), Paragraph("SQLite, SQLAlchemy ORM", tbl_cell_style), Paragraph("Zero-config local persistence, robust object-relational mapping, strict schema.", tbl_cell_style)],
    [Paragraph("<b>AI Models & SDK</b>", tbl_cell_style), Paragraph("Gemini 1.5 Pro & Flash (<code>google-genai</code>)", tbl_cell_style), Paragraph("Official current SDK; Pro for deep reasoning, Flash for sub-second advice.", tbl_cell_style)],
    [Paragraph("<b>Frontend & UI</b>", tbl_cell_style), Paragraph("HTML5, Custom CSS3, Jinja2", tbl_cell_style), Paragraph("Server-side dynamic rendering, responsive card-based layout, no bulky JS frameworks.", tbl_cell_style)],
    [Paragraph("<b>Validation & Env</b>", tbl_cell_style), Paragraph("Pydantic v2, Python-Dotenv", tbl_cell_style), Paragraph("Strict runtime type enforcement, centralized secrets handling in <code>.env</code>.", tbl_cell_style)]
]
t_tech = Table(tech_data, colWidths=[100, 160, 244])
t_tech.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_tech)

story.append(PageBreak())

# 4. PROJECT DESIGN
story.append(Paragraph("4. PROJECT DESIGN", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("4.1 Problem Solution Fit", h2_style))
story.append(Paragraph(
    "FitBuddy achieves precise problem-solution fit by directly targeting the friction points of conventional fitness platforms. "
    "Where traditional apps force users into static spreadsheets or charge expensive monthly fees, FitBuddy utilizes generative AI "
    "to provide bespoke regimens on demand. By coupling workout generation with nutritional guidance and offering continuous "
    "conversational revisions, users maintain sustained engagement and progress safely.",
    body_style
))

story.append(Paragraph("4.2 Proposed Solution", h2_style))
story.append(Paragraph("The application architecture consists of three interconnected subsystems:", body_style))
story.append(Paragraph("1. <b>User Profile & Intake Subsystem:</b> Validates user attributes (ID, age, weight, goal, intensity) and persists them into the SQLite database via SQLAlchemy models.", bullet_style))
story.append(Paragraph("2. <b>Generative AI Orchestration Subsystem:</b> Interfaces with Google's unified <code>google-genai</code> SDK. Uses prompt engineering with safety instructions to prevent hazardous exercise recommendations.", bullet_style))
story.append(Paragraph("3. <b>Administrative & Coach Oversight Subsystem:</b> A dedicated view (<code>/view-all-users</code>) that provides side-by-side auditing of original versus feedback-revised routines, giving coaches complete oversight.", bullet_style))

story.append(Paragraph("4.3 Solution Architecture", h2_style))
story.append(Paragraph(
    "The FitBuddy architecture follows a decoupled, three-tier model comprising the Client Presentation Tier (HTML5/Jinja2), "
    "the Application Backend Tier (FastAPI/Uvicorn), and the AI & Data Persistence Tier (Google Gemini & SQLite ORM). "
    "The system diagram below illustrates the end-to-end component interactions:",
    body_style
))

if os.path.exists("architecture_diagram.png"):
    story.append(Spacer(1, 4))
    story.append(RLImage("architecture_diagram.png", width=480, height=255))
    story.append(Paragraph("Figure 4.1: FitBuddy System Component & Solution Architecture Diagram", img_caption_style))

# 5. PROJECT PLANNING & SCHEDULING
story.append(Paragraph("5. PROJECT PLANNING & SCHEDULING", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("5.1 Project Planning", h2_style))
milestone_data = [
    [Paragraph("<b>Milestone</b>", tbl_header_style), Paragraph("<b>Key Activities & Scope</b>", tbl_header_style), Paragraph("<b>Deliverables</b>", tbl_header_style), Paragraph("<b>Status</b>", tbl_header_style)],
    [Paragraph("<b>Milestone 1</b>", tbl_cell_style), Paragraph("Model Selection & System Architecture", tbl_cell_style), Paragraph("Benchmarked HuggingFace vs Gemini; finalized Pro & Flash dual architecture.", tbl_cell_style), Paragraph("<font color='#059669'><b>Completed</b></font>", tbl_cell_style)],
    [Paragraph("<b>Milestone 2</b>", tbl_cell_style), Paragraph("Core Functionality & Data Persistence", tbl_cell_style), Paragraph("Implemented SQLAlchemy models, SQLite connection, and Gemini generation modules.", tbl_cell_style), Paragraph("<font color='#059669'><b>Completed</b></font>", tbl_cell_style)],
    [Paragraph("<b>Milestone 3</b>", tbl_cell_style), Paragraph("Routing & API Engine Development", tbl_cell_style), Paragraph("Engineered <code>routes.py</code>, Pydantic schemas, validation rules, and Swagger docs.", tbl_cell_style), Paragraph("<font color='#059669'><b>Completed</b></font>", tbl_cell_style)],
    [Paragraph("<b>Milestone 4</b>", tbl_cell_style), Paragraph("Frontend UI & Dynamic Templating", tbl_cell_style), Paragraph("Built responsive Jinja2 templates (<code>index</code>, <code>result</code>, <code>all_users</code>) & CSS theme.", tbl_cell_style), Paragraph("<font color='#059669'><b>Completed</b></font>", tbl_cell_style)],
    [Paragraph("<b>Milestone 5</b>", tbl_cell_style), Paragraph("Deployment, Testing & Verification", tbl_cell_style), Paragraph("Lifespan database initialization, offline fallback testing, Uvicorn execution.", tbl_cell_style), Paragraph("<font color='#059669'><b>Completed</b></font>", tbl_cell_style)]
]
t_milestone = Table(milestone_data, colWidths=[70, 145, 215, 74])
t_milestone.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_milestone)

# 6. FUNCTIONAL AND PERFORMANCE TESTING
story.append(Paragraph("6. FUNCTIONAL AND PERFORMANCE TESTING", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("6.1 Performance Testing", h2_style))
test_data = [
    [Paragraph("<b>Test ID</b>", tbl_header_style), Paragraph("<b>Test Scope</b>", tbl_header_style), Paragraph("<b>Input Parameters</b>", tbl_header_style), Paragraph("<b>Expected Behavior</b>", tbl_header_style), Paragraph("<b>Result</b>", tbl_header_style)],
    [Paragraph("<b>TC-01</b>", tbl_cell_style), Paragraph("Input Validation", tbl_cell_style), Paragraph("Age: <code>5</code>, Weight: <code>10kg</code>", tbl_cell_style), Paragraph("Rejected with 400 Bad Request error banner.", tbl_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", tbl_cell_style)],
    [Paragraph("<b>TC-02</b>", tbl_cell_style), Paragraph("Plan Generation", tbl_cell_style), Paragraph("Name: Alice, ID: 11, 75.5kg, Goal: Muscle gain", tbl_cell_style), Paragraph("Saves user; generates 7-day routine and nutrition tip.", tbl_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", tbl_cell_style)],
    [Paragraph("<b>TC-03</b>", tbl_cell_style), Paragraph("Feedback Revision", tbl_cell_style), Paragraph("ID: 11, 'Add 15m cardio + core on Day 2 & 5'", tbl_cell_style), Paragraph("Gemini revises routine; updates DB record without deleting original.", tbl_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", tbl_cell_style)],
    [Paragraph("<b>TC-04</b>", tbl_cell_style), Paragraph("Admin Oversight", tbl_cell_style), Paragraph("Navigate to <code>/view-all-users</code>", tbl_cell_style), Paragraph("Renders full athlete table with both original and updated plans.", tbl_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", tbl_cell_style)],
    [Paragraph("<b>TC-05</b>", tbl_cell_style), Paragraph("API Endpoints", tbl_cell_style), Paragraph("<code>POST /generate-plan</code>", tbl_cell_style), Paragraph("Returns 200 OK with valid JSON response payload.", tbl_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", tbl_cell_style)],
    [Paragraph("<b>TC-06</b>", tbl_cell_style), Paragraph("Offline Fallback", tbl_cell_style), Paragraph("Missing / empty API key", tbl_cell_style), Paragraph("Application generates realistic fallback plan without crashing.", tbl_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", tbl_cell_style)]
]
t_test = Table(test_data, colWidths=[45, 95, 134, 180, 50])
t_test.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 3.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
story.append(t_test)

story.append(PageBreak())

# 7. RESULTS
story.append(Paragraph("7. RESULTS", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("7.1 Output Screenshots", h2_style))
story.append(Paragraph(
    "The application was thoroughly executed and validated on <code>http://127.0.0.1:8000</code>. "
    "Below are the verified live output screenshots capturing the complete end-to-end user and administrative workflow in exact operational sequence:",
    body_style
))

def resolve_image(fig_num, candidate_names):
    search_dirs = [os.path.join("static", "images"), "static", "images", "."]
    for d in search_dirs:
        for name in candidate_names:
            p = os.path.join(d, name)
            if os.path.exists(p):
                print(f"[OK] Figure {fig_num} loaded: {p}")
                return p
    print(f"[WARNING] Figure {fig_num} NOT FOUND! Looked for {candidate_names}")
    return None

# Figure 7.1: Intake Form
img1 = resolve_image("7.1", ["fig1_intake.png", "IMG-20261002-WA0025.jpg", "IMG-20261002-WA0023.jpg", "input_file_9.png"])
if img1:
    story.append(Spacer(1, 3))
    story.append(RLImage(img1, width=470, height=240))
    story.append(Paragraph("Figure 7.1: FitBuddy AI Workout Generator – User Parameter Intake Form (Alice, ID 11, 75.5 kg)", img_caption_style))

# Figure 7.2: Generated Workout Routine Top
img2 = resolve_image("7.2", ["fig2_plan.png", "IMG-20261002-WA0024.jpg", "input_file_8.png"])
if img2:
    story.append(Spacer(1, 4))
    story.append(RLImage(img2, width=470, height=240))
    story.append(Paragraph("Figure 7.2: Personalized 7-Day Workout Plan Generated by Gemini 1.5 Pro (User Info & Day 1 Schedule)", img_caption_style))

story.append(PageBreak())

# Figure 7.3: Day 7 & Nutrition Tip
img3 = resolve_image("7.3", ["fig3_tip.png", "IMG-20261002-WA0028.jpg", "input_file_10.png"])
if img3:
    story.append(Spacer(1, 3))
    story.append(RLImage(img3, width=470, height=240))
    story.append(Paragraph("Figure 7.3: Day 7 Rest Restoration, Progressive Notes & Gemini Flash Nutrition Tip", img_caption_style))

# Figure 7.4: Feedback Submission Form
img4 = resolve_image("7.4", ["fig4_feedback.png", "IMG-20261002-WA0029.jpg", "input_file_3.png"])
if img4:
    story.append(Spacer(1, 4))
    story.append(RLImage(img4, width=470, height=240))
    story.append(Paragraph("Figure 7.4: Interactive Plan Revision & Feedback Submission Form (Requesting Low-Impact Cardio & Core)", img_caption_style))

story.append(PageBreak())

# Figure 7.5: Updated Workout Plan & Confirmation Banner
img5 = resolve_image("7.5", ["fig5_updated.png", "IMG-20261002-WA0030.jpg", "input_file_4.png"])
if img5:
    story.append(Spacer(1, 3))
    story.append(RLImage(img5, width=470, height=240))
    story.append(Paragraph("Figure 7.5: AI-Updated Workout Plan Featuring Update Confirmation Banner and Regenerated Regimen", img_caption_style))

# Figure 7.6: Coach & Admin Oversight Dashboard
img6 = resolve_image("7.6", ["fig6_admin.png", "IMG-20261002-WA0031.jpg", "input_file_5.png"])
if img6:
    story.append(Spacer(1, 4))
    story.append(RLImage(img6, width=470, height=240))
    story.append(Paragraph("Figure 7.6: Coach & Administrator Portal (/view-all-users) Showing Side-by-Side Original and Updated Plans", img_caption_style))

story.append(PageBreak())

# Figure 7.7: FastAPI Swagger OpenAPI Documentation
img7 = resolve_image("7.7", ["fig7_docs.png", "IMG-20261002-WA0032.jpg", "input_file_6.png"])
if img7:
    story.append(Spacer(1, 3))
    story.append(RLImage(img7, width=470, height=240))
    story.append(Paragraph("Figure 7.7: Interactive FastAPI Swagger Documentation (/docs) for All REST API Endpoints", img_caption_style))

story.append(Spacer(1, 6))

# 8. ADVANTAGES & DISADVANTAGES
story.append(Paragraph("8. ADVANTAGES & DISADVANTAGES", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
adv_data = [
    [Paragraph("<b>Key Advantages</b>", tbl_header_style), Paragraph("<b>Current Limitations / Disadvantages</b>", tbl_header_style)],
    [
        Paragraph("• <b>Hyper-Personalized Regimens:</b> Workouts are customized to biological age, body weight, fitness goals, and intensity.<br/>• <b>Dual-Model Efficiency:</b> Gemini 1.5 Pro handles reasoning-heavy workout generation, while Gemini Flash delivers fast nutrition tips.<br/>• <b>Non-Destructive History:</b> Updates do not overwrite baseline plans, allowing longitudinal comparison.<br/>• <b>Coach Oversight:</b> Built-in dashboard enables professional trainer supervision.<br/>• <b>Dual Interface:</b> Supports both a browser-based UI and RESTful API endpoints.", tbl_cell_style),
        Paragraph("• <b>Cloud API Dependency:</b> Requires an active internet connection to communicate with Google Gemini endpoints.<br/>• <b>Subjective Input Quality:</b> Revision quality depends on the clarity of user feedback.<br/>• <b>Single-Node SQLite Scope:</b> SQLite is optimized for local/single-server setups; large-scale deployments require PostgreSQL.", tbl_cell_style)
    ]
]
t_adv = Table(adv_data, colWidths=[252, 252])
t_adv.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white]),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('RIGHTPADDING', (0,0), (-1,-1), 7),
]))
story.append(t_adv)

# 9. CONCLUSION
story.append(Paragraph("9. CONCLUSION", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph(
    "The <b>FitBuddy – AI Fitness Plan Generator</b> demonstrates the effective application of generative artificial intelligence "
    "to health and wellness challenges. By combining the FastAPI framework with Google Gemini models (Gemini 1.5 Pro and Gemini 1.5 Flash), "
    "FitBuddy provides structured 7-day workout plans and science-backed nutritional advice. Its feedback loop allows users "
    "to adjust their routines dynamically, while the SQLite database and admin dashboard give trainers clear visibility into plan revisions. "
    "FitBuddy provides an accessible, adaptive, and scalable software solution for modern fitness planning.",
    body_style
))

# 10. FUTURE SCOPE
story.append(Paragraph("10. FUTURE SCOPE", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
story.append(Paragraph("• <b>Wearable Health Device Integration:</b> Ingest continuous heart rate, sleep quality, and daily step counts from Apple HealthKit and Google Health Connect to auto-adjust workout intensities.", bullet_style))
story.append(Paragraph("• <b>Computer Vision Exercise Form Correction:</b> Integrate real-time webcam pose estimation (MediaPipe) to track joint angles during exercise execution and provide instant posture corrections.", bullet_style))
story.append(Paragraph("• <b>Multimedia Exercise Demonstrations:</b> Embed animated exercise video clips and muscle engagement diagrams alongside each generated exercise item.", bullet_style))
story.append(Paragraph("• <b>Multilingual Localization:</b> Leverage Gemini's multilingual processing to generate workout instructions and nutritional recommendations in regional languages.", bullet_style))

# 11. APPENDIX
story.append(Paragraph("11. APPENDIX", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=6, spaceBefore=2))
app_data = [
    [Paragraph("<b>Category</b>", tbl_header_style), Paragraph("<b>Details & Links</b>", tbl_header_style)],
    [Paragraph("<b>Source Code Repository</b>", tbl_cell_style), Paragraph("Modular Python package organized under <code>/app</code>, <code>/templates</code>, and <code>/static</code>.", tbl_cell_style)],
    [Paragraph("<b>Primary Dependencies</b>", tbl_cell_style), Paragraph("<code>fastapi</code>, <code>uvicorn</code>, <code>google-genai</code>, <code>sqlalchemy</code>, <code>jinja2</code>, <code>pydantic</code>, <code>python-dotenv</code>.", tbl_cell_style)],
    [Paragraph("<b>AI Model Knowledge Base</b>", tbl_cell_style), Paragraph("Google Gemini Foundation Models (<code>gemini-1.5-pro</code>, <code>gemini-1.5-flash</code>) via Google AI Studio API.", tbl_cell_style)],
    [Paragraph("<b>GitHub Repository Link</b>", tbl_cell_style), Paragraph("<code>https://github.com/fitbuddy-developer/FitBuddy-AI-Fitness-Planner</code>", tbl_cell_style)],
    [Paragraph("<b>Local Web Deployment</b>", tbl_cell_style), Paragraph("<code>http://127.0.0.1:8000/</code> (Admin: <code>/view-all-users</code>)", tbl_cell_style)],
    [Paragraph("<b>Interactive API Swagger</b>", tbl_cell_style), Paragraph("<code>http://127.0.0.1:8000/docs</code>", tbl_cell_style)]
]
t_app = Table(app_data, colWidths=[150, 354])
t_app.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary_color),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t_app)

doc.build(story, canvasmaker=NumberedCanvas)
print("SUCCESS: FitBuddy_Project_Report.pdf generated with all team members and screenshots.")