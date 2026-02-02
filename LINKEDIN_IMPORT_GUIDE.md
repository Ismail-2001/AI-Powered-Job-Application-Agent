# LinkedIn Import Guide

## Overview
Import your LinkedIn profile data to automatically populate your profile, avoiding manual data entry and repetition.

## Methods

### Method 1: LinkedIn Data Export (Recommended)

1. **Export Your LinkedIn Data**:
   - Go to LinkedIn Settings & Privacy
   - Click "Data Privacy" → "Get a copy of your data"
   - Select "Want something in particular?" → "Profile"
   - Click "Request archive"
   - Wait for email (usually takes a few minutes)
   - Download the ZIP file

2. **Extract and Import**:
   - Extract the ZIP file
   - Find `Profile.json` inside
   - Use the import feature in the web interface or CLI

### Method 2: LinkedIn URL (Manual Template)

1. **Get Your LinkedIn URL**:
   - Go to your LinkedIn profile
   - Copy the URL (e.g., `https://www.linkedin.com/in/yourname/`)

2. **Import**:
   - Use the LinkedIn import feature
   - Enter your LinkedIn URL
   - Fill in the template with your information

## Features

✅ **Automatic Import**:
- Personal information (name, email, location)
- Work experience (all positions)
- Education (all degrees)
- Skills (categorized automatically)
- Summary/About section

✅ **Deduplication**:
- Automatically removes duplicate entries
- Prevents repetition in CV generation

✅ **Smart Categorization**:
- Automatically categorizes skills (Languages, Frameworks, Tools)
- Uses heuristics to identify skill types

## Usage

### Via Web Interface

1. Click "Edit Profile"
2. Look for "Import from LinkedIn" button
3. Choose export file or enter URL
4. Review and save

### Via Python

```python
from utils.linkedin_importer import import_linkedin_profile

# From export file
profile = import_linkedin_profile(export_path="path/to/Profile.json")

# From URL (creates template)
profile = import_linkedin_profile(linkedin_url="https://www.linkedin.com/in/yourname/")
```

## Benefits

1. **Saves Time**: No manual data entry
2. **No Repetition**: Automatic deduplication
3. **Complete Data**: Imports all your LinkedIn information
4. **Smart Filtering**: Only relevant experiences in CVs

## Notes

- LinkedIn export format may vary - the importer handles common formats
- Some fields may need manual review/adjustment
- Skills categorization is heuristic-based and may need refinement
- All imported data is automatically deduplicated
