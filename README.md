# AI-Powered Job Application Agent

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)](https://github.com/Ismail-2001/AI-Job-Application-Agent)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

> An intelligent, multi-agent AI system that automatically analyzes job descriptions and generates ATS-optimized, customized CVs and cover letters tailored to each application. Built for job seekers who want to maximize their application success rate with minimal effort.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation & Setup](#-installation--setup)
- [Profile Setup](#-profile-setup)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Screenshots / Demo](#-screenshots--demo)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

**AI-Powered Job Application Agent** is a production-ready, multi-agent system designed to automate and optimize the job application process. The system leverages advanced AI agents to analyze job descriptions, extract key requirements, and automatically generate customized CVs and cover letters that are optimized for Applicant Tracking Systems (ATS).

**Who it's for:**
- Job seekers looking to streamline their application process
- Professionals applying to multiple positions
- Career changers needing tailored application materials
- Developers interested in multi-agent AI systems
- Recruiters and HR professionals exploring automation tools

**What it does:**
The system takes a job description as input and produces two professional documents: a customized CV and a personalized cover letter, both optimized for ATS compatibility and keyword matching. The entire process takes 20-30 seconds and requires minimal user input.

---

## ✨ Key Features

### Core Capabilities

- **🤖 Multi-Agent AI Architecture**: Three specialized AI agents work together to analyze, customize, and generate documents
- **🔍 Intelligent Job Analysis**: Extracts requirements, skills, keywords, and qualifications from job descriptions with high accuracy
- **🎨 Smart CV Customization**: Automatically tailors your master profile to match specific job requirements using ATS optimization techniques
- **✍️ Cover Letter Generation**: Creates personalized, compelling cover letters that connect your value to the employer's needs
- **📊 Match Score Analysis**: Calculates compatibility scores between your profile and job requirements with detailed breakdowns
- **🎯 ATS Optimization**: 95%+ compatibility with Applicant Tracking Systems through exact keyword matching and standard formatting

### User Experience

- **🌐 Web Interface**: Beautiful, responsive web UI built with modern design principles
- **💻 Command Line Interface**: Full-featured CLI for power users and automation
- **⚡ Fast Processing**: Complete analysis and document generation in 20-30 seconds
- **📄 Professional Output**: Generates industry-standard DOCX files ready for submission
- **🔄 Retry Logic**: Robust error handling with automatic retries for API calls
- **👤 User-Friendly Setup**: Interactive profile setup wizard for easy onboarding

---

## 🛠️ Tech Stack

### Frontend

- **HTML5/CSS3**: Semantic markup with modern CSS (Custom Properties, Grid, Flexbox)
- **Vanilla JavaScript**: No framework dependencies for optimal performance
- **Responsive Design**: Mobile-first approach with breakpoints at 640px, 768px, 1024px
- **Accessibility**: WCAG AA compliant with ARIA labels and keyboard navigation

### Backend

- **Python 3.10+**: Modern Python with type hints and async capabilities
- **Flask 3.0+**: Lightweight web framework for the API and web interface
- **python-docx**: Professional document generation for Word-compatible files
- **python-dotenv**: Environment variable management

### AI / APIs / Tools

- **DeepSeek API**: Primary LLM provider (OpenAI-compatible interface)
  - Model: `deepseek-chat`
  - Alternative: Google Gemini API support included
- **Multi-Agent System**: Three specialized agents:
  - `JobAnalyzer`: Structured data extraction (temperature: 0.1)
  - `CVCustomizer`: Content tailoring (temperature: 0.5)
  - `CoverLetterGenerator`: Creative writing (temperature: 0.7)
- **Retry Logic**: `tenacity` library for robust API error handling
- **JSON Parsing**: Custom parsing with markdown fence removal and fallbacks

### Hosting / Deployment

- **Local Development**: Flask development server (`python app.py`)
- **Production Options**:
  - **Docker**: Containerization support (Dockerfile ready)
  - **Cloud Platforms**: Compatible with AWS, GCP, Azure, Heroku
  - **PaaS**: Ready for deployment on Railway, Render, Fly.io
  - **Traditional**: Works on any Python-compatible hosting

---

## 🏗️ Architecture

### System Flow

```
┌─────────────────┐
│  Job Description│
│   (User Input)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JobAnalyzer    │ → Extracts: requirements, skills, keywords, role info
│  Agent          │   Output: Structured JSON analysis
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MatchCalculator │ → Calculates: compatibility score, missing skills
│  Utility        │   Output: Match metrics and recommendations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CVCustomizer   │ → Tailors: profile to job requirements
│  Agent          │   Output: Customized CV content (JSON)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│CoverLetterGen   │ → Generates: personalized cover letter
│  Agent          │   Output: Cover letter text
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│DocumentBuilder  │ → Creates: Professional DOCX files
│  Utility        │   Output: CV.docx + CoverLetter.docx
└─────────────────┘
```

### Agent Responsibilities

**1. JobAnalyzer Agent** (`agents/job_analyzer.py`)
- **Role**: Recruitment analyst with 20 years of experience
- **Task**: Deconstruct job descriptions into structured data
- **Output**: JSON with role info, requirements, skills, keywords
- **Temperature**: 0.1 (low for precision and consistency)
- **Key Features**:
  - Extracts exact keywords (preserves capitalization for ATS)
  - Distinguishes must-have vs nice-to-have skills
  - Identifies company name, location, role level
  - Prevents hallucination with validation layer

**2. CVCustomizer Agent** (`agents/cv_customizer.py`)
- **Role**: Career coach and professional resume writer
- **Task**: Rewrite candidate profile to align with job requirements
- **Output**: Customized CV content matching job keywords
- **Temperature**: 0.5 (balanced creativity and adherence)
- **Key Features**:
  - Uses STAR method for achievement quantification
  - Reorders skills to prioritize job requirements
  - Selects most relevant work experience
  - Natural keyword integration (not keyword stuffing)

**3. CoverLetterGenerator Agent** (`agents/cover_letter_generator.py`)
- **Role**: Expert career coach and copywriter
- **Task**: Write compelling, personalized cover letters
- **Output**: Professional cover letter text (250-350 words)
- **Temperature**: 0.7 (creative but professional)
- **Key Features**:
  - Connects candidate value to company needs
  - References specific achievements from profile
  - Professional yet personable tone
  - Avoids generic clichés

### Data Flow

1. **Input**: Raw job description text (user-provided)
2. **Analysis**: Structured JSON extraction (JobAnalyzer)
3. **Matching**: Compatibility calculation (MatchCalculator)
4. **Customization**: Profile tailoring (CVCustomizer)
5. **Generation**: Cover letter creation (CoverLetterGenerator)
6. **Output**: Professional DOCX documents (DocumentBuilder)

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager, included with Python)
- **DeepSeek API Key** ([Get one here](https://platform.deepseek.com/))
- **Git** (for cloning the repository)

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/Ismail-2001/AI-Job-Application-Agent.git
cd AI-Job-Application-Agent
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai>=1.0.0` - For DeepSeek API (OpenAI-compatible)
- `python-docx>=0.8.11` - Document generation
- `tenacity>=8.0.0` - Retry logic
- `python-dotenv>=1.0.0` - Environment variables
- `flask>=3.0.0` - Web framework

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

Add your API key to `.env`:

```env
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional: Flask secret key for sessions
FLASK_SECRET_KEY=your_secret_key_here

# Optional: Google Gemini API (if using Gemini instead)
# GOOGLE_API_KEY=your_google_api_key_here
```

**⚠️ Important**: Never commit your `.env` file. It's already in `.gitignore`.

#### 5. Set Up Your Profile

**Option A: Interactive Setup Wizard (Recommended)**

```bash
python setup_profile.py
```

This wizard will guide you through creating your profile step-by-step.

**Option B: Manual Setup**

1. Copy the template:
   ```bash
   # Windows
   copy data\master_profile.json.template data\master_profile.json
   
   # macOS/Linux
   cp data/master_profile.json.template data/master_profile.json
   ```

2. Edit `data/master_profile.json` with your information

See [PROFILE_SETUP_GUIDE.md](PROFILE_SETUP_GUIDE.md) for detailed instructions.

#### 6. Verify Installation

Run the system verification script:

```bash
python test_system.py
```

You should see:
```
✅ PASS - Dependencies
✅ PASS - Project Structure
✅ PASS - Master Profile
✅ PASS - Environment Config
```

---

## 👤 Profile Setup

### Quick Start

The easiest way to set up your profile is using the interactive wizard:

```bash
python setup_profile.py
```

### What You'll Need

- Personal information (name, email, LinkedIn, location)
- Professional summary (2-3 sentences)
- Skills (languages, frameworks, tools)
- Work experience (with quantified achievements)
- Education details
- Projects (optional)

### Profile Best Practices

1. **Quantify Achievements**: Use numbers, percentages, dollar amounts
2. **Use STAR Method**: Situation, Task, Action, Result
3. **Include Keywords**: Industry-standard terms and technologies
4. **Keep It Current**: Update regularly with new experiences

**Example Achievement:**
- ❌ "Worked on improving system performance"
- ✅ "Improved system performance by 40% through caching strategies, reducing load times from 2s to 0.5s and saving $20K annually"

See [PROFILE_SETUP_GUIDE.md](PROFILE_SETUP_GUIDE.md) for comprehensive guidance.

---

## 🚀 Usage

### Web Interface (Recommended)

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://localhost:5000`

3. **Use the interface**:
   - Paste a job description in the text area
   - Click "Analyze & Generate CV"
   - Wait 20-30 seconds for processing
   - Download your customized CV and cover letter

4. **Stop the server**:
   Press `Ctrl+C` in the terminal

### Command Line Interface

1. **Run the CLI**:
   ```bash
   python main.py
   ```

2. **Follow the prompts**:
   ```
   📋 Paste the Job Description below (Press Ctrl+Z/D then Enter when done):
   [Paste your job description]
   ^Z
   ```

3. **Wait for processing**:
   The system will:
   - Analyze the job description
   - Calculate match score
   - Customize your CV
   - Generate cover letter
   - Create DOCX files

4. **Find your documents**:
   Check the `output/` directory for your files:
   - `CV_CompanyName_JobTitle.docx`
   - `CL_CompanyName_JobTitle.docx`

### Example Workflow

```bash
# 1. Set up your profile (first time only)
python setup_profile.py

# 2. Start web server
python app.py

# 3. In browser: http://localhost:5000
# 4. Paste job description
# 5. Click "Analyze & Generate CV"
# 6. Download documents
# 7. Review and customize if needed
```

### API Usage (Advanced)

The system can also be used programmatically:

```python
from utils.deepseek_client import DeepSeekClient
from agents.job_analyzer import JobAnalyzer
import json

# Initialize
client = DeepSeekClient(api_key="your_key")
analyzer = JobAnalyzer(client)

# Analyze job
job_description = "Senior Python Developer..."
analysis = analyzer.analyze(job_description)

print(json.dumps(analysis, indent=2))
```

---

## 🚢 Deployment

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t ai-job-agent .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 \
     -e DEEPSEEK_API_KEY=your_key \
     ai-job-agent
   ```

### Cloud Platform Deployment

#### Heroku

1. **Create `Procfile`**:
   ```
   web: gunicorn app:app
   ```

2. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set DEEPSEEK_API_KEY=your_key
   git push heroku main
   ```

#### Railway

1. **Connect repository** to Railway
2. **Set environment variables** in Railway dashboard
3. **Deploy automatically** on push

#### Render

1. **Create new Web Service**
2. **Connect GitHub repository**
3. **Set environment variables**
4. **Deploy**

### Traditional Server Deployment

1. **Install dependencies** on server
2. **Use Gunicorn** for production:
   ```bash
   pip install gunicorn
   gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
   ```

3. **Use Nginx** as reverse proxy (recommended)
4. **Set up SSL** with Let's Encrypt

### Environment Variables for Production

```env
DEEPSEEK_API_KEY=your_production_key
FLASK_SECRET_KEY=your_secret_key
FLASK_ENV=production
```

---

## 📸 Screenshots / Demo

### Web Interface

![Web Interface](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=AI+Job+Application+Agent+Web+Interface)

*Screenshot of the modern, responsive web interface showing the job description input and results display.*

### Match Score Display

![Match Score](https://via.placeholder.com/600x300/059669/FFFFFF?text=Match+Score+Analysis)

*Visual representation of the compatibility score between your profile and job requirements.*

### Generated Documents

![Generated CV](https://via.placeholder.com/600x400/DC2626/FFFFFF?text=Generated+CV+Preview)

*Example of a professionally formatted CV generated by the system.*

**Live Demo**: [Coming Soon](#)

---

## 🗺️ Roadmap

### Short-term (1-2 months)

- [ ] **User Authentication**: JWT-based auth system for multi-user support
- [ ] **Database Integration**: PostgreSQL for job history and user profiles
- [ ] **Job History Tracking**: Save and manage past applications
- [ ] **Batch Processing**: Process multiple job descriptions simultaneously
- [ ] **Progress Indicators**: Real-time progress updates for async processing
- [ ] **Profile Editor UI**: Web-based profile editing interface

### Mid-term (3-6 months)

- [ ] **LinkedIn Integration**: Import profile data from LinkedIn
- [ ] **Interview Preparation**: Generate Q&A based on job requirements
- [ ] **A/B Testing Framework**: Test multiple CV versions and track performance
- [ ] **Profile Optimization Suggestions**: AI-powered recommendations for profile improvements
- [ ] **Multi-Profile Support**: Create and manage multiple professional profiles

### Long-term (6-12 months)

- [ ] **Autonomous Job Research**: Agent that scrapes job boards automatically
- [ ] **Application Tracking**: Full CRM for managing applications and follow-ups
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **API Access**: Public API for integrations with other tools
- [ ] **Enterprise Features**: Team accounts, white-label options

### Under Consideration

- [ ] **PDF Export**: Additional output format option
- [ ] **Multi-language Support**: Generate CVs in different languages
- [ ] **Template Library**: Multiple CV/cover letter templates
- [ ] **Analytics Dashboard**: Track application success rates
- [ ] **Chrome Extension**: Browser extension for one-click CV generation

---

## 🤝 Contributing

We welcome contributions! This project is open source and community-driven.

### How to Contribute

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/your-username/AI-Job-Application-Agent.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style (PEP 8)
   - Add type hints
   - Include docstrings
   - Write tests if applicable

4. **Test your changes**
   ```bash
   python test_system.py
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots if UI changes

### Contribution Guidelines

- **Code Quality**: Maintain production-ready standards
- **Documentation**: Update README/docs for new features
- **Testing**: Test your changes before submitting
- **Communication**: Be respectful and constructive
- **License**: Contributions are under MIT License

### Areas for Contribution

- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **New Features**: Implement roadmap items
- 📚 **Documentation**: Improve guides and examples
- 🎨 **Design**: Enhance UI/UX
- ⚡ **Performance**: Optimize speed and efficiency
- 🌐 **Internationalization**: Add language support

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Ismail Sajid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **DeepSeek AI** - For providing the LLM API powering the agents
- **python-docx** - For professional document generation
- **Flask** - For the lightweight web framework
- **Open Source Community** - For inspiration and best practices

## 📞 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Ismail-2001/AI-Job-Application-Agent/issues)
- **Email**: ismailsajid0617@gmail.com
- **LinkedIn**: [Ismail Sajid](https://www.linkedin.com/in/ismailsajid0617/)

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star on GitHub!

---

**Built with ❤️ by [Ismail Sajid](https://www.linkedin.com/in/ismailsajid0617/)**

*Empowering job seekers with AI-powered application automation.*
