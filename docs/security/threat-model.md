# PSI Security Threat Model

**Status:** Phase 2.1 — Design documentation
**Method:** STRIDE-informed threat analysis
**Implementation status:** Proposed mitigations; not yet implemented or security-tested.

## 1. Purpose

This document identifies threats that could compromise PSI accounts, devices, sessions, files, permissions, storage-provider credentials and sharing operations.

It defines the expected prevention, detection and recovery controls for each threat.

This is a design-level threat model. It does not represent a completed penetration test or a guarantee that the proposed controls are effective.

## 2. Scope

The threat model covers:

- Owner accounts.
- Administrator accounts and delegated privileges.
- Trusted Users.
- Temporary Recipients.
- Viewer access.
- Web and future Android clients.
- Authentication and session management.
- Device registration and verification.
- Permission management.
- Invitations and OTP challenges.
- Credential storage.
- Internal backend requests.
- Database and audit records.
- External storage providers.
- Sharing and transfer operations.

## 3. Assets requiring protection

| Asset | Security objective |
|---|---|
| Owner account | Prevent unauthorized account control |
| User identities | Prevent impersonation and unauthorized changes |
| Device private keys | Prevent theft and unauthorized use |
| Sessions | Prevent hijacking and replay |
| Permissions | Prevent unauthorized privilege expansion |
| Invitations | Prevent unauthorized redemption |
| OTP challenges | Prevent interception, guessing and replay |
| Provider credentials | Prevent exposure and unauthorized provider access |
| Files and metadata | Preserve confidentiality and integrity |
| Transfer records | Preserve correctness and traceability |
| Audit events | Preserve integrity and accountability |
| Encryption keys | Prevent unauthorized decryption |
| Recovery records | Prevent false or unauthorized recovery |

## 4. Threat actors

Potential threat actors include:

- External attackers.
- Individuals who obtain a forwarded invitation.
- Attackers with access to a recipient's email or messaging account.
- Attackers with temporary access to an unlocked device.
- Malicious or compromised users.
- Attackers who obtain a stolen session credential.
- Attackers who compromise an application server or database.
- Attackers who compromise a connected storage-provider account.
- Malicious or compromised internal software components.

The threat model assumes that client devices and external provider responses may be compromised or untrusted.

## 5. Risk assessment approach

Each threat is assessed using:

- **Impact:** Potential consequence if exploited.
- **Attack surface:** Entry point or component exposed to the threat.
- **Prevention:** Controls intended to reduce the likelihood.
- **Detection:** Signals that may indicate an attack.
- **Recovery:** Response after the threat is detected.
- **Residual risk:** Risk that remains after proposed controls.

Initial risk labels are qualitative design estimates, not measured results.

## 6. Threat analysis

### T01 — Account compromise

**Category:** Spoofing / Credential compromise

**Description:** An attacker obtains the Owner's authentication credentials or otherwise gains control of the Owner's account.

**Impact:**
- Unauthorized access to personal storage.
- Unauthorized permission changes.
- Creation of malicious invitations.
- Exposure of connected storage accounts.
- Unauthorized sharing or deletion operations.

**Attack surface:**
- Login endpoints.
- Password or passkey recovery.
- Authentication challenges.
- Email or messaging accounts used for verification.
- Owner device security.

**Prevention:**
- Strong Owner authentication.
- Passkeys or MFA.
- Secure account recovery.
- Rate limits and login throttling.
- Device verification.
- Re-authentication for sensitive actions.
- Notifications for important security changes.

**Detection:**
- Repeated authentication failures.
- Login from an unrecognized device.
- Unexpected permission changes.
- Unexpected device registrations.
- Unusual invitation or sharing activity.

**Recovery:**
- Suspend the compromised account.
- Revoke active sessions.
- Revoke suspicious devices.
- Reset authentication credentials through a verified recovery process.
- Review recent permissions, invitations and audit events.

**Residual risk:** A compromised primary email or messaging account may undermine recovery and OTP delivery.

### T02 — Unauthorized resource access

**Category:** Elevation of Privilege / Information Disclosure

**Description:** A user accesses a file, folder, drive or operation outside the permissions explicitly granted to them.

**Impact:**
- Confidentiality breach.
- Unauthorized modification or deletion.
- Exposure of private metadata.
- Unauthorized storage operations.

**Attack surface:**
- API endpoints.
- Resource identifiers.
- File and folder operations.
- Download and sharing endpoints.
- Background jobs.

**Prevention:**
- Backend-enforced RBAC.
- Resource-specific permission checks.
- Action-level authorization.
- Ownership and tenant/resource boundary validation.
- Deny-by-default authorization.
- Authorization on every protected request.

