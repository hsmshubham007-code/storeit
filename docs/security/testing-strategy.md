# PSI Security Testing Strategy

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Test strategy proposed; security-specific automated tests are not yet implemented.

## 1. Purpose

This document defines how PSI security controls will be tested before and during implementation.

Security testing must verify that the system rejects unauthorized actions, protects credentials, enforces device and session boundaries, records security events and fails safely.

The strategy covers unit, integration, API, negative, regression and security-focused testing.

Passing tests provides evidence for the tested scenarios. It does not prove that PSI is completely secure.

## 2. Testing principles

1. Test security requirements alongside functional requirements.
2. Prefer automated tests for repeatable security controls.
3. Test denied and malformed requests, not only successful workflows.
4. Verify authorization at the backend boundary.
5. Test cross-user and cross-resource access attempts.
6. Test expiry, revocation, replay and concurrency behavior.
7. Use synthetic accounts, devices, credentials and files.
8. Never use real provider credentials or personal data in test fixtures.
9. Avoid tests that modify real user data or external accounts.
10. Preserve existing Phase 1 health tests and regression coverage.
11. Record evidence for security acceptance decisions.
12. Do not interpret an untested control as implemented or verified.

## 3. Test environments

### 3.1 Local development

The initial security test environment should run locally on the developer's machine.

Requirements:

- Use synthetic test identities.
- Use isolated test configuration.
- Use temporary test data.
- Avoid company systems, accounts, networks and databases.
- Do not use production secrets.
- Keep test artifacts out of source control when they contain sensitive data.

### 3.2 Automated test environment

Automated tests should run without requiring real cloud-provider accounts.

Mock provider responses and synthetic cryptographic fixtures may be used where appropriate.

Tests requiring external services must be explicitly identified and separated from the default offline suite.

### 3.3 Database testing

A future database integration test suite may use an isolated disposable test database after database architecture and implementation are approved.

Tests must never silently connect to or modify a production or shared database.

PostgreSQL is not configured as part of Phase 2.1.

## 4. Test categories

### 4.1 Unit tests

Test individual security components independently.

Examples:

- Role and permission evaluation.
- Resource ownership checks.
- Session expiry calculations.
- Invitation state transitions.
- OTP expiry and attempt limits.
- Device credential verification.
- Credential encryption and decryption.
- Secret-redaction filters.
- Audit event validation.
- Detection rule evaluation.

### 4.2 Integration tests

Verify interactions between security components.

Examples:

- Authentication followed by session creation.
- Device verification followed by session binding.
- Invitation redemption followed by device registration.
- Permission checks before resource operations.
- Session revocation after device revocation.
- Credential storage through the Credential Vault.
- Audit event generation for security-sensitive operations.

### 4.3 API security tests

Verify that HTTP endpoints enforce authentication, authorization, input validation and safe error behavior.

Tests must cover:

- Missing authentication.
- Invalid authentication.
- Expired sessions.
- Revoked sessions.
- Invalid request bodies.
- Unexpected fields.
- Unauthorized resource identifiers.
- Unsupported operations.
- Excessive request rates.
- Safe error responses.

### 4.4 Negative and adversarial tests

Attempt to violate the security model.

Examples:

- A Viewer attempts a write operation.
- A Trusted User accesses an ungranted resource.
- A Temporary Recipient attempts access after invitation expiry.
- A user attempts to access another user's resource.
- A forwarded invitation is opened from an unauthorized device.
- An expired OTP is submitted.
- An OTP is reused.
- An attacker submits repeated OTP guesses.
- A revoked device attempts authentication.
- A stolen or revoked session credential is replayed.
- A user attempts to grant permissions beyond their authority.
- A client attempts to provide an arbitrary OTP destination.

### 4.5 Regression tests

Every security defect that is fixed should have a regression test where practical.

Existing passing behavior must remain intact unless an approved design change requires otherwise.

## 5. Identity and authentication test strategy

When identity implementation begins, test:

- Successful authentication.
- Incorrect credentials.
- Disabled and suspended accounts.
- Authentication rate limits.
- Authentication state changes.
- Secure logout.
- Session creation only after successful verification.
- Reauthentication for sensitive operations.
- Recovery flow authorization.
- Account enumeration resistance where applicable.

