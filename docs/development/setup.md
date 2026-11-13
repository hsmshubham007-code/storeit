# Local development setup

## Prerequisites

- Python 3.14
- Node.js 24 LTS
- npm
- Git

PostgreSQL is intentionally not part of this initial skeleton. The database
decision and local installation will be handled in a later, separately approved step.

## Backend

Open PowerShell in `backend/`:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Check `http://127.0.0.1:8000/api/v1/health`.

## Frontend

Open another PowerShell window in `frontend/`:

```powershell
npm install
npm run dev
```

Open the local URL printed by Vite (the configured address is
`http://127.0.0.1:5173`).

## Tests

From `backend/`:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Moving to another computer

Push committed source code to the private GitHub repository. On the laptop,
clone the repository and repeat the local setup steps. Virtual environments,
`node_modules`, local databases, and `.env` files are not transferred through Git.
