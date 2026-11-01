# NyayaSetu AI - Backend (Django REST Framework)

West Bengal Government Scheme & Citizen Rights Assistant API.

## Architecture & Features

1. **Schemes Directory (`apps.schemes`)**:
   - West Bengal welfare schemes catalog (*Lakshmir Bhandar*, *Krishak Bandhu*, *Kanyashree*, *Jai Johar*, etc.).
   - Dynamic eligibility matching wizard (`/api/schemes/check-eligibility/`).
   - Mandatory document checklists and common rejection remedies catalog.

2. **Notice & SMS Decrypter (`apps.analyzer`)**:
   - Multimodal Gemini AI service for parsing application status SMS, letters, and receipts (`/api/analyzer/explain/`).
   - Translates bureaucratic jargon into plain Bengali (বাংলা), English, and Hindi with step-by-step physical remedy actions.

3. **Grievance Drafter (`apps.grievances`)**:
   - Generates formal, respectful representations in Bengali or English addressed to BDO, SDO, or Duare Sarkar counters (`/api/grievances/generate/`).
   - Directory of official nodal desks and helpline portals.

4. **Accounts & Tracking (`apps.accounts`)**:
   - Supabase JWT token verification for seamless citizen login (`core.supabase_auth.SupabaseAuthentication`).
   - Bookmarked schemes, saved document checklists, and application status tracking.

## Quick Start

### 1. Activate Environment
```bash
# Windows PowerShell
.\backend\.venv\Scripts\Activate.ps1
```

### 2. Configure Environment (`backend/.env`)
Set your Supabase credentials and Google Gemini API key:
```env
SUPABASE_URL=https://[YOUR-PROJECT].supabase.co
SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
SUPABASE_JWT_SECRET=[YOUR-JWT-SECRET]
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[YOUR-PROJECT].supabase.co:5432/postgres
GEMINI_API_KEY=[YOUR-GEMINI-API-KEY]
```
*(By default, the backend falls back safely to local SQLite and mock pattern matching if keys are not yet configured).*

### 3. Run Migrations & Seed Data
```bash
python backend/manage.py migrate
python backend/manage.py seed_wb_data
```

### 4. Run Development Server
```bash
python backend/manage.py runserver 8000
```
API Root: `http://127.0.0.1:8000/api/`  
Admin Panel: `http://127.0.0.1:8000/admin/`
