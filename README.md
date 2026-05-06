# 🎓 PathWise — AI-Powered Personalized Learning Path Recommendation System

A fully functional, production-ready Flask web application that generates personalized learning paths using a **Hybrid CBR (Case-Based Reasoning) + RBR (Rule-Based Reasoning)** engine powered by **Sentence-BERT** embeddings.

---

## 🏗️ Architecture Overview

```
User Input (Profile + Quiz)
         │
         ▼
   ┌─────────────┐
   │  BERT NLP   │  ← Encode learning goal → embedding
   │  (Sentence  │  ← Classify domain (cybersecurity, data science, etc.)
   │  Transformers)
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  CBR Engine │  ← Compute similarity against case base
   │             │    Sim_total = α·Σ(wf·Sim_f) + (1-α)·Sim_BERT
   │  Top-K=2    │  ← Retrieve top-2 similar past learner cases
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  RBR Engine │  ← Apply 12 rules:
   │             │    - beginner → remove advanced modules
   │             │    - short memory → add revision modules
   │             │    - non-tech → prepend fundamentals
   │             │    - quiz ≥ 50 → skip beginner modules
   │             │    - etc.
   └──────┬──────┘
          │
          ▼
   Personalized Learning Path (5–12 ordered modules)
```

---

## 📁 File Structure

```
learning_path_app/
│
├── app.py                          # Flask app factory + entry point
├── config.py                       # Config classes (Dev/Prod/Test)
├── requirements.txt
├── README.md
│
├── models/                         # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── database.py                 # db = SQLAlchemy()
│   ├── user.py                     # User (auth)
│   ├── profile.py                  # LearnerProfile
│   ├── course.py                   # Course + Module
│   ├── learning_path.py            # LearningPath + LearningPathModule
│   ├── progress.py                 # Progress + ModuleAssessment
│   └── case_base.py                # CBR Case Base
│
├── routes/                         # Flask Blueprints (MVC controllers)
│   ├── __init__.py
│   ├── auth.py                     # /auth/login, /auth/signup, /auth/logout
│   ├── profile.py                  # /profile/create, /profile/quiz
│   ├── learning_path.py            # /path/generate, /path/<id>, etc.
│   └── dashboard.py                # / and /dashboard
│
├── recommender/                    # ML / AI core
│   ├── __init__.py                 # LearningPathRecommender orchestrator
│   ├── bert_model.py               # Sentence-BERT wrapper + domain classifier
│   ├── similarity.py               # All CBR similarity functions
│   ├── cbr.py                      # CBR: Retrieve + Reuse
│   └── rbr.py                      # RBR: 12 rule engine
│
├── utils/
│   ├── __init__.py
│   ├── certificate.py              # ReportLab PDF certificate generator
│   └── quiz.py                     # Quiz generator + scorer
│
├── data/
│   ├── __init__.py
│   └── seed_data.py                # Synthetic courses, modules, cases
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Base layout with nav + alerts
│   ├── auth/
│   │   ├── login.html
│   │   └── signup.html
│   ├── profile/
│   │   ├── create.html             # Profile form (5 attribute selectors)
│   │   └── quiz.html               # Domain quiz (4 domain + 3 CS questions)
│   ├── dashboard/
│   │   └── home.html               # Main dashboard
│   └── learning_path/
│       ├── view.html               # Path view with all modules
│       ├── module.html             # Module content + assessment
│       └── certificate.html        # Completion certificate with confetti
│
└── static/
    ├── css/app.css
    ├── js/app.js
    └── certificates/               # Generated PDF certificates
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- pip
- (Optional) virtualenv

### 1. Clone / Extract the project

```bash
cd learning_path_app
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** First run downloads the Sentence-BERT model (~90MB). Subsequent runs use the cached version.
> If BERT is unavailable, the system automatically falls back to TF-IDF-based embeddings.

### 4. Run the application

```bash
python app.py
```

The app will:
1. Create the SQLite database at `instance/learning_path.db`
2. Seed 28 courses, ~120 modules, and 15 synthetic CBR cases
3. Start the Flask dev server at `http://localhost:5000`

### 5. Open in browser

```
http://localhost:5000
```

---

## 🔄 User Journey

```
1. Sign Up / Login
        ↓
2. Profile Form
   - Persona: college student / professional / job seeker / explorer
   - Learning Goal: free text (BERT encodes + classifies domain)
   - Skill Level: beginner / intermediate / expert
   - Background: tech / non-tech
   - Memory Capacity: short / medium / long
   - Learning Style: theory / video / labs / project / mixed
        ↓
3. Knowledge Quiz
   - 4 domain-specific questions (cybersecurity, data science, etc.)
   - 3 computer knowledge questions
   - Score < 50% → beginner path
   - Score ≥ 50% → intermediate path
        ↓
4. [Generate Path Button]
   - CBR finds top-2 similar past learners
   - RBR applies 12 personalization rules
   - Returns 5–12 ordered modules
        ↓
5. Learning Path
   - View ordered modules with type, difficulty, duration
   - Click module → view content + take assessment
   - Complete assessment → unlock next module
        ↓
6. Certificate
   - All modules complete → PDF certificate generated
   - New learner case stored in CBR case base
```