**Detection:**
- Repeated denied resource requests.
- Access to unrelated resource identifiers.
- Unexpected access patterns.
- Authorization failures.

**Recovery:**
- Revoke inappropriate grants.
- Terminate affected sessions where necessary.
- Review exposed resources.
- Investigate audit records.
- Notify affected parties when appropriate.

**Residual risk:** Authorization mistakes may remain possible when new endpoints or resource types are introduced.

### T03 — Stolen session

**Category:** Spoofing

**Description:** An attacker obtains a valid session credential through malware, browser compromise, device theft or accidental exposure.

**Impact:**
- Account impersonation.
- Unauthorized access within the session's permission scope.
- Unauthorized file or sharing operations.

**Attack surface:**
- Browser cookies.
- Session tokens.
- Local device storage.
- Authentication responses.
- Session refresh mechanisms.

**Prevention:**
- Opaque high-entropy session tokens.
- Store only token hashes server-side.
- Secure, HttpOnly and appropriate SameSite cookies.
- CSRF protection.
- Idle and absolute expiry.
- Session rotation.
- Device association.
- No session credentials in URLs or logs.

**Detection:**
- Unexpected device or session activity.
- Concurrent-session anomalies.
- Session use after revocation.
- Unusual location or behavioral signals.

**Recovery:**
- Revoke the affected session.
- Revoke the device if compromise is suspected.
- Require re-authentication.
- Review actions performed during the compromised session.

**Residual risk:** Malware or an attacker controlling an unlocked device may operate within an otherwise valid session.

### T04 — Device impersonation

**Category:** Spoofing

**Description:** An attacker attempts to act as a registered PSI device without possessing its authorized cryptographic key.

**Impact:**
- Unauthorized session creation.
- Bypass of device restrictions.
- Access to protected resources.

**Attack surface:**
- Device registration.
- Device challenge-response.
- Session creation.
- Device recovery and replacement.

**Prevention:**
- Cryptographic device identity.
- Challenge-response verification.
- Browser WebAuthn/passkeys.
- Android Keystore-backed keys.
- Private keys retained on the device.
- Device revocation.
- New-device approval where required.

IP addresses and browser fingerprints must not be treated as sufficient proof of device identity.

**Detection:**
- Invalid signatures.
- Repeated challenge failures.
- Unexpected device registration.
- Attempts to use revoked device credentials.

**Recovery:**
- Revoke the affected device.
- Invalidate its sessions.
- Require verified device re-enrollment.
- Investigate related account activity.

**Residual risk:** Malware operating on a legitimately registered device may misuse its available capabilities.

### T05 — Forwarded invitation abuse

**Category:** Spoofing / Elevation of Privilege

**Description:** An invitation link is forwarded to another person or device, and that person attempts to redeem it.

**Impact:**
- Unauthorized recipient access.
- Exposure of shared resources.
- Abuse of temporary permissions.

**Attack surface:**
- Invitation URLs.
- Invitation redemption endpoint.
- OTP delivery.
- Device-binding workflow.

**Prevention:**
- High-entropy one-time invitation links.
- Protected invitation-token storage.
- OTP delivery only to the pre-registered destination.
- Cryptographic device binding after verification.
- One-time redemption.
- Invitation expiry and revocation.
- Owner approval option before OTP delivery.

Forwarding the link alone must never authorize another device.

**Detection:**
- Redemption from unexpected devices.
- Repeated redemption attempts.
- Expired or already-used invitation attempts.
- Unexpected recipient verification activity.

**Recovery:**
- Revoke the invitation.
- Revoke any resulting unauthorized session.
- Review access to affected resources.
- Issue a new invitation only after owner review.

**Residual risk:** An attacker who also compromises the registered OTP destination may attempt to complete verification.

### T06 — OTP interception or brute force

**Category:** Spoofing

**Description:** An attacker intercepts, guesses, reuses or manipulates an OTP challenge.

**Impact:**
- Unauthorized invitation redemption.
- Unauthorized access establishment.
- Recipient impersonation.

**Attack surface:**
- OTP generation.
- Email and messaging delivery.
- Verification endpoints.
- Destination-change workflows.

**Prevention:**
- Single-use OTP challenges.
- Five-minute default expiry.
- Maximum five verification attempts.
- Rate limits.
- Secure random OTP generation.
- OTP values stored as protected verifiers rather than plaintext.
- Destination changes restricted to verified Owner-controlled workflows.
- OTP destination must not be freely selected by a visitor.

