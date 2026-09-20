# Support CRM Ticketing System

A full-stack customer support ticketing system built with FastAPI, SQLite, and vanilla JS/Tailwind CSS. Supports creating tickets, searching/filtering, and updating status with notes.

**Live demo:** [your-railway-url-here]
**Demo video:** [your-youtube-link-here]

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** SQLite + SQLAlchemy ORM
- **Frontend:** HTML, Tailwind CSS (CDN), Vanilla JavaScript
- **Deployment:** Railway.app

## Features

- Create tickets with customer info, subject, and description
- Auto-generated sequential ticket IDs (e.g. `TKT-001`)
- List all tickets with live search (name, ID, email, description)
- Filter tickets by status (Open / In Progress / Closed)
- Detail view per ticket with full description and note history
- Update ticket status and append notes

## Project Structure

```
support-crm/
├── app/
│   ├── main.py         # FastAPI app + routes
│   ├── database.py     # DB engine/session setup
│   ├── models.py       # SQLAlchemy models (Ticket, Note)
│   ├── schemas.py       # Pydantic request/response schemas
│   └── crud.py          # Database query logic
├── static/
│   ├── index.html       # Ticket list + search + filter
│   ├── create.html      # New ticket form
│   └── ticket.html       # Ticket detail + update
├── requirements.txt
├── Procfile
├── .env.example
└── .gitignore
```

## API Endpoints

| Method | Endpoint                  | Description                          |
|--------|----------------------------|---------------------------------------|
| POST   | `/api/tickets`              | Create a new ticket                   |
| GET    | `/api/tickets`               | List tickets (`?status=`, `?search=`) |
| GET    | `/api/tickets/{ticket_id}`   | Get full ticket detail + notes        |
| PUT    | `/api/tickets/{ticket_id}`   | Update status and/or add a note       |

## Local Setup

1. **Clone the repo**
```bash
   git clone https://github.com/YOUR_USERNAME/support-crm.git
   cd support-crm
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   # Mac/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Run the app**
```bash
   uvicorn app.main:app --reload
```

5. **Open it**
   - App: `http://127.0.0.1:8000/static/index.html`
   - API docs: `http://127.0.0.1:8000/docs`

The SQLite database file (`support_crm.db`) is created automatically on first run.

## Deployment

Deployed on [Railway](https://railway.app). The `Procfile` defines the start command:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Known Tradeoffs

- **SQLite on Railway's ephemeral filesystem**: data resets on redeploy. Acceptable for this assignment's scope; a production version would use a persistent Postgres database.
- **Ticket ID generation** uses a row count (`TKT-001`, `TKT-002`, ...) for readability, which has a theoretical race condition under concurrent writes at scale — a UUID or DB auto-increment would be more robust for high-concurrency production use.
