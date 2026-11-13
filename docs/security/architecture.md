# PSI Security Architecture

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Planned; security controls described here are not yet implemented unless explicitly stated otherwise.

## 1. Purpose

This document defines the proposed security architecture for Personal Storage Infrastructure (PSI).

PSI is designed to provide a unified interface for managing personal storage accounts, files, transfers, sharing and recovery. Security must protect the owner's account, registered devices, storage-provider credentials, files, permissions and sharing operations.

The architecture must support the initial responsive web application and a future Android client without requiring a backend redesign.

## 2. Architecture principles

The security architecture follows these principles:

1. **Owner control:** The Owner retains ultimate control over account access, permissions and sensitive operations.
2. **Least privilege:** Every identity receives only the permissions required for its assigned responsibilities.
3. **Explicit authorization:** Authentication alone never grants access to every resource.
4. **Device verification:** Sensitive sessions must be associated with a cryptographically verified device.
5. **Secure credential handling:** Provider credentials must never be exposed to the frontend or written to logs.
6. **Defense in depth:** Multiple independent controls protect important operations.
7. **Revocation:** Invitations, devices, sessions and permissions must be revocable.
8. **Auditability:** Security-sensitive operations must produce attributable audit events.
9. **Fail securely:** Missing, expired or invalid security evidence must not result in access.
10. **Honest implementation status:** A designed control must not be represented as an operational feature before implementation and testing.

## 3. Application architecture

PSI will use a modular-monolith architecture.

The initial technology stack is:

- Frontend: React and TypeScript.
- Backend: Python and FastAPI.
- Database: PostgreSQL planned for a later phase; not currently configured.
- Initial environment: Local Windows development.
- Future client: Android application using the same versioned backend API.

Security responsibilities will be implemented as backend modules with documented interfaces.

The frontend is an untrusted client. It may display permissions and security status, but it must never be the final authority for access decisions.

## 4. Security components

### 4.1 Identity Gateway

The Identity Gateway is the entry point for authenticated API requests.

Responsibilities:

- Identify the requesting principal.
- Validate authentication evidence.
- Validate session status and expiry.
- Verify device association and device status.
- Reject invalid or revoked credentials.
- Pass verified identity context to authorization services.

### 4.2 Identity and Account Manager

Responsibilities:

- Owner authentication.
- User identity records.
- Trusted-user lifecycle.
- Temporary-recipient lifecycle.
- Account status and recovery.
- Authentication challenge management.

An Administrator is a delegated role and does not automatically receive Owner-level control.

### 4.3 Device Identity Manager

Responsibilities:

- Device registration.
- Cryptographic public-key registration.
- Challenge-response verification.
- Device status and trust records.
- Device revocation.
- Session invalidation following device revocation.

Browser clients are expected to use WebAuthn/passkeys where appropriate. Android clients are expected to use Android Keystore-backed keys.

Private keys remain on the device. The backend stores public-key material and associated device metadata.

### 4.4 Permission Engine

Responsibilities:

- Role-based access control (RBAC).
- Resource-specific permissions.
- Action-level authorization.
- Permission expiry and scheduling.
- Device and session restrictions.
- Sensitive-operation approval requirements.
- Permission revocation.

The Permission Engine must make the authoritative access decision on the backend.

### 4.5 Credential Vault

Responsibilities:

- Protect storage-provider credentials.
- Encrypt sensitive credential material.
- Separate encryption keys from encrypted data.
- Restrict access to credential operations.
- Support credential rotation and revocation.
- Prevent credentials from appearing in application logs or API responses.

Provider integrations and real provider credentials are outside the current Phase 2.1 implementation scope.

### 4.6 Session Manager

Responsibilities:

- Session creation and validation.
- Idle and absolute expiry.
- Session rotation.
- Concurrent-session limits.
- Session revocation.
- Refresh-token rotation and reuse detection, if refresh credentials are used.

### 4.7 Audit and Threat Detection

Responsibilities:

- Record security-sensitive events.
- Associate events with identities, devices and sessions.
- Detect repeated authentication failures.
- Detect suspicious device and session activity.
- Record permission and invitation changes.
- Support incident investigation and response.

Audit records must not contain passwords, OTP values, private keys, access tokens or provider secrets.

## 5. Authorization request flow

Every protected request should follow this sequence:

