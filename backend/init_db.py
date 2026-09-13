"""
CLI script to initialize database tables and seed data.
"""

from app.db.init_db import init_db

if __name__ == "__main__":
    print("Running LearnMate Database Initialization...")
    init_db(seed_data=True)
    print("Database initialization complete.")
