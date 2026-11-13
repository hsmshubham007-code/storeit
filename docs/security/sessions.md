# PSI Session Management Architecture

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Proposed session controls; session management is not yet implemented.

## 1. Purpose

This document defines how PSI creates, validates, maintains, expires, and revokes authenticated sessions.

Sessions represent an authenticated period of access. They must be associated with the correct user, authorization context and, where required, a verified device.

A valid session does not grant unrestricted access. Every protected operation must still pass the Permission Engine.

## 2. Session security principles

1. Sessions must be created only after successful authentication or an approved invitation-redemption flow.
2. Session identifiers and credentials must be cryptographically unpredictable.
3. Session credentials must be protected in transit and at rest where persisted.
4. Sessions must have idle and absolute expiration limits.
5. High-risk operations may require recent authentication or additional verification.
6. Session privileges must reflect current account and resource permissions.
7. Revoked users and devices must not continue using existing sessions.
8. Session credentials must never appear in logs, URLs or audit records.
9. Logout and revocation must invalidate server-side session state.
10. Session validation must fail securely when session state cannot be established.

## 3. Session categories

PSI distinguishes the following access contexts:

| Category | Description |
|---|---|
| Owner | Primary account owner with full account control |
| Administrator | Delegated account-management access |
| Trusted User | Recurring access within explicitly granted permissions |
| Temporary Recipient | Time-limited access granted through an invitation |
| Viewer | Read-only access within the assigned resource scope |

Session policy must account for the actual privileges granted, not merely the displayed role name.

## 4. Proposed session defaults

The following are initial design defaults, not implemented settings.

| Access category | Idle timeout | Absolute lifetime | Concurrent sessions |
|---|---:|---:|---:|
| Owner | 15 minutes | 12 hours | 5 |
| Trusted User | 30 minutes | 12 hours | 3 |
| Temporary Recipient | 15 minutes | 4 hours | 1 |

Administrator and Viewer session limits remain policy decisions. They should be derived from their effective privileges and risk profile rather than assigned arbitrary fixed limits.

The Owner must be able to revoke sessions. Security policy may impose stricter limits where required.

## 5. Session creation

The proposed sequence is:

1. Client completes the applicable authentication flow.
2. Backend validates the authentication result.
3. Backend checks account status.
4. Backend checks device registration and approval requirements.
5. Backend establishes the effective access category and authorization context.
6. Backend generates a cryptographically secure session credential.
7. Backend stores the corresponding server-side session state.
8. Session expiry and device-binding information are recorded.
9. The client receives the session credential through a protected transport.
10. PSI records a session-creation audit event without recording the credential.

Failed authentication or device verification must not produce an active session.

## 6. Session credential handling

Session credentials must:

- Be generated using a cryptographically secure random generator.
- Have sufficient entropy to resist guessing.
- Be transmitted only over HTTPS in deployed environments.
- Never be placed in URLs or query strings.
- Never be written to application logs.
- Be invalidated on logout, revocation or applicable security events.

For the browser client, the preferred design is a Secure, HttpOnly cookie with an appropriate SameSite policy.

The cookie must be scoped to the minimum required host and path.

State-changing browser requests must also have appropriate CSRF protection. SameSite settings alone must not be treated as the complete CSRF defense.

For a future Android client, the session credential should be stored using appropriate platform-protected storage and transmitted in an authorization header over TLS.

The browser and Android clients must not share session credentials through insecure storage or application logs.

## 7. Session binding

Where device-bound access is required, a session must be associated with the verified device registration.

The backend should validate:

- Session identifier.
- Session status.
- Associated user.
- Associated device, where required.
- Device registration status.
- Session expiry.
- Account status.
- Relevant security restrictions.

A copied invitation link or stolen session credential must not be treated as proof that a different device is authorized.

Cryptographic device proof may be required for sensitive operations or higher-risk sessions.

## 8. Session renewal

Session renewal must not extend the absolute lifetime indefinitely.

