"""Improved Gemini-based skills extraction with atomic matching."""
import json
import logging
import re
from typing import Dict, List, Set

logger = logging.getLogger(__name__)

class SkillsExtractor:
    """Extract structured skills with atomic matching and proper model handling."""
    
    def __init__(self):
        self.synonym_map = {
            "spring": "spring-boot",
            "postgres": "postgresql",
            "postgresql": "postgresql",
            "js": "javascript",
            "ts": "typescript",
            "k8s": "kubernetes",
            "docker": "docker",
            "aws": "aws",
            "gcp": "google-cloud",
            "azure": "microsoft-azure",
            "golang": "go"
        }
        
        # Curated whitelist for fallback
        self.skill_whitelist = {
            "languages": ["java", "python", "javascript", "typescript", "c++", "c#", "go", "rust", "kotlin", "scala", "ruby", "php", "swift"],
            "frameworks": ["spring-boot", "spring", "react", "angular", "vue", "django", "flask", "express", "fastapi", "nest", "laravel"],
            "databases": ["postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra", "dynamodb", "oracle", "sql-server"],
            "cloud": ["aws", "azure", "google-cloud", "gcp", "heroku", "digitalocean"],
            "devops": ["docker", "kubernetes", "jenkins", "gitlab", "github-actions", "terraform", "ansible", "circleci"],
            "tools": ["git", "maven", "gradle", "npm", "webpack", "vite", "jira", "confluence"],
            "testing": ["junit", "mockito", "selenium", "jest", "cypress", "pytest", "testng"],
            "other": ["rest-api", "graphql", "microservices", "oauth", "jwt", "websocket", "grpc"]
        }
    
    def extract_skills(self, text: str, is_jd: bool = False) -> Dict:
        """Extract structured skills from text with model fallback."""
        extractor_info = {"extractor": "unknown", "model": "none", "reason": "not_attempted"}
        
        # Try LLM extraction first
        try:
            skills_data, extractor_info = self._llm_extraction(text, is_jd)
            logger.info(f"Skills extraction: {extractor_info}")
            return skills_data
        except Exception as e:
            logger.warning(f"LLM extraction failed: {e}, falling back to regex")
            extractor_info = {"extractor": "regex", "model": "none", "reason": str(e)[:50]}
        
        # Fallback to regex extraction
        skills_data = self._regex_extraction(text, is_jd)
        logger.info(f"Skills extraction: {extractor_info}")
        return skills_data
    
    def _llm_extraction(self, text: str, is_jd: bool) -> tuple:
        """Try LLM extraction with model fallback."""
        import google.generativeai as genai
        from app.config import settings
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Try gemini-pro first (for google-generativeai==0.4.1)
        models_to_try = ["gemini-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"]
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                prompt = self._build_extraction_prompt(text, is_jd)
                response = model.generate_content(prompt)
                
                # Parse JSON response
                skills_data = self._parse_llm_response(response.text)
                skills_data = self._normalize_and_validate(skills_data, text, is_jd)
                
                return skills_data, {"extractor": "llm", "model": model_name, "reason": "ok"}
            except Exception as e:
                if "404" in str(e) or "not found" in str(e).lower():
                    logger.debug(f"Model {model_name} not available, trying next")
                    continue
                else:
                    raise
        
        raise Exception("All LLM models failed")
    
    def _parse_llm_response(self, response_text: str) -> Dict:
        """Parse LLM response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        text = response_text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text)
    
    def _regex_extraction(self, text: str, is_jd: bool) -> Dict:
        """Fallback regex-based extraction with atomic matching."""
        skills = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "cloud": [],
            "devops": [],
            "tools": [],
            "testing": [],
            "other": []
        }
        
        text_lower = text.lower()
        
        for category, skill_list in self.skill_whitelist.items():
            for skill in skill_list:
                if self._is_skill_present(skill, text_lower):
                    normalized = self.synonym_map.get(skill, skill)
                    if normalized not in skills[category]:
                        skills[category].append(normalized)
        
        if is_jd:
            # Heuristic: first 2 languages + first 2 frameworks = required
            skills["required"] = (skills["languages"][:2] + skills["frameworks"][:2])
            skills["preferred"] = (skills["cloud"] + skills["devops"])[:4]
        
        return skills
    
    def _is_skill_present(self, skill: str, text: str) -> bool:
        """Check if skill is present with word boundary matching."""
        # Special case for "go" - must be whole word and not part of other words
        if skill == "go":
            # Match "go" or "golang" as whole words
            pattern = r'\b(go|golang)\b'
            if re.search(pattern, text):
                # Exclude false positives
                false_positives = ["good", "google", "governance", "going", "gone", "got"]
                for fp in false_positives:
                    if fp in text:
                        # Check if "go" appears independently
                        go_matches = re.findall(r'\bgo\b', text)
                        if go_matches:
                            return True
                return bool(re.search(r'\bgolang\b', text))
            return False
        
        # For other skills, use word boundary matching
        pattern = r'\b' + re.escape(skill.replace('-', r'[-\s]?')) + r'\b'
        return bool(re.search(pattern, text))
    
    def _normalize_and_validate(self, skills_data: Dict, original_text: str, is_jd: bool) -> Dict:
        """Normalize synonyms and validate skills exist in text."""
        text_lower = original_text.lower()
        validated = {}
        
        for category in skills_data:
            if isinstance(skills_data[category], list):
                validated_list = []
                for skill in skills_data[category]:
                    skill_lower = skill.lower().strip()
                    normalized = self.synonym_map.get(skill_lower, skill_lower)
                    
                    # Validate skill exists in text
                    if self._is_skill_present(normalized, text_lower):
                        if normalized not in validated_list:
                            validated_list.append(normalized)
                
                validated[category] = validated_list
            elif isinstance(skills_data[category], dict):
                # Handle required/preferred
                validated[category] = {}
                for sub_key in skills_data[category]:
                    validated_list = []
                    for skill in skills_data[category][sub_key]:
                        skill_lower = skill.lower().strip()
                        normalized = self.synonym_map.get(skill_lower, skill_lower)
                        
                        if self._is_skill_present(normalized, text_lower):
                            if normalized not in validated_list:
                                validated_list.append(normalized)
                    
                    validated[category][sub_key] = validated_list
        
        return validated
    
    def _build_extraction_prompt(self, text: str, is_jd: bool) -> str:
        """Build extraction prompt for Gemini."""
        role = "job description" if is_jd else "resume"
        
        base_format = '''{\n  "languages": ["java", "python", "javascript"],\n  "frameworks": ["spring-boot", "react", "angular"],\n  "databases": ["postgresql", "mysql", "mongodb"],\n  "cloud": ["aws", "azure", "gcp"],\n  "devops": ["docker", "kubernetes", "jenkins"],\n  "tools": ["git", "maven", "gradle"],\n  "testing": ["junit", "mockito", "selenium"],\n  "other": ["rest-api", "microservices"]'''
        
        if is_jd:
            jd_addition = ',\n  "required": ["java", "spring-boot"],\n  "preferred": ["aws", "docker"]'
            format_example = base_format + jd_addition + '\n}'
        else:
            format_example = base_format + '\n}'
        
        return f"""Extract technical skills from this {role} and return as JSON. Be specific and atomic.

