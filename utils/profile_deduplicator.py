"""
Profile Deduplicator
Removes duplicate entries and prevents repetition in CV generation
"""

from typing import Dict, Any, List

class ProfileDeduplicator:
    """
    Utility to remove duplicates and prevent repetition in profile data.
    """
    
    @staticmethod
    def deduplicate_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove duplicate entries from profile.
        
        Args:
            profile: Profile dictionary
            
        Returns:
            Deduplicated profile
        """
        deduplicated = profile.copy()
        
        # Deduplicate experience
        if 'experience' in deduplicated:
            deduplicated['experience'] = ProfileDeduplicator._deduplicate_experience(
                deduplicated['experience']
            )
        
        # Deduplicate education
        if 'education' in deduplicated:
            deduplicated['education'] = ProfileDeduplicator._deduplicate_education(
                deduplicated['education']
            )
        
        # Deduplicate skills
        if 'skills' in deduplicated:
            deduplicated['skills'] = ProfileDeduplicator._deduplicate_skills(
                deduplicated['skills']
            )
        
        # Deduplicate projects
        if 'projects' in deduplicated:
            deduplicated['projects'] = ProfileDeduplicator._deduplicate_projects(
                deduplicated['projects']
            )
        
        return deduplicated
    
    @staticmethod
    def _deduplicate_experience(experience_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate work experiences"""
        seen = set()
        unique_experiences = []
        
        for exp in experience_list:
            # Create a unique key from company + title + dates
            key = (
                exp.get('company', '').lower().strip(),
                exp.get('title', '').lower().strip(),
                exp.get('dates', '').strip()
            )
            
            if key not in seen and key[0] and key[1]:  # Must have company and title
                seen.add(key)
                unique_experiences.append(exp)
        
        return unique_experiences
    
    @staticmethod
    def _deduplicate_education(education_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate education entries"""
        seen = set()
        unique_education = []
        
        for edu in education_list:
            # Create a unique key from school + degree + dates
            key = (
                edu.get('school', '').lower().strip(),
                edu.get('degree', '').lower().strip(),
                edu.get('dates', '').strip()
            )
            
            if key not in seen and key[0] and key[1]:  # Must have school and degree
                seen.add(key)
                unique_education.append(edu)
        
        return unique_education
    
    @staticmethod
    def _deduplicate_skills(skills: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Remove duplicate skills within each category"""
        deduplicated = {}
        
        for category, skill_list in skills.items():
            if isinstance(skill_list, list):
                # Remove duplicates while preserving order
                seen = set()
                unique_skills = []
                for skill in skill_list:
                    skill_lower = skill.lower().strip()
                    if skill_lower and skill_lower not in seen:
                        seen.add(skill_lower)
                        unique_skills.append(skill)
                deduplicated[category] = unique_skills
            else:
                deduplicated[category] = skill_list
        
        return deduplicated
    
    @staticmethod
    def _deduplicate_projects(projects_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate projects"""
        seen = set()
        unique_projects = []
        
        for proj in projects_list:
            # Create a unique key from project name
            key = proj.get('name', '').lower().strip()
            
            if key and key not in seen:
                seen.add(key)
                unique_projects.append(proj)
        
        return unique_projects
    
    @staticmethod
    def remove_repetitive_content(cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove repetitive content between sections.
        For example, if summary repeats what's in experience, simplify summary.
        """
        cleaned = cv_data.copy()
        
        # Extract key phrases from experience section
        experience_keywords = set()
        if 'experience' in cleaned:
            for exp in cleaned['experience']:
                company = exp.get('company', '').lower()
                title = exp.get('title', '').lower()
                if company:
                    experience_keywords.add(company)
                if title:
                    experience_keywords.add(title)
        
        # Simplify summary if it's too repetitive
        if 'summary' in cleaned and experience_keywords:
            summary = cleaned['summary']
            # If summary mentions same companies/titles multiple times, it's repetitive
            summary_lower = summary.lower()
            mentions = sum(1 for keyword in experience_keywords if keyword in summary_lower)
            if mentions > 2:  # Too many mentions
                # Keep summary but mark for review (in production, could use AI to rewrite)
                pass  # For now, just keep as is but deduplicated
        
        return cleaned