Tests must verify that error responses do not reveal sensitive authentication details.

## 6. Permission testing strategy

Test the combination of:

- Principal.
- Role.
- Resource.
- Requested action.
- Resource-specific grant.
- Resource ownership.
- Grant status and expiry.

Required cases:

1. Owner can perform permitted owner operations.
2. Administrator is restricted to delegated privileges.
3. Trusted User can perform only explicitly granted actions.
4. Temporary Recipient is restricted to invitation scope.
5. Viewer cannot perform write or administrative operations.
6. Revoked grants are immediately rejected by new authorization decisions.
7. Expired grants are rejected.
8. Cross-user resource access is denied.
9. Resource identifiers cannot be used to bypass authorization.
10. Permission changes cannot be silently overridden by an existing session.

Tests must verify backend enforcement even when the frontend hides or disables an action.

## 7. Invitation and OTP testing strategy

Test the approved Option B workflow.

Required cases:

- Valid invitation redemption.
- Invalid invitation identifier.
- Expired invitation.
- Revoked invitation.
- Already redeemed invitation.
- OTP delivered only to the pre-registered destination.
- Invalid OTP.
- Expired OTP.
- Reused OTP.
- OTP attempt-limit enforcement.
- Rate limiting across relevant identifiers.
- Owner approval required before OTP delivery.
- Owner approval rejected.
- Forwarded link opened from another device.
- Device binding after successful OTP verification.
- Unauthorized attempts to change the delivery destination.

OTP values must be synthetic test data and must never appear in test logs or committed fixtures.

## 8. Device identity testing strategy

### Browser

Test:

- Valid WebAuthn registration.
- Valid assertion.
- Invalid signature.
- Incorrect challenge.
- Replayed challenge.
- Incorrect origin.
- Incorrect relying-party identifier.
- Revoked credential.
- Suspended device.
- Device approval requirement.
- Session binding to the verified device.

### Android

When the Android client is introduced, test:

- Keystore-backed key generation.
- Public-key registration.
- Challenge-response verification.
- Private-key non-exportability where supported.
- Invalid proof.
- Device revocation.
- Replacement-device enrollment.

Platform security claims must be based on verified capabilities, not assumed hardware support.

## 9. Session security testing strategy

Test:

- Secure session creation.
- Session credential unpredictability.
- Idle expiration.
- Absolute expiration.
- Concurrent-session limits.
- Session renewal.
- Credential rotation where implemented.
- Logout invalidation.
- Owner-initiated revocation.
- Device-triggered session revocation.
- Account suspension.
- Permission reduction during an active session.
- Replayed revoked session credentials.
- Missing or unavailable session state.

Verify that clearing a client cookie alone does not substitute for backend session invalidation.

## 10. Credential Vault testing strategy

Test:

- Successful encryption and decryption.
- Ciphertext integrity verification.
- Incorrect or unavailable key.
- Modified ciphertext.
- Modified nonce or authentication tag.
- Unauthorized credential retrieval.
- Credential isolation between owners.
- Credential replacement.
- Token refresh failure.
- Credential revocation.
- Key-version migration.
- Backup restoration behavior.

Verify that:

- Plaintext credentials are never persisted.
- Frontend responses never contain provider tokens.
- Logs and audit events contain no secrets.
- Database-only access does not reveal plaintext credentials.
- Encryption failure does not fall back to plaintext storage.

Use synthetic credentials and test keys only.

## 11. Audit and threat detection testing strategy

Test:

- Required events are generated.
- Event timestamps are assigned by trusted backend code.
- Event structure is validated.
- Correlation identifiers are preserved.
- Secret fields are rejected or redacted.
- Unauthorized audit queries are denied.
- Unauthorized audit modification is prevented.
- Repeated OTP failures trigger configured detection.
- Repeated authentication failures trigger configured detection.
- Revoked credential use is denied and recorded.
- Suspicious permission changes generate appropriate signals.
- Alert-delivery failures are handled safely.
- Audit persistence failures follow the approved fail-safe policy.

Tests must not mistake alert generation for successful incident containment.

## 12. API and application security checks

