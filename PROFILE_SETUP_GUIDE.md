# Profile Setup Guide
## Getting Started with Your Professional Profile

This guide will help you set up your professional profile so the AI Job Application Agent can generate customized CVs and cover letters for you.

---

## 🚀 Quick Setup (Recommended)

### Option 1: Interactive Setup Wizard

The easiest way to set up your profile is using the interactive wizard:

```bash
python setup_profile.py
```

This wizard will guide you through:
1. Personal information (name, email, LinkedIn, etc.)
2. Professional summary
3. Skills (languages, frameworks, tools)
4. Work experience
5. Education
6. Projects (optional)

**The wizard will:**
- ✅ Ask you questions step-by-step
- ✅ Provide examples and tips
- ✅ Validate your input
- ✅ Save everything automatically

### Option 2: Manual Setup

1. **Copy the template**:
   ```bash
   # Windows
   copy data\master_profile.json.template data\master_profile.json
   
   # macOS/Linux
   cp data/master_profile.json.template data/master_profile.json
   ```

2. **Edit the file** with your information:
   - Open `data/master_profile.json` in a text editor
   - Replace all placeholder values with your actual information
   - Save the file

---

## 📋 Profile Structure

Your profile should include the following sections:

### 1. Personal Information

```json
{
  "personal_info": {
    "name": "Your Full Name",
    "email": "your.email@example.com",
    "phone": "+1 555-0123",
    "linkedin": "https://www.linkedin.com/in/yourprofile",
    "location": "Your City, State/Country"
  }
}
```

**Tips:**
- Use your full professional name
- Include a professional email address
- Add your LinkedIn profile URL (helps with networking)
- Location helps with location-specific job matching

### 2. Professional Summary

```json
{
  "summary": "2-3 sentences highlighting your experience, expertise, and key achievements..."
}
```

**Tips:**
- Keep it to 2-3 sentences
- Include years of experience
- Mention core expertise areas
- Highlight 1-2 key achievements
- Example: "Senior Software Engineer with 8 years of experience building scalable distributed systems. Expert in Python, cloud architecture, and team leadership. Proven track record of delivering high-impact projects that increased efficiency by 40%+."

### 3. Skills

```json
{
  "skills": {
    "Languages": ["Python", "JavaScript", "Go"],
    "Frameworks": ["Django", "React", "FastAPI"],
    "Tools": ["AWS", "Docker", "Kubernetes"],
    "Soft Skills": ["Leadership", "Communication"]
  }
}
```

**Tips:**
- List skills exactly as they appear in job descriptions
- Include all relevant technologies
- Add soft skills that are important for your field
- Keep lists comprehensive but focused

### 4. Work Experience

```json
{
  "experience": [
    {
      "company": "Company Name",
      "title": "Your Job Title",
      "dates": "2020 - Present",
      "location": "City, State",
      "responsibilities": [
        "Achievement with metrics using STAR method",
        "Another quantified achievement"
      ]
    }
  ]
}
```

**Tips for Responsibilities:**
- Use the **STAR method** (Situation, Task, Action, Result)
- **Quantify everything**: Use numbers, percentages, dollar amounts
- **Show impact**: What did you achieve? How did it help?
- **Use action verbs**: Led, Developed, Improved, Reduced, etc.

**Examples:**
- ❌ "Worked on improving system performance"
- ✅ "Improved system performance by 40% by implementing caching strategies, reducing server costs by $20K annually"

- ❌ "Led a team"
- ✅ "Led a team of 5 engineers to migrate legacy monolith to microservices, improving system uptime from 99.5% to 99.99%"

### 5. Education

```json
{
  "education": [
    {
      "school": "University Name",
      "degree": "B.S. Computer Science",
      "dates": "2014 - 2018",
      "gpa": "3.8/4.0",
      "honors": ["Dean's List", "Summa Cum Laude"]
    }
  ]
}
```

**Tips:**
- Include GPA only if it's strong (3.5+)
- Add honors/awards if relevant
- Include relevant coursework if recent graduate

### 6. Projects (Optional)

```json
{
  "projects": [
    {
      "name": "Project Name",
      "description": "Brief description, technologies, and impact",
      "technologies": ["Python", "Django"],
      "url": "https://github.com/yourusername/project"
    }
  ]
}
```

**Tips:**
- Include personal projects, open source contributions
- Add GitHub links if available
- Describe impact and technologies used

---

## ✨ Best Practices

### 1. Be Specific and Quantify

**Bad:**
- "Worked on AI projects"
- "Improved performance"
- "Led a team"