A renewal operation must:

1. Validate the existing session.
2. Check account and device status.
3. Check whether the session is eligible for renewal.
4. Enforce idle and absolute expiration limits.
5. Rotate session credentials when required by policy.
6. Invalidate superseded credentials.
7. Record the renewal event without logging secrets.

A revoked, expired or otherwise invalid session must not be renewed.

## 9. Reauthentication and step-up verification

PSI may require recent authentication or additional verification before sensitive actions.

Examples include:

- Changing account security settings.
- Registering a new trusted device.
- Changing a verified OTP destination.
- Granting Administrator permissions.
- Creating or changing a sharing invitation.
- Revoking a security control.
- Accessing credential-management operations.
- Initiating sensitive recovery operations.

The exact step-up policy will be defined with the corresponding feature.

A session's existence must never bypass the authorization requirements for these actions.

## 10. Logout and revocation

### 10.1 User logout

Logout must:

1. Invalidate the current server-side session.
2. Clear the client-side session credential.
3. Prevent further use of the invalidated credential.
4. Record the logout event.

Clearing a browser cookie without invalidating server-side state is insufficient.

### 10.2 Owner-initiated revocation

The Owner or an authorized security administrator may revoke sessions within their permitted scope.

Revocation must:

- Invalidate the selected session.
- Prevent further authenticated requests using it.
- Record the initiating identity and target session.
- Notify the Owner where appropriate.

### 10.3 Security-triggered revocation

Sessions may be revoked after:

- Account suspension.
- Device revocation.
- Credential compromise.
- Password or primary authentication changes, when policy requires.
- Invitation expiry or revocation.
- Security incident response.
- Permission or identity changes requiring session invalidation.

Revocation must take effect on the backend, not merely in the client interface.

## 11. Session storage

The proposed server-side session record may contain:

| Field | Purpose |
|---|---|
| Session ID | Internal session identifier |
| User ID | Associated principal |
| Device ID | Associated device, where applicable |
| Access category | Session category at creation |
| Created at | Session creation time |
| Last activity at | Last accepted activity |
| Idle expiry | Idle expiration time |
| Absolute expiry | Maximum session lifetime |
| Status | Active, expired or revoked |
| Revoked at | Revocation timestamp |
| Revocation reason | Non-secret reason code |

Do not store raw session credentials in the database.

The implementation must choose a secure credential-verification strategy appropriate to the session-token format.

## 12. Permission changes during a session

Session creation must not permanently freeze authorization.

The Permission Engine must evaluate current permissions for protected operations.

When permissions are reduced or revoked:

- New requests must use the updated permissions.
- Sensitive operations already queued must be reassessed before execution.
- Sessions may be invalidated when the change affects the user's security standing.
- Authorization decisions must be auditable.

A session must not preserve access that the user no longer has.

## 13. Concurrent sessions

Concurrent-session limits must be enforced by the backend.

When a limit is reached, PSI must apply a documented policy, such as rejecting a new session or requiring the user to revoke an existing one.

PSI must not silently terminate an unrelated session without an explicit policy and audit event.

The Owner should be able to review and revoke active sessions.

## 14. Failure handling

Session validation must fail securely when:

- The session record is missing.
- The credential is invalid.
- The session is expired or revoked.
- The associated account is disabled.
- Required device verification fails.
- Session state cannot be retrieved reliably.
- The session's authorization context is invalid.

The API must return an appropriate authentication or authorization error without revealing session secrets or internal security details.

## 15. Implementation status

| Capability | Status |
|---|---|
| Session lifecycle design | Documented |
| Session timeout defaults | Proposed |
| Browser cookie strategy | Proposed |
| Android secure-storage strategy | Proposed |
| Device-bound session design | Documented |
| Session renewal | Designed |
| Logout and revocation | Designed |
| Step-up authentication policy | Deferred to feature design |
| Server-side session implementation | Not implemented |
| Automated session security tests | Planned |

## 16. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/credential-vault.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`