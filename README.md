# Personal Storage Infrastructure (PSI)

PSI is a local-first personal storage management project. The initial client is a
responsive web application. The backend is designed as a modular monolith so
additional clients, including a future Android application, can use the same API.

## Project layout

- `frontend/` — React + TypeScript web client
- `backend/` — Python + FastAPI API
- `docs/` — architecture, security, and development notes
- `scripts/` — project maintenance scripts

## Local development

See `docs/development/setup.md` for setup instructions.

## Security basics

- Never commit `.env` files, passwords, access tokens, private keys, or real user data.
- `.env.example` contains placeholders only.
- Do not connect company systems or use company data for PSI.
- Do not configure cloud storage providers until their integration is explicitly planned and approved.

## Current phase

Phase 1 — Project Foundation. This repository currently contains only the initial
application skeleton. Storage providers, database migrations, authentication,
uploads, and sharing are not implemented yet.
