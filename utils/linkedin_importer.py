"""
LinkedIn Profile Importer
Extracts profile data from LinkedIn export or API
"""

import json
import re
from typing import Dict, Any, List, Optional
from pathlib import Path

class LinkedInImporter:
    """
    Import LinkedIn profile data and convert to our profile format.
    Supports:
    - LinkedIn Data Export (JSON format)
    - Manual LinkedIn URL parsing (future: API integration)
    """
    
    def __init__(self):
        self.supported_formats = ['linkedin_export', 'manual']
    
    def import_from_export(self, export_path: str) -> Dict[str, Any]:
        """
        Import from LinkedIn Data Export (Settings > Data Privacy > Get a copy of your data)
        
        Args:
            export_path: Path to LinkedIn export directory or Profile.json file
            
        Returns:
            Profile dictionary in our format
        """
        try:
            # Try to find Profile.json in export directory
            if Path(export_path).is_dir():
                profile_file = Path(export_path) / "Profile.json"
            else:
                profile_file = Path(export_path)
            
            if not profile_file.exists():
                raise FileNotFoundError(f"LinkedIn export file not found: {profile_file}")
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                linkedin_data = json.load(f)
            
            return self._convert_linkedin_to_profile(linkedin_data)
            
        except Exception as e:
            raise ValueError(f"Failed to import LinkedIn data: {e}")
    
    def import_from_url(self, linkedin_url: str, profile_name: str = None) -> Dict[str, Any]:
        """
        Import from LinkedIn profile URL (manual entry).
        Note: Full automation requires LinkedIn API access.
        This provides a template structure for manual completion.
        
        Args:
            linkedin_url: LinkedIn profile URL
            profile_name: Optional name extracted from URL or provided by user
            
        Returns:
            Profile dictionary template with helpful structure
        """
        # Extract profile ID from URL
        profile_id = self._extract_profile_id(linkedin_url)
        
        if not profile_id:
            raise ValueError("Invalid LinkedIn URL format. Please use format: https://www.linkedin.com/in/yourprofile/")
        
        # Try to extract name from URL (basic heuristic)
        if not profile_name:
            # Convert profile ID to readable name (basic)
            profile_name = profile_id.replace('-', ' ').title()
        
        # Return template structure with helpful placeholders
        return {
            "personal_info": {
                "name": profile_name or "",
                "email": "",
                "phone": "",
                "linkedin": linkedin_url,
                "location": ""
            },
            "summary": "Professional summary from LinkedIn. Edit this section to highlight your key achievements, years of experience, and core expertise.",
            "skills": {
                "Languages": [],
                "Frameworks": [],
                "Tools": [],
                "Soft Skills": []
            },
            "experience": [
                {
                    "company": "Company Name",
                    "title": "Your Job Title",
                    "dates": "2020 - Present",
                    "location": "City, State",
                    "responsibilities": [
                        "Add your key achievements here using STAR method",
                        "Quantify your impact (e.g., 'Increased revenue by 30%')",
                        "Highlight relevant skills and technologies"
                    ]
                }
            ],
            "education": [
                {
                    "school": "University Name",
                    "degree": "Your Degree",
                    "dates": "2014 - 2018"
                }
            ],
            "projects": [],
            "certifications": [],
            "languages": []
        }
    
    def _extract_profile_id(self, url: str) -> Optional[str]:
        """Extract LinkedIn profile ID from URL"""
        patterns = [
            r'linkedin\.com/in/([^/?]+)',
            r'linkedin\.com/pub/([^/?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def _convert_linkedin_to_profile(self, linkedin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert LinkedIn export format to our profile format.
        LinkedIn export structure varies, so we handle common fields.
        """
        profile = {
            "personal_info": {},
            "summary": "",
            "skills": {
                "Languages": [],
                "Frameworks": [],
                "Tools": [],
                "Soft Skills": []
            },
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "languages": []
        }
        
        # Extract personal info
        if 'Profile' in linkedin_data:
            profile_data = linkedin_data['Profile']
            
            # Name
            if 'firstName' in profile_data and 'lastName' in profile_data:
                profile["personal_info"]["name"] = f"{profile_data.get('firstName', '')} {profile_data.get('lastName', '')}".strip()
            
            # Email
            if 'emailAddress' in profile_data:
                profile["personal_info"]["email"] = profile_data['emailAddress']
            
            # Phone
            if 'phoneNumbers' in profile_data and len(profile_data['phoneNumbers']) > 0:
                profile["personal_info"]["phone"] = profile_data['phoneNumbers'][0].get('number', '')
            
            # Location
            if 'location' in profile_data:
                location = profile_data['location']
                if isinstance(location, dict):
                    profile["personal_info"]["location"] = location.get('name', '')
                else:
                    profile["personal_info"]["location"] = str(location)
            
            # LinkedIn URL
            if 'publicProfileUrl' in profile_data:
                profile["personal_info"]["linkedin"] = profile_data['publicProfileUrl']
            
            # Summary
            if 'summary' in profile_data:
                profile["summary"] = profile_data['summary']
            
            # Experience
            if 'positions' in profile_data:
                for pos in profile_data['positions'].get('values', []):
                    exp = {
                        "company": pos.get('companyName', ''),
                        "title": pos.get('title', ''),
                        "dates": self._format_dates(pos.get('startDate'), pos.get('endDate')),
                        "location": pos.get('location', {}).get('name', '') if isinstance(pos.get('location'), dict) else '',
                        "responsibilities": []
                    }
                    
                    # Description
                    if 'description' in pos:
                        desc = pos['description']
                        # Split into bullet points
                        responsibilities = [line.strip() for line in desc.split('\n') if line.strip()]
                        exp["responsibilities"] = responsibilities
                    
                    profile["experience"].append(exp)
            
            # Education
            if 'educations' in profile_data:
                for edu in profile_data['educations'].get('values', []):
                    education = {
                        "school": edu.get('schoolName', ''),
                        "degree": edu.get('degree', ''),
                        "dates": self._format_dates(edu.get('startDate'), edu.get('endDate')),
                    }
                    
                    if 'fieldOfStudy' in edu:
                        education["degree"] = f"{edu.get('degree', '')} in {edu['fieldOfStudy']}".strip()
                    
                    profile["education"].append(education)
            
            # Skills
            if 'skills' in profile_data:
                skills_list = []
                for skill in profile_data['skills'].get('values', []):
                    skill_name = skill.get('skill', {}).get('name', '') if isinstance(skill.get('skill'), dict) else skill.get('name', '')
                    if skill_name:
                        skills_list.append(skill_name)
                
                # Try to categorize skills (basic heuristic)
                profile["skills"]["Languages"] = [s for s in skills_list if self._is_language(s)]
                profile["skills"]["Frameworks"] = [s for s in skills_list if self._is_framework(s)]
                profile["skills"]["Tools"] = [s for s in skills_list if not self._is_language(s) and not self._is_framework(s)]
        
        return profile
    
    def _format_dates(self, start_date: Optional[Dict], end_date: Optional[Dict]) -> str:
        """Format LinkedIn date objects to readable string"""
        if not start_date:
            return ""
        
        start_str = ""
        if 'year' in start_date:
            start_str = str(start_date['year'])
        if 'month' in start_date:
            start_str = f"{start_date['month']:02d}/{start_str}"
        
        end_str = "Present"
        if end_date:
            if 'year' in end_date:
                end_str = str(end_date['year'])
            if 'month' in end_date:
                end_str = f"{end_date['month']:02d}/{end_str}"
        
        return f"{start_str} - {end_str}"
    
    def _is_language(self, skill: str) -> bool:
        """Heuristic to identify programming languages"""
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'sql', 'r', 'scala', 'typescript']
        return skill.lower() in languages
    
    def _is_framework(self, skill: str) -> bool:
        """Heuristic to identify frameworks"""
        frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'express', 'laravel', 'rails', 'tensorflow', 'pytorch']
        return skill.lower() in frameworks


def import_linkedin_profile(export_path: Optional[str] = None, linkedin_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to import LinkedIn profile.
    
    Args:
        export_path: Path to LinkedIn export file/directory
        linkedin_url: LinkedIn profile URL (for manual import)
        
    Returns:
        Profile dictionary
    """
    importer = LinkedInImporter()
    
    if export_path:
        return importer.import_from_export(export_path)
    elif linkedin_url:
        return importer.import_from_url(linkedin_url)
    else:
        raise ValueError("Either export_path or linkedin_url must be provided")
