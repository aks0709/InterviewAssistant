"""Helper script to add test candidates."""
from app.models.database import SessionLocal, Candidate

def add_test_candidate(name: str, email: str, score: int, status: str = "shortlisted"):
    """Add a test candidate to database."""
    db = SessionLocal()
    try:
        candidate = Candidate(
            name=name,
            email=email,
            phone="+1234567890",
            resume_path="/uploads/resume.pdf",
            similarity_score=score,
            status=status
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        print(f"Added candidate: {candidate.name} (ID: {candidate.id}, Status: {candidate.status})")
        return candidate.id
    except Exception as e:
        print(f"Error adding candidate: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding test candidates...")
    add_test_candidate("Alice Johnson", "alice.j@email.com", 85, "shortlisted")
    add_test_candidate("Bob Smith", "bob.s@email.com", 78, "shortlisted")
    add_test_candidate("Charlie Brown", "charlie.b@email.com", 92, "shortlisted")
    print("Test candidates added!")