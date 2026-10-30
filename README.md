# SURAKSHA — Adaptive Community Disaster Intelligence Platform (ACDIP)

## Project Overview
SURAKSHA is a disaster management platform designed to support disaster information sharing, emergency rescue, shelter management, and relief coordination in Bangladesh.

**Course:** CSE471 — System Analysis and Design  
**Institution:** BRAC University

## Technology Stack
- **Language:** Python
- **Backend Framework:** Flask
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** MySQL
- **ORM:** Flask-SQLAlchemy / SQLAlchemy
- **Database Migrations:** Flask-Migrate
- **MySQL Driver:** PyMySQL
- **Environment Variables:** python-dotenv
- **Code Editor:** Visual Studio Code
- **Version Control:** Git and GitHub
- **Local Server:** XAMPP MySQL

## Required Software
Install these before starting:
- Python 3.11 or later
- Git
- XAMPP (for MySQL)
- Visual Studio Code (recommended)

## How to Clone and Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/PronoyPramanick/CSE471-ACDIP.git
```

### 2. Open the Project Folder
```bash
cd CSE471-ACDIP
```

### 3. Create a Virtual Environment
```bash
python -m venv .venv
```

### 4. Activate the Environment (Windows)
```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Required Packages
```bash
python -m pip install -r requirements.txt
```

### 6. Configure MySQL
- Start MySQL from XAMPP.
- Create a database named `suraksha_db`.
- Create a `.env` file in the project root and configure the database credentials according to your local MySQL setup.

Example:
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=suraksha_db
DB_USER=root
DB_PASSWORD=
```

### 7. Run the Application
```bash
flask --app app db upgrade
python app.py
```

Open in your browser: http://127.0.0.1:5000

## Important Notes
- Each team member must create their own virtual environment.
- Each team member must configure their own `.env` file and local database.
- Never upload `.env` or `.venv/` to GitHub.
- Use separate Git branches for assigned tasks.
- Keep `requirements.txt` updated when dependencies change.

## Project Status
Under Development
