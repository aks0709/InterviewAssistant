"""Database initialization script for Agent 2."""
from app.models.database import Base, engine, SessionLocal, Panel, Candidate
from datetime import datetime

def init_db():
    """Create all tables and seed initial data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    # Seed initial panels
    db = SessionLocal()
    try:
        # Check if panels already exist
        existing_panels = db.query(Panel).count()
        if existing_panels == 0:
            print("Seeding initial panel data...")
            panels = [
                Panel(name="John Smith", email="john.smith@company.com", expertise="Java/Backend"),
                Panel(name="Sarah Johnson", email="sarah.j@company.com", expertise="Python/ML"),
                Panel(name="Mike Chen", email="mike.chen@company.com", expertise="Frontend/React"),
                Panel(name="Emily Davis", email="emily.d@company.com", expertise="DevOps/Cloud"),
                Panel(name="Robert Wilson", email="robert.w@company.com", expertise="Full Stack")
            ]
            db.add_all(panels)
            db.commit()
            print(f"Added {len(panels)} panels to database")
        else:
            print(f"Database already has {existing_panels} panels")
        
        # Check candidates
        existing_candidates = db.query(Candidate).count()
        print(f"Database has {existing_candidates} candidates")
        
    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()