---

## 🧮 CBR Similarity Formula

```
Sim_total(u, c) = α × Σ(wf × Sim_f(u, c))  +  (1 - α) × Sim_BERT(u, c)

Where:
  α = 0.7 (tunable in config.py)
  wf = persona-based feature weights (config.py → PERSONA_WEIGHTS)

Feature similarities:
  - Skill Level    → Ordinal:     1 - |idx_u - idx_c| / 2
  - Memory         → Ordinal:     1 - |idx_u - idx_c| / 2
  - Learning Style → Ordinal:     1 - |idx_u - idx_c| / 4
  - Background     → Jaccard:     |u ∩ c| / |u ∪ c|
  - Goal Domain    → Jaccard:     |u ∩ c| / |u ∪ c|
  - Quiz Score     → Numerical:   1 - |score_u - score_c| / 100
  - Persona        → Categorical: 1 if equal, else 0
  - Learning Goal  → BERT cosine similarity of embeddings
```

---

## 🔧 RBR Rules Engine (12 Rules)

| Priority | Rule | Condition | Action |
|----------|------|-----------|--------|
| 1 | remove_advanced_for_beginner | skill == beginner | Remove advanced modules |
| 1 | remove_beginner_for_expert | skill == expert | Remove beginner modules |
| 2 | skip_beginner_if_quiz_passed | quiz_score ≥ 50 | Remove beginner modules |
| 2 | add_fundamentals_for_non_tech | background == non_tech | Prepend intro modules |
| 3 | add_revision_for_short_memory | memory == short | Insert revision every 3 modules |
| 3 | prioritize_video_modules | style == video | Sort video modules first |
| 3 | prioritize_lab_modules | style == labs | Sort lab modules first |
| 3 | prioritize_theory_modules | style == theory | Sort theory modules first |
| 4 | focus_practical_for_job_seeker | persona == job_seeker | Sort project/lab first |
| 5 | limit_for_professional | persona == professional | Cap at 8 high-value modules |
| 6 | add_capstone_for_long_memory | memory == long | Append capstone project |
| 10 | sort_by_difficulty_progression | always | Sort: beginner→intermediate→advanced |

---

## 🗄️ Database Schema

```
users               → id, username, email, password_hash, full_name
learner_profiles    → user_id, persona, learning_goal, skill_level, background,
                      memory_capacity, learning_style, goal_embedding_json,
                      quiz_score, prior_knowledge, goal_domain
courses             → id, title, category, difficulty, duration_hrs, format_type
modules             → id, course_id, title, module_type, difficulty, duration_min,
                      domain, assessment_questions_json
learning_paths      → id, user_id, title, domain, total_modules, estimated_hours,
                      cbr_cases_used_json, rbr_rules_applied_json, status
learning_path_modules → learning_path_id, module_id, order_index, is_completed, is_locked
progress            → user_id, learning_path_id, modules_completed, average_score
module_assessments  → user_id, module_id, score, answers_json, passed
case_base           → id, persona, learning_goal, skill_level, background,
                      memory_capacity, learning_style, quiz_score,
                      goal_embedding_json, path_module_ids_json
```

---

## ⚙️ Configuration (config.py)

```python
CBR_ALPHA = 0.7          # Feature vs BERT similarity balance
CBR_TOP_K = 2            # Number of similar cases to retrieve
CBR_MIN_SIMILARITY = 0.3 # Minimum similarity threshold
QUIZ_PASS_THRESHOLD = 50 # Score ≥ 50 → intermediate path
BERT_MODEL_NAME = 'all-MiniLM-L6-v2'  # Sentence-BERT model
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9+, Flask 3.0 |
| Database | SQLite (SQLAlchemy ORM) |
| ML / NLP | Sentence-BERT (all-MiniLM-L6-v2) |
| Recommendation | Custom CBR + RBR engine |
| Auth | Flask-Login + Flask-Bcrypt |
| PDF | ReportLab |
| Frontend | Vanilla HTML/CSS/JS (no framework) |
| Fonts | Syne + DM Sans (Google Fonts) |

---

## 🔁 Extending the System

- **Add new rules:** Extend `rbr.py → _register_default_rules()`
- **Add new domains:** Extend `bert_model.py → DOMAIN_KEYWORDS`
- **Add new quiz questions:** Extend `utils/quiz.py → DOMAIN_QUESTIONS`
- **Add real courses:** Seed `data/seed_data.py → SAMPLE_COURSES`
- **Switch to PostgreSQL:** Change `SQLALCHEMY_DATABASE_URI` in `.env`
- **Tune CBR:** Adjust `CBR_ALPHA`, `CBR_TOP_K`, `PERSONA_WEIGHTS` in `config.py`
