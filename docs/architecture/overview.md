# PSI Architecture Overview

**Status:** Initial foundation with Phase 2.1 security design documented
**Implementation status:** The application skeleton exists. The security architecture is documented but its controls are not yet implemented.

## 1. Project architecture

PSI uses a **modular-monolith architecture**.

The backend remains a single deployable application containing clearly separated domain and security modules. Modules communicate through documented interfaces and contracts rather than directly modifying another module's internal data.

The initial technology foundation is:

- **Frontend:** React 19, TypeScript and Vite.
- **Backend:** Python 3.14, FastAPI and Uvicorn.
- **Database:** PostgreSQL planned for a later phase; not currently configured.
- **Storage providers:** Provider integrations will be isolated behind adapters when implemented.
- **Initial environment:** Local Windows development.
- **Future client:** Android application using the same versioned backend API.

## 2. Core functional systems

PSI is designed around six major functional systems:

1. **Storage Intelligence and Allocation** — selects suitable storage destinations based on capacity, health, file characteristics and user preferences.
2. **File Intelligence** — analyzes, categorizes, indexes and manages file metadata, archives and duplicate detection.
3. **Drive Management** — manages connected storage providers, account status, capacity and provider health.
4. **Transfer Management** — coordinates uploads, downloads, migration, verification and transfer lifecycle.
5. **Sharing Intelligence** — manages invitations, recipient access, sharing permissions and revocation.
6. **Availability and Recovery** — detects availability problems and coordinates verified recovery operations.

These systems are architectural responsibilities, not a statement that their functionality is already implemented.

## 3. Security architecture

Security is a cross-cutting responsibility enforced through backend boundaries.

The documented security design includes:

- Identity and authentication.
- Role-based and resource-specific authorization.
- Device identity and cryptographic verification.
- Device-bound sessions.
- Invitation and OTP verification.
- Credential Vault for future provider credentials.
- Session lifecycle and revocation.
- Security audit events and threat detection.
- Security-focused automated testing.

The design preserves the following access categories:

- Owner.
- Administrator.
- Trusted User.
- Temporary Recipient.
- Viewer.

The Permission Engine must evaluate both the principal's role and the requested action on the specific resource.

## 4. Security boundaries

The proposed trust boundaries separate:

- Browser and future Android clients.
- Backend API and request validation.
- Identity and session management.
- Device verification.
- Permission enforcement.
- Functional domain modules.
- Credential Vault.
- Persistent application and audit data.
- External storage providers.

Frontend controls are not security boundaries. Protected operations must be validated by the backend.

Provider credentials and device private keys must not be exposed to frontend code or ordinary business modules.

## 5. Invitation and device-bound access

The approved invitation design uses a one-time device-bound workflow:

1. Recipient opens a unique invitation.
2. PSI validates the invitation.
3. OTP is delivered to a pre-registered destination.
4. Recipient verifies the OTP.
5. The device establishes cryptographic identity.
6. PSI binds access to the verified device.
7. The Permission Engine enforces the granted resource and action scope.

Forwarding the invitation link alone must not authorize another device.

The design also supports access requests and recurring Trusted User access with explicit permissions, restrictions, device policies and revocation.

## 6. Proposed backend organization

The backend is expected to evolve into modules such as:

- `api` — versioned HTTP routes and request validation.
- `identity` — account authentication and identity lifecycle.
- `authorization` — roles, permissions and resource access decisions.
- `devices` — device registration and verification.
- `sessions` — session creation, expiry and revocation.
- `credentials` — protected provider credential operations.
- `audit` — security event recording and investigation support.
- `storage` — storage provider abstractions and drive management.
- `files` — file metadata and intelligence.
- `transfers` — transfer lifecycle and verification.
- `sharing` — invitations and sharing workflows.
- `recovery` — availability and recovery coordination.

This is a proposed logical organization. It does not authorize creating all modules during Phase 2.1.

## 7. Architecture invariants

The following rules must remain true as implementation progresses:

- Backend authorization is required for every protected operation.
- Resource permissions must be checked independently of frontend visibility.
- Device identity must use cryptographic proof where device binding is required.
- IP addresses and browser fingerprints are not sufficient proof of identity.
- Private device keys remain on their devices.
- Provider credentials must not be exposed through APIs or logs.
- Revoked sessions and devices must not retain future access.
- Forwarded invitation links alone must not authorize access.
- A migration source must not be deleted before destination verification and explicit approval.
- A transfer must not be reported complete before verification.
- Duplicate detection must not automatically delete files.
- Recovery must not be reported successful without verification.
- Disconnection of a storage provider must not be treated as data deletion.
- Multiple storage providers must not automatically be treated as backup.
- Revocation cannot guarantee removal of files already downloaded by recipients.

## 8. Architecture documentation

The following documents describe the current design:

- `docs/architecture/security-boundaries.md` — trust boundaries and protected flows.
- `docs/security/architecture.md` — overall security architecture.
- `docs/security/threat-model.md` — threats, mitigations and residual risks.
- `docs/security/identity-and-access.md` — roles, permissions and access workflows.
- `docs/security/device-identity.md` — browser and Android device identity.
- `docs/security/credential-vault.md` — credential encryption and lifecycle.
- `docs/security/sessions.md` — session lifecycle and revocation.
- `docs/security/audit-and-detection.md` — audit and threat detection.
- `docs/security/testing-strategy.md` — security test plan.

## 9. Implementation status and limitations

The current repository contains the initial frontend and backend foundation.

The following are not yet implemented:

- Owner authentication.
- Role and resource permission enforcement.
- Device registration and cryptographic verification.
- Session management.
- Credential Vault.
- Audit persistence and threat detection.
- Database migrations and PostgreSQL integration.
- Cloud storage provider integrations.
- File upload, transfer and sharing workflows.
- Verified recovery functionality.

Phase 2.1 establishes design documentation only. Subsequent implementation phases require their own scoped work and verification.
