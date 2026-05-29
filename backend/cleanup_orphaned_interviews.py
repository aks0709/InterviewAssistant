"""Clean up orphaned interviews - delete interviews for candidates that no longer exist."""
from app.models.database import SessionLocal, Candidate, Interview

def cleanup_orphaned_interviews():
    """Remove interviews that reference non-existent candidates."""
    db = SessionLocal()
    try:
        # Get all interviews
        interviews = db.query(Interview).all()
        
        deleted_count = 0
        
        for interview in interviews:
            # Check if candidate exists
            candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()
            
            if not candidate:
                # Orphaned interview - delete it
                print(f"Deleting orphaned interview ID {interview.id} for non-existent candidate {interview.candidate_id} ({interview.candidate_name})")
                db.delete(interview)
                deleted_count += 1
            else:
                print(f"Keeping interview ID {interview.id} for candidate {interview.candidate_id} ({interview.candidate_name})")
        
        db.commit()
        print(f"\n[OK] Cleanup complete: Deleted {deleted_count} orphaned interviews")
        
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_orphaned_interviews()
