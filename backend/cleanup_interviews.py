"""Clean up duplicate interview entries - keep only the first interview per candidate."""
from app.models.database import SessionLocal, Interview
from sqlalchemy import func

def cleanup_duplicate_interviews():
    """Remove duplicate interviews, keeping only the first one for each candidate."""
    db = SessionLocal()
    try:
        # Get all interviews grouped by candidate_id
        interviews = db.query(Interview).order_by(Interview.candidate_id, Interview.id).all()
        
        seen_candidates = set()
        deleted_count = 0
        
        for interview in interviews:
            if interview.candidate_id in seen_candidates:
                # Duplicate - delete it
                print(f"Deleting duplicate interview ID {interview.id} for candidate {interview.candidate_id} ({interview.candidate_name})")
                db.delete(interview)
                deleted_count += 1
            else:
                # First interview for this candidate - keep it
                seen_candidates.add(interview.candidate_id)
                print(f"Keeping interview ID {interview.id} for candidate {interview.candidate_id} ({interview.candidate_name}) with panel {interview.panel_name}")
        
        db.commit()
        print(f"\n[OK] Cleanup complete: Deleted {deleted_count} duplicate interviews")
        print(f"[OK] Remaining interviews: {len(seen_candidates)}")
        
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicate_interviews()
