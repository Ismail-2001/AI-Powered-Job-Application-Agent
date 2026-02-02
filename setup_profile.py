"""
Profile Setup Wizard
Interactive script to help users create their master profile.
"""

import json
import os
import sys
from typing import Dict, Any, List

def print_header():
    """Print welcome header."""
    print("\n" + "=" * 60)
    print("🎯 AI Job Application Agent - Profile Setup Wizard")
    print("=" * 60)
    print("\nThis wizard will help you create your professional profile.")
    print("Your profile will be used to generate customized CVs and cover letters.\n")

def get_input(prompt: str, default: str = "", required: bool = True) -> str:
    """Get user input with optional default value."""
    if default:
        full_prompt = f"{prompt} (default: {default}): "
    else:
        full_prompt = f"{prompt}: "
    
    value = input(full_prompt).strip()
    
    if not value:
        if default:
            return default
        elif required:
            print("⚠️  This field is required. Please enter a value.")
            return get_input(prompt, default, required)
        else:
            return ""
    
    return value

def get_list_input(prompt: str, example: str = "") -> List[str]:
    """Get a list of items from user."""
    print(f"\n{prompt}")
    if example:
        print(f"Example: {example}")
    print("Enter items one per line. Press Enter twice when done:")
    
    items = []
    while True:
        item = input().strip()
        if not item:
            if items:
                break
            else:
                print("⚠️  Please enter at least one item.")
                continue
        items.append(item)
    
    return items

def collect_personal_info() -> Dict[str, str]:
    """Collect personal information."""
    print("\n" + "-" * 60)
    print("📋 Step 1: Personal Information")
    print("-" * 60)
    
    return {
        "name": get_input("Full Name"),
        "email": get_input("Email Address"),
        "phone": get_input("Phone Number", required=False),
        "linkedin": get_input("LinkedIn Profile URL", required=False),
        "location": get_input("Location (City, State/Country)")
    }

def collect_summary() -> str:
    """Collect professional summary."""
    print("\n" + "-" * 60)
    print("📝 Step 2: Professional Summary")
    print("-" * 60)
    print("\nWrite a 2-3 sentence summary highlighting:")
    print("  • Years of experience")
    print("  • Core expertise")
    print("  • Key achievements")
    print("\nExample: 'Senior Software Engineer with 8 years of experience...'")
    print("\nEnter your professional summary:")
    
    summary = input().strip()
    while not summary or len(summary) < 50:
        print("⚠️  Summary should be at least 50 characters. Please try again:")
        summary = input().strip()
    
    return summary

def collect_skills() -> Dict[str, List[str]]:
    """Collect skills information."""
    print("\n" + "-" * 60)
    print("🛠️  Step 3: Skills")
    print("-" * 60)
    
    skills = {}
    
    print("\nEnter your programming languages:")
    skills["Languages"] = get_list_input("Languages", "Python, JavaScript, Go, SQL")
    
    print("\nEnter your frameworks/libraries:")
    skills["Frameworks"] = get_list_input("Frameworks", "Django, React, FastAPI")
    
    print("\nEnter your tools/platforms:")
    skills["Tools"] = get_list_input("Tools", "AWS, Docker, Kubernetes, Git")
    
    print("\nEnter your soft skills (optional):")
    soft_skills = get_list_input("Soft Skills", "Leadership, Communication")
    if soft_skills:
        skills["Soft Skills"] = soft_skills
    
    return skills