The future API should be evaluated for:

- Broken access control.
- Broken authentication.
- Injection vulnerabilities.
- Unsafe input handling.
- Cross-site scripting (XSS).
- Cross-site request forgery (CSRF).
- Server-side request forgery (SSRF), where outbound request functionality exists.
- Insecure direct object references.
- Security misconfiguration.
- Sensitive information exposure.
- Unsafe file handling.
- Rate-limit bypass.
- Replay attacks.
- Insecure session management.

Only test features that exist. Do not claim that a vulnerability class has been addressed merely because it appears in this strategy.

## 13. Dependency and configuration checks

Before adding security dependencies:

1. Check Python and Node.js compatibility.
2. Review package maintenance and security history.
3. Prefer established, maintained libraries.
4. Review transitive dependencies.
5. Avoid unnecessary dependencies.
6. Pin or constrain versions appropriately.
7. Review vulnerability advisories.
8. Document why each dependency is required.

Configuration checks should verify:

- Debug behavior is appropriate for the environment.
- Secrets are not committed.
- Production configuration does not use development defaults.
- HTTPS is required in deployed environments.
- CORS is restricted to approved origins.
- Cookies use appropriate security attributes.
- Error responses do not expose stack traces or secrets.

No new security dependency is authorized by this Phase 2.1 document.

## 14. Test data and secret handling

All security tests must use synthetic data.

Do not use:

- Real provider refresh tokens.
- Real API keys.
- Real passwords.
- Real OTP delivery destinations.
- Real personal documents.
- Production session credentials.
- Company data or accounts.

Test secrets must be isolated and discarded after testing.

Test output must be reviewed for accidental secret disclosure.

## 15. Security test evidence

For each security requirement, record:

- Requirement identifier.
- Test name.
- Component under test.
- Preconditions.
- Expected result.
- Actual result.
- Test environment.
- Pass or fail.
- Defect reference, if applicable.
- Date of verification.

A test result must not be marked as passed without execution evidence.

A skipped or unimplemented test must remain visibly incomplete.

## 16. Proposed implementation sequence

| Order | Test scope | Dependency |
|---|---|---|
| 1 | Test framework and security test conventions | Existing Phase 1 foundation |
| 2 | Identity and authentication tests | Owner authentication implementation |
| 3 | Permission and resource-scope tests | Permission Engine |
| 4 | Invitation and OTP tests | Invitation and OTP implementation |
| 5 | Device identity tests | Device registration implementation |
| 6 | Session lifecycle tests | Session Management |
| 7 | Credential Vault tests | Credential Vault implementation |
| 8 | Audit and detection tests | Audit service |
| 9 | Cross-module security regression | Integrated security components |

The sequence follows the approved Phase 2.2–2.7 implementation roadmap. Test coverage should be added alongside each implementation rather than postponed until the end.

## 17. Acceptance criteria

Phase 2 security implementation must not be considered complete until:

- Unauthorized requests are rejected by backend controls.
- Role and resource permissions are enforced.
- Expired and revoked invitations cannot authorize access.
- Forwarded invitation links alone cannot authorize another device.
- OTP expiry, reuse and attempt limits are enforced.
- Device verification uses cryptographic proof.
- Revoked devices cannot continue using their credentials.
- Expired and revoked sessions are rejected.
- Credential secrets are not exposed through APIs, logs or audit records.
- Credential encryption and integrity checks are verified.
- Security-relevant actions produce appropriate audit events.
- Audit access is restricted.
- Relevant threat detection rules are tested.
- Regression tests pass.
- Known residual risks are documented.

These criteria apply to implemented and tested controls. Documentation alone does not satisfy implementation acceptance.

## 18. Implementation status

| Capability | Status |
|---|---|
| Security test strategy | Documented |
| Threat coverage | Documented |
| Identity test plan | Documented |
| Permission test plan | Documented |
| Invitation and OTP test plan | Documented |
| Device test plan | Documented |
| Session test plan | Documented |
| Credential Vault test plan | Documented |
| Audit and detection test plan | Documented |
| Automated security test suite | Not implemented |
| Security acceptance execution | Deferred until implementation |

## 19. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/credential-vault.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`