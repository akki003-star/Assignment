# AI Job Application Agent

An AI-powered web application that automatically searches for jobs, customizes resumes, applies to suitable positions, and notifies users via email when clarification is needed.

## Features

- **Authentication** — Sign up, login, JWT-based auth, password reset, profile management
- **Resume Management** — Upload (PDF/TXT), parsing, versioning, AI-powered optimization
- **Job Search** — Multi-source search with keyword, location, and salary filtering
- **AI Matching Engine** — Match score calculation, skill gap analysis, recommendations
- **Auto Apply Engine** — Automated form filling, resume & cover letter submission
- **Communication** — Email notifications for confirmations, updates, and clarification requests
- **Dashboard** — Application tracking, status updates, analytics

## Tech Stack

| Layer      | Technology                     |
|------------|-------------------------------|
| Frontend   | React 18, Tailwind CSS, Vite  |
| Backend    | Python, FastAPI               |
| Database   | PostgreSQL                    |
| AI         | OpenAI API                    |
| Automation | Playwright                    |
| Email      | Gmail API                     |
| Cache      | Redis                         |
| Deploy     | Docker, Docker Compose        |

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── core/            # Config, security, dependencies
│   │   ├── db/              # Database session, base
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── tests/               # Unit tests
│   ├── alembic/             # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   └── context/         # React context (auth)
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick Start

### Using Docker (Recommended)

```bash
cp .env.example .env
# Edit .env with your API keys
docker-compose up --build
```

- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:3000

### Manual Setup

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint                         | Description                |
|--------|----------------------------------|----------------------------|
| POST   | /api/v1/auth/register            | Create account             |
| POST   | /api/v1/auth/login               | Login                      |
| GET    | /api/v1/auth/me                  | Get profile                |
| PUT    | /api/v1/auth/me                  | Update profile             |
| POST   | /api/v1/auth/password-reset      | Request password reset     |
| POST   | /api/v1/resumes/upload           | Upload resume              |
| GET    | /api/v1/resumes/                 | List resumes               |
| POST   | /api/v1/resumes/optimize         | AI-optimize resume for job |
| POST   | /api/v1/jobs/search              | Search jobs                |
| GET    | /api/v1/jobs/{id}                | Get job details            |
| GET    | /api/v1/jobs/{id}/match-score    | Get AI match score         |
| POST   | /api/v1/applications/apply       | Apply to job               |
| GET    | /api/v1/applications/            | List applications          |
| GET    | /api/v1/applications/dashboard   | Dashboard stats            |
| PUT    | /api/v1/applications/{id}/status | Update application status  |

## Database Schema

- **Users** — Authentication, profile, preferences
- **Resumes** — File storage, versioning, parsed content
- **Jobs** — Aggregated job listings from multiple sources
- **Applications** — Application records with match scores
- **Application_Statuses** — Status history tracking
- **Email_Notifications** — Email log and status
- **User_Responses** — Clarification Q&A

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

## Security

- JWT Authentication with bcrypt password hashing
- CORS protection
- File upload validation and size limits
- Rate limiting (configurable)
- Audit logging

## Environment Variables

See `.env.example` for all configuration options.

## License

MIT