1. Receive the API request.
2. Validate the authentication credential.
3. Resolve the requesting identity.
4. Validate the session and expiry.
5. Verify the registered device and its status.
6. Identify the requested resource and action.
7. Evaluate role-based permissions.
8. Evaluate resource-specific grants and restrictions.
9. Check time, expiry, device and approval conditions.
10. Reject the request if any mandatory condition fails.
11. Pass authorized work to the owning business module.
12. Record the security-relevant outcome in the audit system.
13. Return the API response.

A frontend route guard or hidden interface element is not an authorization control.

## 6. Access categories

PSI preserves three principal access categories:

- **Owner:** Primary account owner with ultimate control.
- **Trusted User:** A recurring user with explicitly granted permissions.
- **Temporary Recipient:** A user receiving limited, time-bound access.

The system also defines delegated roles:

- **Administrator:** Performs explicitly delegated administrative operations.
- **Viewer:** Receives read-only access within assigned resource boundaries.

Roles and access categories must not be treated as interchangeable. A person's identity category and their resource-specific permissions are evaluated separately.

## 7. Invitation and temporary access security

PSI uses the approved Option B device-bound invitation workflow.

The proposed flow is:

1. Owner creates an invitation.
2. Owner selects the recipient, permissions, expiry and pre-registered OTP destination.
3. PSI generates a unique, high-entropy invitation link.
4. The first device opening the invitation starts the verification process.
5. OTP is delivered only to the pre-registered destination.
6. Recipient submits the OTP.
7. PSI validates the OTP, expiry and attempt limit.
8. The device is associated with a cryptographic public key.
9. PSI creates a limited device-bound session.
10. The Permission Engine enforces the invitation's resource and action restrictions.
11. The invitation redemption and resulting access are audited.

The Owner may choose automatic OTP delivery or approval before OTP delivery.

Supported design channels are WhatsApp and email, with SMS as an optional fallback.

Forwarding the invitation link alone must never authorize another device.

## 8. Access Request Gateway

A visitor may request access to the application or a specific resource.

The request may include:

- Requested resource.
- Reason for access.
- Contact information.
- Device registration information.

The Owner can approve or reject the request.

Approval must define the permitted resource scope and duration. The visitor must not be allowed to choose an arbitrary OTP destination.

## 9. Trusted recurring access

Trusted User access is an approved PSI requirement.

The design supports:

- Persistent or time-limited access.
- Granular resource permissions.
- Restrictions and schedules.
- Device limits.
- Owner approval for new devices.
- OTP re-verification when required.
- Suspension and revocation.
- Audit records for access changes.

Full implementation may occur in a later release. It must not be silently removed from the architecture.

## 10. Security boundaries

Security boundaries separate:

1. Frontend and backend.
2. Identity and authorization.
3. Authorization and business modules.
4. Application and credential vault.
5. Application and persistent storage.
6. Application and external storage providers.
7. Owner-controlled operations and recipient-controlled actions.

Each module must access another module's capabilities through documented interfaces rather than directly modifying another module's internal data.

See `docs/architecture/security-boundaries.md`.

## 11. Backend structure proposal

The following structure is a proposed organization for future implementation. It does not mean these modules already exist.

```text
backend/
  app/
    api/
      v1/
        router.py
    core/
      config.py
      security.py
      exceptions.py
    modules/
      identity/
      permissions/
      devices/
      credentials/
      audit/
    main.py
  tests/
    security/
```

Existing Phase 1 files must be preserved. New source modules will be introduced only in their approved implementation phases.

## 12. Security failure handling

The system must fail closed when:

- Authentication evidence is invalid.
- A session has expired or been revoked.
- A device is revoked or cannot be verified.
- A permission is missing or expired.
- An invitation has already been redeemed.
- OTP verification fails or exceeds the attempt limit.
- Required owner approval is absent.
- Credential integrity verification fails.

Security errors must not disclose secrets, internal keys or sensitive implementation details.

## 13. Implementation status

| Capability | Phase 2.1 status |
|---|---|
| Security architecture | Documented |
| Security boundaries | Documented |
| Threat model | Documented |
| Identity management | Planned |
| Permission engine | Planned |
| Device identity | Planned |
| Credential vault | Planned |
| Session management | Planned |
| Audit and detection | Planned |
| Automated security tests | Planned |
| PostgreSQL configuration | Deferred |
| Provider integrations | Deferred |

The existing application currently contains the initial Phase 1 foundation. This document does not claim that authentication, authorization, encryption, device verification, session management or auditing are operational.

## 14. Related documents

- `docs/architecture/overview.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/baseline.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/credential-vault.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`
