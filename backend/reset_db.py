"""Reset database with new schema including overlapping_skills column."""
from app.models.database import Base, engine, SessionLocal, Panel, Candidate
from sqlalchemy import text

def reset_db():
    """Drop all tables and recreate with new schema."""
    print("WARNING: This will delete all existing data!")
    print("Dropping all tables...")
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("[OK] All tables dropped")
        
        # Recreate all tables with new schema
        print("Creating tables with new schema...")
        Base.metadata.create_all(bind=engine)
        print("[OK] Tables created successfully!")
        
        # Seed initial panels
        db = SessionLocal()
        try:
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
            print(f"[OK] Added {len(panels)} panels to database")
            
            print("")
            print("[SUCCESS] Database reset complete!")
            print("You can now use Agent 1, 2, and 3 with the new schema.")
            
        except Exception as e:
            print(f"[ERROR] Error seeding data: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Error resetting database: {e}")

if __name__ == "__main__":
    reset_db()