**Good:**
- "Built 15+ production AI agents using LangChain and Python, automating document processing for enterprise clients"
- "Improved application performance by 40% through caching strategies, reducing load times from 2s to 0.5s"
- "Led a team of 5 engineers to migrate legacy system, improving uptime from 99.5% to 99.99%"

### 2. Use Industry Keywords

- Include exact technology names (Python, not "programming")
- Use industry-standard terms
- Match terminology from job descriptions

### 3. Keep It Current

- Update your profile regularly
- Add new skills as you learn them
- Update achievements with latest metrics

### 4. STAR Method for Achievements

**S**ituation: Context/background  
**T**ask: What needed to be done  
**A**ction: What you did  
**R**esult: Measurable outcome

**Example:**
- Situation: "Legacy monolith system with 99.5% uptime"
- Task: "Migrate to microservices architecture"
- Action: "Led team of 5 engineers, designed architecture, implemented services"
- Result: "Improved uptime to 99.99%, reduced deployment time by 60%"

---

## 🔍 Profile Validation

After setting up your profile, verify it:

```bash
python test_system.py
```

This will check:
- ✅ Profile file exists
- ✅ Valid JSON format
- ✅ Required fields present
- ✅ No placeholder values

---

## 🎯 Profile Optimization Tips

### For Better Match Scores

1. **Include Comprehensive Skills**: List all technologies you've used
2. **Quantify Achievements**: Numbers make you stand out
3. **Use Industry Terms**: Match terminology from job postings
4. **Keep It Updated**: Add new experiences and skills regularly

### For ATS Optimization

1. **Exact Keywords**: Use exact terms from job descriptions
2. **Standard Headers**: The system uses ATS-friendly headers
3. **No Graphics**: Documents are text-only for maximum compatibility
4. **Full Terms**: "Natural Language Processing" not "NLP"

---

## 🛠️ Updating Your Profile

### Via Web Interface

1. Start the web server: `python app.py`
2. Navigate to profile settings (if implemented)
3. Edit and save

### Via File Editor

1. Open `data/master_profile.json`
2. Edit any section
3. Save the file
4. Changes take effect immediately

### Via Setup Wizard

Run the wizard again:
```bash
python setup_profile.py
```

It will ask if you want to overwrite existing profile.

---

## ❓ Common Questions

### Q: Do I need to fill in every field?

**A:** No, but more information = better customization. At minimum:
- Personal info (name, email)
- Summary
- Skills
- At least one work experience

### Q: Can I have multiple profiles?

**A:** Currently, the system uses one profile. You can:
- Create multiple profile files and swap them
- Use different profile files for different career paths
- Future versions will support multiple profiles

### Q: How often should I update my profile?

**A:** Update whenever you:
- Start a new job
- Complete a major project
- Learn new skills
- Achieve significant results

### Q: What if I don't have much experience?

**A:** Focus on:
- Education and coursework
- Personal projects
- Internships or volunteer work
- Relevant skills and certifications
- Quantify what you can (e.g., "Built 3 web applications")

---

## 🚨 Troubleshooting

### Profile Not Found

```
❌ Error: Profile file not found at data/master_profile.json
```

**Solution:**
1. Run `python setup_profile.py`
2. Or copy template: `cp data/master_profile.json.template data/master_profile.json`

### Invalid JSON

```
❌ Error: Invalid JSON in data/master_profile.json
```

**Solution:**
1. Check for missing commas, brackets, or quotes
2. Use a JSON validator: https://jsonlint.com/
3. Or run the setup wizard again

### Placeholder Values Detected

```
⚠️ Profile exists but contains placeholder values
```

**Solution:**
1. Open `data/master_profile.json`
2. Replace all "Your Full Name", "your.email@example.com", etc. with your actual information
3. Save the file

---

## 📚 Additional Resources

- **STAR Method Guide**: [How to Use the STAR Method](https://www.themuse.com/advice/star-interview-method)
- **Resume Writing Tips**: [ATS-Friendly Resume Guide](https://www.jobscan.co/blog/ats-resume-optimization)
- **LinkedIn Optimization**: [LinkedIn Profile Best Practices](https://www.linkedin.com/help/linkedin/answer/a1339360)

---

## ✅ Checklist

Before using the application, ensure:

- [ ] Profile file exists at `data/master_profile.json`
- [ ] All personal information is filled in (not placeholders)
- [ ] Professional summary is written
- [ ] Skills are listed
- [ ] At least one work experience is added
- [ ] Education information is included
- [ ] Profile validated with `python test_system.py`

---

**Ready to generate your customized CVs and cover letters!** 🚀

Run `python app.py` to start the web interface, or `python main.py` for the CLI.
