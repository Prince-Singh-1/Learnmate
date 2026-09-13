# 🎓 LearnMate — Autonomous Learning Planner

LearnMate is an AI-powered system that **continuously** monitors student performance, detects knowledge gaps, curates personalized learning resources, and optimizes study schedules — automatically replanning when progress or availability drifts.

> **This is NOT a simple study timetable.** LearnMate operates as a closed-loop autonomous agent that dynamically adapts and verifies learning paths to guarantee deadline achievement.

---

## ✨ The 10-Step Autonomous Learning Loop

LearnMate's closed feedback loop continuously executes:

1. **Analyze Student Performance** — Calculates mastery percentages across topics and identifies score trajectories.
2. **Detect Knowledge Gaps** — Compares mastery against benchmark targets; classifies gaps into High, Medium, and Low severity.
3. **Match Learning Resources** — Curates high-yield videos, cheat sheets, practice problem sets, and interactive tools.
4. **Check Study Time Availability** — Queries calendar slots for open study windows and avoids conflicting commitments.
5. **Formulate Personalized Plan** — Balances daily cognitive load and schedules prioritized activities.
6. **Track Activities** — Records completions and missed sessions in real-time.
7. **Reassess Progress** — Evaluates performance gains and updates mastery curves.
8. **Detect Drift** — Identifies schedule slippage or concept regression.
9. **Autonomous Replan** — Automatically rebalances unfinished tasks into upcoming free windows.
10. **Verify Plan & Deadline Guarantee** — Mathematically confirms that the updated plan satisfies target deadlines and coverage.

---

## 🛠️ Tech Stack

### Frontend
- **React 19** + **TypeScript** — Component-driven reactive UI
- **Vite** — High-speed dev server and production bundler
- **Tailwind CSS v4** — Utility-first ambient design system
- **shadcn/ui** — Accessible UI primitives
- **Framer Motion** — Smooth micro-animations and modal transitions
- **Recharts** — Responsive weekly trend lines and mastery bar charts
- **Lucide React** — Icon suite

### Backend
- **Python** + **FastAPI** — Asynchronous RESTful API framework
- **Pydantic v2** — Request/response data validation schemas
- **SQLAlchemy 2.0** — Engine-agnostic ORM (SQLite / PostgreSQL)
- **Uvicorn** — ASGI production server

---

## 📁 Project Structure

```
learnmate/
├── frontend/                     # React application
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── ui/               # shadcn/ui primitives (card, button, dialog)
│   │   │   ├── layout/           # Sidebar, Header, Navigation
│   │   │   └── dashboard/        # Interactive widgets (AI card, replan modal, charts)
│   │   ├── pages/                # Route-level views (Dashboard, Plan, Performance, Goals)
│   │   ├── data/                 # Centralized mock data models
│   │   ├── lib/                  # API client supporting all 12 API groups
│   │   └── types/                # TypeScript type definitions
│   └── package.json
│
├── backend/                      # FastAPI application
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py           # Service dependency injection
│   │   │   └── routes/           # 12 API Group routers
│   │   │       ├── student.py    # /api/student
│   │   │       ├── goals.py      # /api/goals
│   │   │       ├── performance.py# /api/performance
│   │   │       ├── gaps.py       # /api/gaps
│   │   │       ├── resources.py  # /api/resources
│   │   │       ├── calendar.py   # /api/calendar
│   │   │       ├── activities.py # /api/activities
│   │   │       ├── assessments.py# /api/assessments
│   │   │       ├── plan.py       # /api/plan
│   │   │       ├── agent.py      # /api/agent
│   │   │       ├── replan.py     # /api/replan
│   │   │       └── verification.py# /api/verification
│   │   ├── services/             # Dedicated business logic layer
│   │   │   ├── student_service.py
│   │   │   ├── activity_service.py
│   │   │   ├── performance_analyzer.py
│   │   │   ├── gap_detector.py
│   │   │   ├── resource_recommender.py
│   │   │   ├── schedule_engine.py
│   │   │   ├── plan_generator.py
│   │   │   ├── replanner.py
│   │   │   └── plan_verifier.py
│   │   ├── agent/
│   │   │   └── learning_agent.py # 10-step autonomous loop orchestrator
│   │   ├── models/               # 17 SQLAlchemy domain models
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── mock/                 # Deterministic in-memory state store
│   │   └── db/                   # Database engine, session, and init_db script
│   ├── init_db.py                # Database CLI initializer
│   ├── test_api_endpoints.py     # 30-endpoint API verification suite
│   ├── test_models.py            # 77-test SQLAlchemy model suite
│   └── requirements.txt
│
├── docs/                         # Documentation
│   └── architecture.md           # System architecture, data flow & model ER diagram
│
└── README.md                     # This file
```

---

## 🚀 Getting Started

### 1. Backend Setup

```bash
cd backend

# Activate existing virtual environment (Windows)
.\venv\Scripts\activate

# Initialize Database Schema & Seed Data
python init_db.py

# Run FastAPI Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Server: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies (if not already done)
npm install

# Start Vite Development Server
npm run dev
```
- Frontend Dashboard: `http://localhost:5173`

---

## 🧪 Testing & Verification

Both test suites are automated and verify end-to-end functionality:

```bash
cd backend

# Run Model Test Suite (77 tests covering all 17 models)
python test_models.py

# Run API Test Suite (30 tests covering all 12 API groups)
python test_api_endpoints.py
```

---

## 📖 Complete Documentation

For detailed architecture diagrams, module interaction sequences, ER diagrams, and endpoint specifications, see [docs/architecture.md](docs/architecture.md).