def collect_experience() -> List[Dict[str, Any]]:
    """Collect work experience."""
    print("\n" + "-" * 60)
    print("💼 Step 4: Work Experience")
    print("-" * 60)
    print("\nEnter your work experience. For each role, provide:")
    print("  • Company name")
    print("  • Job title")
    print("  • Dates (e.g., '2020 - Present' or '2018 - 2020')")
    print("  • Location")
    print("  • Key achievements (use STAR method with metrics)")
    
    experience = []
    add_more = True
    
    while add_more:
        print(f"\n--- Experience Entry {len(experience) + 1} ---")
        exp = {
            "company": get_input("Company Name"),
            "title": get_input("Job Title"),
            "dates": get_input("Dates", "2020 - Present"),
            "location": get_input("Location", required=False),
            "responsibilities": []
        }
        
        print("\nEnter your key achievements/responsibilities:")
        print("Tip: Use STAR method and include metrics (e.g., 'Increased revenue by 30%')")
        print("Enter one achievement per line. Press Enter twice when done:")
        
        responsibilities = []
        while True:
            resp = input().strip()
            if not resp:
                if responsibilities:
                    break
                else:
                    print("⚠️  Please enter at least one achievement.")
                    continue
            responsibilities.append(resp)
        
        exp["responsibilities"] = responsibilities
        experience.append(exp)
        
        if len(experience) >= 5:
            print("\n⚠️  You've added 5 experiences. You can add more later in the JSON file.")
            add_more = False
        else:
            add_more = input("\nAdd another experience? (y/n): ").strip().lower() == 'y'
    
    return experience

def collect_education() -> List[Dict[str, Any]]:
    """Collect education information."""
    print("\n" + "-" * 60)
    print("🎓 Step 5: Education")
    print("-" * 60)
    
    education = []
    add_more = True
    
    while add_more:
        print(f"\n--- Education Entry {len(education) + 1} ---")
        edu = {
            "school": get_input("School/University Name"),
            "degree": get_input("Degree", "B.S. Computer Science"),
            "dates": get_input("Dates", "2014 - 2018"),
            "gpa": get_input("GPA (optional)", required=False),
            "honors": []
        }
        
        honors_input = get_input("Honors/Awards (comma-separated, optional)", required=False)
        if honors_input:
            edu["honors"] = [h.strip() for h in honors_input.split(",")]
        else:
            del edu["honors"]
        
        if not edu["gpa"]:
            del edu["gpa"]
        
        education.append(edu)
        add_more = input("\nAdd another education entry? (y/n): ").strip().lower() == 'y'
    
    return education

def collect_projects() -> List[Dict[str, Any]]:
    """Collect project information."""
    print("\n" + "-" * 60)
    print("🚀 Step 6: Projects (Optional)")
    print("-" * 60)
    
    add_projects = input("Do you want to add projects? (y/n): ").strip().lower() == 'y'
    
    if not add_projects:
        return []
    
    projects = []
    add_more = True
    
    while add_more:
        print(f"\n--- Project {len(projects) + 1} ---")
        project = {
            "name": get_input("Project Name"),
            "description": get_input("Description"),
            "technologies": [],
            "url": get_input("URL (GitHub, website, optional)", required=False)
        }
        
        techs_input = get_input("Technologies (comma-separated)", "Python, Django")
        project["technologies"] = [t.strip() for t in techs_input.split(",")]
        
        if not project["url"]:
            del project["url"]
        
        projects.append(project)
        add_more = input("\nAdd another project? (y/n): ").strip().lower() == 'y'
    
    return projects

def save_profile(profile: Dict[str, Any], path: str = "data/master_profile.json"):
    """Save profile to JSON file."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Profile saved to: {path}")

def main():
    """Main setup wizard."""
    print_header()
    
    # Check if profile already exists
    if os.path.exists("data/master_profile.json"):
        overwrite = input("\n⚠️  Profile already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    try:
        # Collect all information
        profile = {
            "personal_info": collect_personal_info(),
            "summary": collect_summary(),
            "skills": collect_skills(),
            "experience": collect_experience(),
            "education": collect_education(),
            "projects": collect_projects()
        }
        
        # Save profile
        save_profile(profile)
        
        print("\n" + "=" * 60)
        print("✨ Profile Setup Complete!")
        print("=" * 60)
        print(f"\n✅ Your profile has been created for: {profile['personal_info']['name']}")
        print("\n💡 Next steps:")
        print("   1. Review your profile at: data/master_profile.json")
        print("   2. Make any adjustments if needed")
        print("   3. Run the application: python app.py")
        print("\n🚀 You're ready to generate customized CVs and cover letters!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