**Detection:**
- Repeated incorrect OTP submissions.
- Excessive challenge generation.
- Expired challenge reuse.
- Unexpected OTP destination changes.

**Recovery:**
- Invalidate the challenge.
- Temporarily restrict further attempts.
- Revoke suspicious invitations.
- Verify the registered destination.
- Require a new challenge.

**Residual risk:** Compromise of the recipient's email or messaging account can expose delivered OTPs.

### T07 — Credential exposure

**Category:** Information Disclosure

**Description:** Passwords, tokens, private keys or other sensitive credentials are exposed through source code, logs, database records, API responses or development artifacts.

**Impact:**
- Account compromise.
- Storage-provider compromise.
- Unauthorized data access.
- Persistent access through stolen refresh tokens.

**Attack surface:**
- Environment files.
- Source control.
- Application logs.
- API responses.
- Error reporting.
- Database backups.
- Developer machines.

**Prevention:**
- Keep real secrets out of Git.
- Use `.env.example` placeholders only.
- Encrypt sensitive persistent credentials.
- Restrict credential access to authorized backend components.
- Never return provider tokens to the frontend.
- Redact secrets from exceptions and logs.
- Apply least-privilege access.
- Rotate exposed credentials.

**Detection:**
- Secret scanning.
- Unexpected credential access.
- Repository scanning.
- Unusual provider authentication activity.

**Recovery:**
- Revoke exposed credentials.
- Rotate affected keys and tokens.
- Remove exposed material from active systems.
- Review access logs.
- Assess whether historical repository or backup copies remain exposed.

**Residual risk:** Previously copied secrets may remain usable until revoked, even after removal from the current source tree.

### T08 — Privilege escalation

**Category:** Elevation of Privilege

**Description:** A user obtains permissions beyond those explicitly granted by the Owner or an authorized policy.

**Impact:**
- Unauthorized administrative control.
- Permission bypass.
- Access to private resources.
- Unauthorized security-setting changes.

**Attack surface:**
- Role assignment endpoints.
- Permission-management APIs.
- User-supplied role fields.
- Administrative functions.
- Internal service interfaces.

**Prevention:**
- Server-side authorization.
- Explicit privilege-assignment rules.
- Separate Owner and Administrator authority.
- Least privilege.
- Sensitive-operation approval.
- No trust in client-supplied role values.

**Detection:**
- Unexpected role changes.
- Unauthorized privilege-assignment attempts.
- Administrative operations outside expected scope.

**Recovery:**
- Revoke unauthorized privileges.
- Invalidate affected sessions.
- Review actions performed with elevated access.
- Restore approved permissions.

**Residual risk:** A compromised Owner account may legitimately perform actions that are otherwise reserved for the Owner.

### T09 — Permission-change abuse

**Category:** Tampering / Elevation of Privilege

**Description:** An attacker or unauthorized user changes resource permissions, schedules, restrictions or expiry settings.

**Impact:**
- Unauthorized access expansion.
- Loss of intended restrictions.
- Exposure of files or folders.
- Unauthorized recurring access.

**Attack surface:**
- Permission APIs.
- Sharing management.
- Invitation creation.
- Trusted-user management.

**Prevention:**
- Owner-controlled sensitive grants.
- Resource-specific authorization.
- Permission-change validation.
- Explicit approval where required.
- Audit records for every security-relevant change.
- Revalidation before background-job execution.

**Detection:**
- Unexpected grant changes.
- Permission expansion.
- Unusual recipient additions.
- Unexpected expiry or schedule modifications.

**Recovery:**
- Restore the approved permission state.
- Revoke affected sessions or invitations.
- Review resource access during the exposure window.

**Residual risk:** A valid privileged user may misuse permissions within their legitimate authority.

### T10 — Malicious internal request

**Category:** Tampering / Elevation of Privilege

**Description:** A compromised or incorrectly implemented internal module sends a request that bypasses expected authorization or attempts to modify another module's data.

**Impact:**
- Unauthorized data modification.
- Permission bypass.
- Credential misuse.
- Inconsistent application state.

**Attack surface:**
- Internal module interfaces.
- Background jobs.
- Shared service functions.
- Database access.
- Internal API calls.

**Prevention:**
- Documented module interfaces.
- Explicit identity and authorization context.
- Least-privilege service access.
- Module ownership of its business data.
- Input validation.
- No direct cross-module table modification.
- Sensitive-operation authorization at the owning module boundary.

**Detection:**
- Unexpected internal operations.
- Missing authorization context.
- Unusual database access.
- Audit events with invalid or absent initiating identity.

