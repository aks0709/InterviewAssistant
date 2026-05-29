"""
Database migration: Add overlapping_skills column to candidates table

Run this script to update existing database:
python backend/migrate_add_skills.py
"""
import sys
from sqlalchemy import text
from app.models.database import engine

def migrate():
    """Add overlapping_skills column to candidates table."""
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='candidates' AND column_name='overlapping_skills'
            """))
            
            if result.fetchone():
                print("Column 'overlapping_skills' already exists. Skipping migration.")
                return
            
            # Add column
            conn.execute(text("""
                ALTER TABLE candidates 
                ADD COLUMN overlapping_skills TEXT
            """))
            conn.commit()
            
            print("✓ Successfully added 'overlapping_skills' column to candidates table")
            
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
