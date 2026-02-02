/**
 * Comprehensive Profile Editor
 * Handles all profile sections: Personal Info, Experience, Education, Skills, Projects, Certifications
 */

// Profile data storage
let currentProfile = {
    personal_info: {},
    summary: '',
    skills: { Languages: [], Frameworks: [], Tools: [], 'Soft Skills': [] },
    experience: [],
    education: [],
    projects: [],
    certifications: [],
    languages: []
};

// Tab management
let activeTab = 'personal';

function switchTab(tabName) {
    activeTab = tabName;
    
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

function loadProfile() {
    return fetch('/api/profile')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.profile) {
                currentProfile = {
                    personal_info: data.profile.personal_info || {},
                    summary: data.profile.summary || '',
                    skills: data.profile.skills || { Languages: [], Frameworks: [], Tools: [], 'Soft Skills': [] },
                    experience: data.profile.experience || [],
                    education: data.profile.education || [],
                    projects: data.profile.projects || [],
                    certifications: data.profile.certifications || [],
                    languages: data.profile.languages || []
                };
                populateForms();
            }
        })
        .catch(error => {
            console.log('No existing profile to load');
        });
}

function populateForms() {
    // Personal Info
    if (currentProfile.personal_info) {
        document.getElementById('profile-name').value = currentProfile.personal_info.name || '';
        document.getElementById('profile-email').value = currentProfile.personal_info.email || '';
        document.getElementById('profile-phone').value = currentProfile.personal_info.phone || '';
        document.getElementById('profile-linkedin').value = currentProfile.personal_info.linkedin || '';
        document.getElementById('profile-location').value = currentProfile.personal_info.location || '';
    }
    document.getElementById('profile-summary').value = currentProfile.summary || '';
    
    // Skills
    renderSkills();
    
    // Experience
    renderExperience();
    
    // Education
    renderEducation();
    
    // Projects
    renderProjects();
    
    // Certifications
    renderCertifications();
    
    // Languages
    renderLanguages();
}

function renderSkills() {
    const container = document.getElementById('skills-container');
    if (!container) return;
    
    const categories = ['Languages', 'Frameworks', 'Tools', 'Soft Skills'];
    container.innerHTML = categories.map(category => {
        const skills = currentProfile.skills[category] || [];
        return `
            <div class="form-group">
                <label>${category}</label>
                <div class="skills-input-group">
                    <input type="text" 
                           class="skill-input" 
                           data-category="${category}"
                           placeholder="Add ${category.toLowerCase()} (comma-separated)"
                           value="${skills.join(', ')}">
                    <small>Enter skills separated by commas</small>
                </div>
            </div>
        `;
    }).join('');
}

function renderExperience() {
    const container = document.getElementById('experience-container');
    if (!container) return;
    
    if (currentProfile.experience.length === 0) {
        container.innerHTML = '<p style="color: var(--gray-500);">No work experience added yet. Click "Add Experience" to get started.</p>';
        return;
    }
    
    container.innerHTML = currentProfile.experience.map((exp, index) => `
        <div class="experience-item" data-index="${index}">
            <div class="item-header">
                <h4>${exp.title || 'Untitled'} at ${exp.company || 'Unknown'}</h4>
                <button type="button" class="btn-icon-only" onclick="removeExperience(${index})" aria-label="Remove experience">
                    <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>Company *</label>
                    <input type="text" class="exp-company" value="${exp.company || ''}" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Job Title *</label>
                    <input type="text" class="exp-title" value="${exp.title || ''}" data-index="${index}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>Dates *</label>
                    <input type="text" class="exp-dates" value="${exp.dates || ''}" placeholder="2020 - Present" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Location</label>
                    <input type="text" class="exp-location" value="${exp.location || ''}" data-index="${index}">
                </div>
            </div>
            <div class="form-group">
                <label>Responsibilities/Achievements *</label>
                <textarea class="exp-responsibilities" rows="3" data-index="${index}" placeholder="Enter one achievement per line. Use STAR method with metrics.">${(exp.responsibilities || []).join('\n')}</textarea>
                <small>One achievement per line. Include metrics (e.g., "Increased revenue by 30%")</small>
            </div>
        </div>
    `).join('');
}

