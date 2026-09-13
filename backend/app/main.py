"""
LearnMate Backend — FastAPI Application Factory.

Configures CORS, registers all 12 API route groups:
1.  /api/student
2.  /api/goals
3.  /api/performance
4.  /api/gaps
5.  /api/resources
6.  /api/calendar
7.  /api/activities
8.  /api/assessments
9.  /api/plan
10. /api/agent
11. /api/replan
12. /api/verification
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    health,
    student,
    goals,
    performance,
    gaps,
    resources,
    calendar,
    activities,
    assessments,
    plan,
    agent,
    replan,
    verification,
    simulation,
    ai,
    adaptive_practice,
    auth,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LearnMate Autonomous Learning Planner API",
        description="Autonomous Learning Planner backend with continuous performance analysis, gap detection, dynamic replanning, and deadline verification.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS for React frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "*",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API groups
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(student.router, prefix="/api/student", tags=["Student"])
    app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
    app.include_router(performance.router, prefix="/api/performance", tags=["Performance"])
    app.include_router(gaps.router, prefix="/api/gaps", tags=["Knowledge Gaps"])
    app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])
    app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
    app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
    app.include_router(assessments.router, prefix="/api/assessments", tags=["Assessments"])
    app.include_router(plan.router, prefix="/api/plan", tags=["Learning Plan"])
    app.include_router(agent.router, prefix="/api/agent", tags=["Autonomous Agent"])
    app.include_router(replan.router, prefix="/api/replan", tags=["Autonomous Replan"])
    app.include_router(verification.router, prefix="/api/verification", tags=["Plan Verification"])
    app.include_router(simulation.router, prefix="/api/simulation", tags=["Demo Simulation"])
    app.include_router(ai.router, prefix="/api/ai", tags=["AI Reasoning"])
    app.include_router(adaptive_practice.router, prefix="/api/practice/adaptive", tags=["Adaptive Practice"])
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

    return app


app = create_app()
