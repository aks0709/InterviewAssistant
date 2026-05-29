"""Clear all data and reset panels for fresh start."""
from app.models.database import SessionLocal, Candidate, Interview, Panel

def reset_database():
    """Clear all candidates and interviews, reset panel busy_until to NULL."""
    db = SessionLocal()
    try:
        # Delete all interviews
        interview_count = db.query(Interview).delete()
        print(f"Deleted {interview_count} interviews")
        
        # Delete all candidates
        candidate_count = db.query(Candidate).delete()
        print(f"Deleted {candidate_count} candidates")
        
        # Reset all panels (set busy_until to NULL)
        panels = db.query(Panel).all()
        for panel in panels:
            panel.busy_until = None
            print(f"Reset panel: {panel.name}")
        
        db.commit()
        print("\n[OK] Database reset complete!")
        print(f"[OK] All panels are now available")
        
    except Exception as e:
        print(f"[ERROR] Reset failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()