function addExperience() {
    currentProfile.experience.push({
        company: '',
        title: '',
        dates: '',
        location: '',
        responsibilities: []
    });
    renderExperience();
    document.getElementById('experience-container').scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function removeExperience(index) {
    if (confirm('Are you sure you want to remove this experience?')) {
        currentProfile.experience.splice(index, 1);
        renderExperience();
    }
}

function renderEducation() {
    const container = document.getElementById('education-container');
    if (!container) return;
    
    if (currentProfile.education.length === 0) {
        container.innerHTML = '<p style="color: var(--gray-500);">No education entries added yet. Click "Add Education" to get started.</p>';
        return;
    }
    
    container.innerHTML = currentProfile.education.map((edu, index) => `
        <div class="education-item" data-index="${index}">
            <div class="item-header">
                <h4>${edu.degree || 'Untitled'} - ${edu.school || 'Unknown'}</h4>
                <button type="button" class="btn-icon-only" onclick="removeEducation(${index})" aria-label="Remove education">
                    <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>School/University *</label>
                    <input type="text" class="edu-school" value="${edu.school || ''}" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Degree *</label>
                    <input type="text" class="edu-degree" value="${edu.degree || ''}" data-index="${index}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>Dates *</label>
                    <input type="text" class="edu-dates" value="${edu.dates || ''}" placeholder="2014 - 2018" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>GPA</label>
                    <input type="text" class="edu-gpa" value="${edu.gpa || ''}" placeholder="3.8/4.0" data-index="${index}">
                </div>
            </div>
        </div>
    `).join('');
}

function addEducation() {
    currentProfile.education.push({
        school: '',
        degree: '',
        dates: '',
        gpa: ''
    });
    renderEducation();
    document.getElementById('education-container').scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function removeEducation(index) {
    if (confirm('Are you sure you want to remove this education entry?')) {
        currentProfile.education.splice(index, 1);
        renderEducation();
    }
}

function renderProjects() {
    const container = document.getElementById('projects-container');
    if (!container) return;
    
    if (currentProfile.projects.length === 0) {
        container.innerHTML = '<p style="color: var(--gray-500);">No projects added yet. Click "Add Project" to get started.</p>';
        return;
    }
    
    container.innerHTML = currentProfile.projects.map((proj, index) => `
        <div class="project-item" data-index="${index}">
            <div class="item-header">
                <h4>${proj.name || 'Untitled Project'}</h4>
                <button type="button" class="btn-icon-only" onclick="removeProject(${index})" aria-label="Remove project">
                    <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
            <div class="form-group">
                <label>Project Name *</label>
                <input type="text" class="proj-name" value="${proj.name || ''}" data-index="${index}">
            </div>
            <div class="form-group">
                <label>Description *</label>
                <textarea class="proj-description" rows="3" data-index="${index}">${proj.description || ''}</textarea>
            </div>
            <div class="form-group">
                <label>Technologies</label>
                <input type="text" class="proj-technologies" value="${(proj.technologies || []).join(', ')}" placeholder="Python, Django, PostgreSQL" data-index="${index}">
            </div>
            <div class="form-group">
                <label>URL</label>
                <input type="url" class="proj-url" value="${proj.url || ''}" placeholder="https://github.com/..." data-index="${index}">
            </div>
        </div>
    `).join('');
}

function addProject() {
    currentProfile.projects.push({
        name: '',
        description: '',
        technologies: [],
        url: ''
    });
    renderProjects();
    document.getElementById('projects-container').scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function removeProject(index) {
    if (confirm('Are you sure you want to remove this project?')) {
        currentProfile.projects.splice(index, 1);
        renderProjects();
    }
}

function renderCertifications() {
    const container = document.getElementById('certifications-container');
    if (!container) return;
    
    if (currentProfile.certifications.length === 0) {
        container.innerHTML = '<p style="color: var(--gray-500);">No certifications added yet. Click "Add Certification" to get started.</p>';
        return;
    }
    
    container.innerHTML = currentProfile.certifications.map((cert, index) => `
        <div class="cert-item" data-index="${index}">
            <div class="item-header">
                <h4>${cert.name || 'Untitled Certification'}</h4>
                <button type="button" class="btn-icon-only" onclick="removeCertification(${index})" aria-label="Remove certification">
                    <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>Certification Name *</label>
                    <input type="text" class="cert-name" value="${cert.name || ''}" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Issuer</label>
                    <input type="text" class="cert-issuer" value="${cert.issuer || ''}" data-index="${index}">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>Date</label>
                    <input type="text" class="cert-date" value="${cert.date || ''}" placeholder="2023" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Expiry</label>
                    <input type="text" class="cert-expiry" value="${cert.expiry || ''}" placeholder="2026" data-index="${index}">
                </div>
            </div>
        </div>
    `).join('');
}

function addCertification() {
    currentProfile.certifications.push({
        name: '',
        issuer: '',
        date: '',
        expiry: ''
    });
    renderCertifications();
    document.getElementById('certifications-container').scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function removeCertification(index) {
    if (confirm('Are you sure you want to remove this certification?')) {
        currentProfile.certifications.splice(index, 1);
        renderCertifications();
    }
}

function renderLanguages() {
    const container = document.getElementById('languages-container');
    if (!container) return;
    
    if (currentProfile.languages.length === 0) {
        container.innerHTML = '<p style="color: var(--gray-500);">No languages added yet. Click "Add Language" to get started.</p>';
        return;
    }
    
    container.innerHTML = currentProfile.languages.map((lang, index) => `
        <div class="language-item" data-index="${index}">
            <div class="item-header">
                <h4>${lang.language || 'Unknown'} - ${lang.proficiency || 'Unknown'}</h4>
                <button type="button" class="btn-icon-only" onclick="removeLanguage(${index})" aria-label="Remove language">
                    <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
            </div>
            <div class="form-row">
                <div class="form-group" style="flex: 1;">
                    <label>Language *</label>
                    <input type="text" class="lang-language" value="${lang.language || ''}" data-index="${index}">
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>Proficiency *</label>
                    <select class="lang-proficiency" data-index="${index}">
                        <option value="Native" ${lang.proficiency === 'Native' ? 'selected' : ''}>Native</option>
                        <option value="Fluent" ${lang.proficiency === 'Fluent' ? 'selected' : ''}>Fluent</option>
                        <option value="Professional" ${lang.proficiency === 'Professional' ? 'selected' : ''}>Professional</option>
                        <option value="Conversational" ${lang.proficiency === 'Conversational' ? 'selected' : ''}>Conversational</option>
                        <option value="Basic" ${lang.proficiency === 'Basic' ? 'selected' : ''}>Basic</option>
                    </select>
                </div>
            </div>
        </div>
    `).join('');
}

function addLanguage() {
    currentProfile.languages.push({
        language: '',
        proficiency: 'Professional'
    });
    renderLanguages();
    document.getElementById('languages-container').scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function removeLanguage(index) {
    if (confirm('Are you sure you want to remove this language?')) {
        currentProfile.languages.splice(index, 1);
        renderLanguages();
    }
}

function collectFormData() {
    // Personal Info
    const personalInfo = {
        name: document.getElementById('profile-name').value.trim(),
        email: document.getElementById('profile-email').value.trim(),
        phone: document.getElementById('profile-phone').value.trim() || '',
        linkedin: document.getElementById('profile-linkedin').value.trim() || '',
        location: document.getElementById('profile-location').value.trim() || ''
    };
    
    const summary = document.getElementById('profile-summary').value.trim();
    
    // Skills
    const skills = {};
    document.querySelectorAll('.skill-input').forEach(input => {
        const category = input.dataset.category;
        const value = input.value.trim();
        skills[category] = value ? value.split(',').map(s => s.trim()).filter(s => s) : [];
    });
    
    // Experience
    const experience = [];
    document.querySelectorAll('.experience-item').forEach((item, index) => {
        const company = item.querySelector('.exp-company').value.trim();
        const title = item.querySelector('.exp-title').value.trim();
        const dates = item.querySelector('.exp-dates').value.trim();
        const location = item.querySelector('.exp-location').value.trim();
        const responsibilitiesText = item.querySelector('.exp-responsibilities').value.trim();
        const responsibilities = responsibilitiesText ? responsibilitiesText.split('\n').filter(r => r.trim()) : [];
        
        if (company && title && dates) {
            experience.push({
                company,
                title,
                dates,
                location: location || undefined,
                responsibilities
            });
        }
    });
    
    // Education
    const education = [];
    document.querySelectorAll('.education-item').forEach((item, index) => {
        const school = item.querySelector('.edu-school').value.trim();
        const degree = item.querySelector('.edu-degree').value.trim();
        const dates = item.querySelector('.edu-dates').value.trim();
        const gpa = item.querySelector('.edu-gpa').value.trim();
        
        if (school && degree && dates) {
            const edu = { school, degree, dates };
            if (gpa) edu.gpa = gpa;
            education.push(edu);
        }
    });
    
    // Projects
    const projects = [];
    document.querySelectorAll('.project-item').forEach((item, index) => {
        const name = item.querySelector('.proj-name').value.trim();
        const description = item.querySelector('.proj-description').value.trim();
        const technologiesText = item.querySelector('.proj-technologies').value.trim();
        const technologies = technologiesText ? technologiesText.split(',').map(t => t.trim()).filter(t => t) : [];
        const url = item.querySelector('.proj-url').value.trim();
        
        if (name && description) {
            const proj = { name, description, technologies };
            if (url) proj.url = url;
            projects.push(proj);
        }
    });
    
    // Certifications
    const certifications = [];
    document.querySelectorAll('.cert-item').forEach((item, index) => {
        const name = item.querySelector('.cert-name').value.trim();
        const issuer = item.querySelector('.cert-issuer').value.trim();
        const date = item.querySelector('.cert-date').value.trim();
        const expiry = item.querySelector('.cert-expiry').value.trim();
        
        if (name) {
            const cert = { name };
            if (issuer) cert.issuer = issuer;
            if (date) cert.date = date;
            if (expiry) cert.expiry = expiry;
            certifications.push(cert);
        }
    });
    
    // Languages
    const languages = [];
    document.querySelectorAll('.language-item').forEach((item, index) => {
        const language = item.querySelector('.lang-language').value.trim();
        const proficiency = item.querySelector('.lang-proficiency').value;
        
        if (language) {
            languages.push({ language, proficiency });
        }
    });
    
    return {
        personal_info: personalInfo,
        summary,
        skills,
        experience,
        education,
        projects,
        certifications,
        languages
    };
}

function saveFullProfile(event) {
    event.preventDefault();
    
    const profileData = collectFormData();
    
    // Validation
    if (!profileData.personal_info.name || !profileData.personal_info.email || !profileData.summary) {
        showAlert('Please fill in all required fields (Name, Email, Summary)', 'error');
        return;
    }
    
    // Save profile
    fetch('/api/profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ profile: profileData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('✅ Profile saved successfully!', 'success');
            closeProfileEditor();
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('❌ Error saving profile: ' + (data.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        showAlert('❌ Network error: ' + error.message, 'error');
    });
}

// Make functions globally available
window.switchTab = switchTab;
window.loadProfile = loadProfile;
window.addExperience = addExperience;
window.removeExperience = removeExperience;
window.addEducation = addEducation;
window.removeEducation = removeEducation;
window.addProject = addProject;
window.removeProject = removeProject;
window.addCertification = addCertification;
window.removeCertification = removeCertification;
window.addLanguage = addLanguage;
window.removeLanguage = removeLanguage;
window.saveFullProfile = saveFullProfile;
