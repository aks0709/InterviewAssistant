"""Delete last candidate entry from database."""
from app.models.database import SessionLocal, Candidate

def delete_last_candidate():
    """Delete the most recent candidate entry."""
    db = SessionLocal()
    try:
        # Get last candidate (highest ID)
        last_candidate = db.query(Candidate).order_by(Candidate.id.desc()).first()
        
        if last_candidate:
            print(f"Deleting candidate: ID={last_candidate.id}, Name={last_candidate.name}, Email={last_candidate.email}")
            db.delete(last_candidate)
            db.commit()
            print("[OK] Last candidate deleted successfully")
        else:
            print("[INFO] No candidates found in database")
            
    except Exception as e:
        print(f"[ERROR] Failed to delete candidate: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    delete_last_candidate()
