# PSI backend

FastAPI application for the Personal Storage Infrastructure project.

## Setup

Run these commands from the `backend` directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Run the API

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Health endpoint: `http://127.0.0.1:8000/api/v1/health`

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```