**Recovery:**
- Disable the affected operation or module.
- Revoke compromised service credentials.
- Investigate database and audit records.
- Restore verified data where necessary.

**Residual risk:** A fully compromised application process may have access to multiple internal capabilities.

### T11 — Storage-provider token theft

**Category:** Information Disclosure / Spoofing

**Description:** An attacker obtains a storage-provider access or refresh token.

**Impact:**
- Unauthorized access to connected cloud storage.
- Data disclosure, modification or deletion.
- Persistence through refresh-token use.

**Attack surface:**
- OAuth callback handling.
- Credential Vault.
- Database.
- Application logs.
- Backup files.
- Provider integration services.

**Prevention:**
- Minimum OAuth scopes.
- Encrypted token storage.
- Restricted Credential Vault access.
- No provider tokens in frontend code.
- No token logging.
- Secure OAuth callback validation.
- Token rotation and revocation.

**Detection:**
- Unexpected provider activity.
- Token reuse anomalies.
- Provider security alerts.
- Unexpected credential access.

**Recovery:**
- Revoke the affected provider token.
- Reauthorize the provider through a verified flow.
- Rotate relevant encryption keys if compromise is suspected.
- Review provider activity and affected files.

**Residual risk:** Provider-account compromise may expose data independently of PSI.

### T12 — Sharing abuse

**Category:** Information Disclosure / Repudiation

**Description:** A user or attacker creates unauthorized sharing links, grants excessive recipient permissions or distributes resources beyond their intended audience.

**Impact:**
- Unintended data exposure.
- Persistent external access.
- Unauthorized redistribution.

**Attack surface:**
- Sharing endpoints.
- Invitation creation.
- Recipient permissions.
- External provider sharing links.
- Access expiry and revocation.

**Prevention:**
- Explicit sharing permissions.
- Recipient and resource validation.
- Expiry and revocation.
- Owner approval for sensitive distribution.
- Restricted sharing scopes.
- Audit of sharing creation and changes.
- No silent external distribution.

**Detection:**
- Unusual sharing volume.
- Unexpected recipients.
- Permission expansion.
- Sharing outside configured restrictions.

**Recovery:**
- Revoke PSI-managed invitations and grants.
- Revoke provider links where supported.
- Notify the Owner.
- Review access records.

**Residual risk:** Revocation cannot erase copies already downloaded or independently redistributed.

### T13 — Replay attack

**Category:** Spoofing / Tampering

**Description:** An attacker resubmits a previously valid authentication challenge, OTP, invitation redemption request or sensitive operation.

**Impact:**
- Repeated unauthorized actions.
- Duplicate transfers or changes.
- Unauthorized session establishment.

**Attack surface:**
- Authentication endpoints.
- OTP verification.
- Invitation redemption.
- Transfer APIs.
- Sensitive operation endpoints.

**Prevention:**
- Single-use challenges.
- Nonces and timestamps where appropriate.
- Challenge expiry.
- Idempotency controls for appropriate operations.
- One-time invitation redemption.
- Server-side state validation.

**Detection:**
- Reused challenge identifiers.
- Duplicate redemption attempts.
- Repeated operation identifiers.
- Unexpected duplicate state transitions.

**Recovery:**
- Reject reused requests.
- Invalidate affected challenges.
- Reconcile operation state.
- Revoke suspicious sessions if necessary.

**Residual risk:** Poorly designed idempotency or concurrency controls may still allow duplicate side effects.

### T14 — Database compromise

**Category:** Information Disclosure / Tampering / Denial of Service

**Description:** An attacker obtains unauthorized database access or compromises the database host, backups or stored records.

**Impact:**
- Exposure of personal information.
- Modification of permissions and identities.
- Theft of encrypted credentials.
- Destruction or corruption of records.

**Attack surface:**
- Database service.
- Database credentials.
- Network access.
- Backup files.
- Administrative tools.
- Application database roles.

**Prevention:**
- Network restrictions.
- Least-privilege database accounts.
- Strong authentication.
- Encryption of sensitive fields.
- Separate encryption-key management.
- Protected backups.
- Database patching and access monitoring.

**Detection:**
- Unexpected database connections.
- Unusual query activity.
- Privilege changes.
- Integrity-check failures.
- Unexpected backup access.

**Recovery:**
- Isolate the compromised database.
- Revoke compromised credentials.
- Assess data exposure and integrity.
- Restore from a verified protected backup where necessary.
- Rotate relevant encryption keys.
- Reconcile affected records.

**Residual risk:** An attacker who obtains both encrypted data and its effective decryption keys may recover protected credentials.

