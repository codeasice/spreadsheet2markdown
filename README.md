# Spreadsheet2Markdown Project

This project converts Excel spreadsheets to markdown files with frontmatter.

## Overview
A Streamlit web application that allows users to:
- Upload Excel spreadsheets
- Select columns for different markdown components
- Generate markdown files with frontmatter
- Download all generated files as a ZIP

## Project Structure
- `spreadsheet2markdown.py` - Main Streamlit application
- `requirements.txt` - Project dependencies
- `/generated_markdown/` - Output directory for converted markdown files
- `.streamlit/` - Streamlit configuration (if needed)

## Dependencies
- streamlit >= 1.43.2
- pandas >= 2.2.3
- openpyxl >= 3.1.2

## Installation
```bash
# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Development
Standard imports used in the project:
```python
import streamlit as st
import pandas as pd
from io import BytesIO
import os
import zipfile
```

### Generated Markdown Format
The generated markdown files will follow this structure:
```markdown
---
title:
labels: []
---

## Section
Content
```

## Usage
1. Start the Streamlit app:
```bash
streamlit run spreadsheet2markdown.py
```

2. Clean generated files (if needed):
```bash
rm -rf generated_markdown/*.md
```

3. Create output directory (if needed):
```bash
mkdir -p generated_markdown
```

# 📝 Spreadsheet2Markdown

**Spreadsheet2Markdown** is a simple **Streamlit app** that converts Excel spreadsheets into structured Markdown files. This tool allows users to dynamically select columns for filenames, properties, labels, and sections, making it easy to generate Markdown documentation from tabular data.

## 🚀 Features
- Upload an Excel file (`.xlsx`)
- Select a **column for filenames**
- Optionally choose a **column for folder organization**
- Map spreadsheet columns to:
  - **Frontmatter properties** (YAML format)
  - **Labels** (tags for categorization)
  - **Sections** (headers with corresponding text)
- **Preview the Markdown output** before exporting
- Download all generated Markdown files as a ZIP archive

---

## 🎥 Demo
[![Watch the video](https://img.shields.io/badge/Demo-Click_Here-blue)](LINK_TO_VIDEO)
(Screenshot or video walkthrough link here)

---

## 🛠 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/codeasice/spreadsheet2markdown.git
cd spreadsheet2markdown
