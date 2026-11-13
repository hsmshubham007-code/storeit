# PSI architecture — initial foundation

PSI uses a modular-monolith approach:

- React + TypeScript responsive web client
- Python + FastAPI backend
- PostgreSQL planned for persistent application data in a later phase
- Provider integrations isolated behind adapters when implemented

The backend remains a single deployable application with domain modules and
explicit interfaces. A future Android client can use the same versioned API.

This is an initial project foundation, not a production-ready architecture or
security implementation.