PostgreSQL is planned but not configured in the current project foundation.

### T15 — Audit tampering

**Category:** Tampering / Repudiation

**Description:** An attacker modifies, deletes or forges audit records to conceal unauthorized activity or misrepresent an operation.

**Impact:**
- Loss of accountability.
- Inability to investigate incidents.
- False security conclusions.
- Concealed privilege or credential abuse.

**Attack surface:**
- Audit storage.
- Database administrative access.
- Audit-writing interfaces.
- Backup and restore processes.
- Application logging.

**Prevention:**
- Restricted audit-write interfaces.
- Separate audit access permissions.
- Append-only design where practical.
- Integrity verification.
- Protected backups.
- Hash chaining or external integrity anchoring where appropriate.
- No secrets in audit events.

A hash chain alone cannot prevent a privileged attacker from rewriting the entire database and recomputing the chain.

**Detection:**
- Integrity-check failures.
- Missing sequence numbers.
- Unexpected deletion or modification.
- Audit gaps.
- Disagreement between independent system records.

**Recovery:**
- Preserve available forensic copies.
- Restore verified audit backups.
- Investigate the integrity failure.
- Rotate compromised administrative credentials.
- Record the incident and known evidence gaps.

**Residual risk:** Fully privileged infrastructure compromise may undermine audit integrity unless independent protected evidence exists.

## 7. Cross-cutting security controls

The following controls apply across multiple threats:

### Authentication
- Strong Owner authentication.
- Passkeys or MFA.
- Secure recovery.
- Rate limiting.
- Re-authentication for sensitive operations.

### Authorization
- RBAC plus resource-specific permissions.
- Deny-by-default.
- Backend enforcement.
- Explicit approval for sensitive operations.
- Permission revalidation for delayed jobs.

### Device security
- Cryptographic device identity.
- Private keys retained on devices.
- Device revocation.
- Session invalidation after revocation.

### Session security
- Opaque random session credentials.
- Server-side session validation.
- Idle and absolute expiry.
- Secure cookies.
- Session rotation and revocation.

### Credential protection
- Authenticated encryption.
- Key separation.
- Restricted credential access.
- Token rotation and revocation.
- Secret redaction.

### Monitoring
- Security audit events.
- Authentication-failure detection.
- Device and session anomaly detection.
- Permission-change monitoring.
- Provider-token activity monitoring.

## 8. Incident response lifecycle

The proposed incident response sequence is:

1. Detect suspicious activity.
2. Record available evidence.
3. Classify severity and affected assets.
4. Contain the incident.
5. Revoke affected sessions, devices, invitations or credentials.
6. Investigate affected resources and operations.
7. Restore verified data or configuration where necessary.
8. Notify the Owner and affected parties when appropriate.
9. Document findings and corrective actions.
10. Review the threat model and tests.

Incident response must not claim successful recovery until the recovered state has been verified.

## 9. Important PSI security invariants

The following rules are mandatory design constraints:

- Authentication does not automatically grant resource access.
- Forwarding an invitation link alone cannot authorize a new device.
- A visitor cannot select an arbitrary OTP destination.
- IP address and browser fingerprint alone do not prove device identity.
- Private device keys remain on the device.
- Provider credentials are never exposed to frontend code.
- A disconnected drive does not automatically mean data loss.
- Multiple connected drives do not automatically constitute a backup.
- A partial transfer must never be marked complete.
- The official file location must not change before destination verification.
- A migration source must not be deleted before verification and explicit approval.
- Duplicate files must not be automatically deleted.
- Recovery must not be claimed without verification.
- Revocation prevents future access but cannot erase downloaded copies.
- Sensitive operations must be authorized and auditable.
- Audit records must not contain secrets.

## 10. Residual risks and open decisions

The following decisions remain open and must be resolved before their corresponding implementation:

- Production encryption-key management.
- Whether end-to-end encryption is required.
- OTP provider selection and delivery costs.
- Public sharing gateway domain and TLS deployment.
- Provider OAuth scopes.
- Backup retention and recovery policy.
- Audit retention and independent integrity storage.
- Legal and privacy obligations.
- File size and transfer limits.
- Security monitoring and alert delivery.
- Incident notification requirements.

No open decision should be silently treated as finalized.

## 11. Review requirements

This threat model must be reviewed:

- Before implementing authentication.
- Before implementing device registration.
- Before implementing the Credential Vault.
- Before enabling external sharing.
- Before connecting storage providers.
- Before production deployment.
- Whenever a significant security boundary or trust assumption changes.

## 12. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/credential-vault.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`