Text: {text[:2000]}

Return JSON format:
{format_example}

Extract only specific technologies present in the text. Return valid JSON only."""
    
    def calculate_skills_overlap(self, jd_skills: Dict, resume_skills: Dict) -> Dict:
        """Calculate intersection-only skills overlap with weighted Jaccard."""
        # Flatten resume skills (INTERSECTION ONLY)
        resume_all = set()
        for category in ["languages", "frameworks", "databases", "cloud", "devops", "tools", "testing", "other"]:
            resume_all.update(resume_skills.get(category, []))
        
        # Get JD requirements
        required_skills = set(jd_skills.get("required", []))
        preferred_skills = set(jd_skills.get("preferred", []))
        
        # Calculate INTERSECTION only
        matched_required = list(resume_all.intersection(required_skills))
        matched_preferred = list(resume_all.intersection(preferred_skills))
        
        # All matched skills (intersection)
        matched_skills = matched_required + matched_preferred
        
        # Missing skills
        missing_required = list(required_skills - resume_all)
        missing_preferred = list(preferred_skills - resume_all)
        
        # Weighted Jaccard: required=2.0, preferred=1.0
        total_weight = len(required_skills) * 2.0 + len(preferred_skills) * 1.0
        matched_weight = len(matched_required) * 2.0 + len(matched_preferred) * 1.0
        
        skills_overlap = matched_weight / max(1, total_weight)
        
        return {
            "skills_overlap": skills_overlap,
            "matched_required": matched_required,
            "matched_preferred": matched_preferred,
            "matched_skills": matched_skills,  # INTERSECTION ONLY
            "missing_required": missing_required,
            "missing_preferred": missing_preferred,
            "total_required": len(required_skills),
            "total_preferred": len(preferred_skills)
        }