"""Agent 3 Service: Interview Question Generator using Gemini 2.5 Flash (new SDK)"""
import logging
import json
from typing import List, Dict, Optional
from google import genai
from google.genai import types
from app.config import settings

logger = logging.getLogger(__name__)

class Agent3Service:
    def __init__(self):
        """Initialize Agent 3 with new google-genai SDK."""
        api_key = settings.GOOGLE_API_KEY
        if not api_key or api_key == "placeholder_key":
            raise ValueError("GOOGLE_API_KEY not configured in .env file")
        
        # Initialize new SDK client
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        logger.info(f"Agent3Service initialized with new SDK, model: {self.model_name}")
    
    def generate_questions(
        self, 
        overlapping_skills: List[str], 
        custom_requirements: Optional[str] = None
    ) -> Dict:
        """Generate interview questions based on overlapping skills."""
        if not overlapping_skills:
            raise ValueError("No overlapping skills provided")
        
        logger.info(f"Generating questions for skills: {overlapping_skills}")
        
        prompt = self._build_prompt(overlapping_skills, custom_requirements)
        
        try:
            # Use new SDK to generate content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            # Extract text from response
            response_text = response.text
            questions = self._parse_response(response_text)
            
            # Validate 15 questions (5 each)
            if (len(questions.get('easy', [])) != 5 or 
                len(questions.get('medium', [])) != 5 or 
                len(questions.get('hard', [])) != 5):
                logger.warning(f"Expected 15 questions, got {len(questions.get('easy', []))} easy, "
                             f"{len(questions.get('medium', []))} medium, {len(questions.get('hard', []))} hard")
            
            logger.info(f"Generated {len(questions.get('easy', []))} easy, "
                       f"{len(questions.get('medium', []))} medium, "
                       f"{len(questions.get('hard', []))} hard questions using {self.model_name}")
            
            return {
                "questions": questions,
                "skills": overlapping_skills,
                "custom_requirements": custom_requirements,
                "model_used": self.model_name
            }
            
        except Exception as e:
            logger.error(f"Error generating questions with {self.model_name}: {str(e)}")
            raise Exception(f"Failed to generate questions: {str(e)}")
    
    def _build_prompt(self, skills: List[str], custom_requirements: Optional[str]) -> str:
        """Build prompt for question generation."""
        skills_str = ", ".join(skills)
        
        prompt = f"""You are an expert technical interviewer. Generate interview questions based on the following skills that overlap between the job description and candidate's resume.

**Skills to focus on:** {skills_str}

**Requirements:**
1. Generate exactly 5 EASY questions (basic concepts, definitions, simple scenarios)
2. Generate exactly 5 MEDIUM questions (practical application, problem-solving, moderate complexity)
3. Generate exactly 5 HARD questions (advanced concepts, system design, complex scenarios, edge cases)

4. Questions should be:
   - Relevant to the specific skills listed
   - Progressive in difficulty
   - Practical and realistic for actual interviews
   - Clear and unambiguous
   - Cover different aspects of each skill

"""
        
        if custom_requirements:
            prompt += f"""
**Additional Requirements from Interviewer:**
{custom_requirements}

Please incorporate these specific requirements into the questions.

"""
        
        prompt += """
**Output Format (JSON):**
```json
{
  "easy": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ],
  "medium": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ],
  "hard": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ]
}
```

Generate ONLY the JSON output, no additional text."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, List[str]]:
        """Parse LLM response to extract questions."""
        try:
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            questions = json.loads(text)
            
            if not all(key in questions for key in ["easy", "medium", "hard"]):
                raise ValueError("Missing difficulty levels in response")
            
            for level in ["easy", "medium", "hard"]:
                if not isinstance(questions[level], list):
                    raise ValueError(f"{level} questions must be a list")
            
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {
                "easy": ["Error generating questions. Please try again."],
                "medium": ["Error generating questions. Please try again."],
                "hard": ["Error generating questions. Please try again."]
            }
