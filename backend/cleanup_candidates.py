"""Clean up duplicate candidate entries - keep only the first candidate per email."""
from app.models.database import SessionLocal, Candidate

def cleanup_duplicate_candidates():
    """Remove duplicate candidates with same email, keeping only the first one."""
    db = SessionLocal()
    try:
        # Get all candidates ordered by email and id
        candidates = db.query(Candidate).order_by(Candidate.email, Candidate.id).all()
        
        seen_emails = {}
        deleted_count = 0
        
        for candidate in candidates:
            if candidate.email in seen_emails:
                # Duplicate - delete it
                print(f"Deleting duplicate candidate ID {candidate.id}: {candidate.name} ({candidate.email})")
                db.delete(candidate)
                deleted_count += 1
            else:
                # First candidate with this email - keep it
                seen_emails[candidate.email] = candidate.id
                print(f"Keeping candidate ID {candidate.id}: {candidate.name} ({candidate.email})")
        
        db.commit()
        print(f"\n[OK] Cleanup complete: Deleted {deleted_count} duplicate candidates")
        print(f"[OK] Remaining candidates: {len(seen_emails)}")
        
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicate_candidates()
