# PSI Security Baseline

**Status:** Phase 1 foundation with Phase 2.1 security design documented
**Implementation status:** Baseline development rules are established. The security controls described in the Phase 2.1 documents are not yet implemented.

## 1. Purpose

This document establishes the minimum security rules for PSI development.

These rules apply throughout local development and future implementation phases.

## 2. Secrets and credentials

- Keep local development secrets in an ignored `.env` file.
- Never commit `.env` files, passwords, access tokens, refresh tokens, API keys or private keys.
- Commit only placeholder values in `.env.example`.
- Never paste real credentials into source code, documentation, issue reports or test fixtures.
- Do not expose secrets through API responses, exceptions, application logs or audit events.
- Use synthetic credentials and test data for automated testing.
- Do not add cloud-provider credentials until the relevant integration is designed and explicitly approved.

## 3. Development environment and data

- Use local development resources only for the current PSI foundation.
- Do not use company accounts, credentials, files, databases, services, networks or systems.
- Do not copy company or third-party confidential data into PSI.
- Keep development and test data separate from any future production data.
- Do not connect external services without an explicitly approved integration design.
- Do not perform destructive operations on real or shared data without explicit authorization.

## 4. Authentication and authorization

- Do not claim authentication exists until it is implemented and tested.
- Do not treat frontend visibility or disabled controls as authorization.
- Enforce protected operations at the backend boundary.
- Apply role-based and resource-specific permission checks.
- Do not allow a Trusted User or Temporary Recipient to exceed explicitly granted permissions.
- Do not treat an invitation link alone as proof of identity or device authorization.
- Do not allow unverified changes to registered OTP destinations.
- Revoke sessions and device credentials when required by approved security policies.

## 5. Device and session security

- Device identity must rely on cryptographic verification where device binding is required.
- Keep private device keys on their respective devices.
- Do not treat IP addresses or browser fingerprints as sufficient identity proof.
- Enforce session expiry and server-side revocation.
- Do not store session credentials in URLs or logs.
- A revoked device or session must not retain future authorized access.

## 6. Credential protection

- Provider credentials must remain within the backend Credential Vault boundary once implemented.
- Do not expose provider tokens to frontend code.
- Use authenticated encryption and a separately managed key-encryption mechanism as approved by the final vault design.
- Do not store production encryption keys alongside encrypted credentials.
- Do not use plaintext credential storage as a fallback.
- Define provider-specific token rotation and revocation behavior before integration.

## 7. File and transfer safety

- Do not report a transfer as complete before destination verification.
- Do not update the official file location before destination verification succeeds.
- Do not delete a migration source before successful verification and explicit Owner approval.
- Preserve original archives when extraction and organization are requested.
- Do not execute uploaded files or archive contents.
- Do not automatically delete suspected duplicate files.
- Do not report recovery as successful without verifying the recovered copy.
- Do not treat multiple connected drives as automatic backup or redundancy.

## 8. Sharing and external access

- Apply explicit resource permissions to shared files and folders.
- Enforce invitation expiry and revocation.
- Require the approved OTP and device-binding workflow for one-time recipient access.
- Do not silently distribute files or create external sharing links.
- Do not claim that revocation removes copies already downloaded by recipients.
- Trusted recurring access must remain within the Owner-approved grant.

## 9. Audit and privacy

- Record security-relevant operations through the approved audit interface once implemented.
- Never include passwords, OTP values, session credentials, provider tokens, private keys or encryption keys in audit records.
- Restrict audit access according to authorization policy.
- Minimize collection of personal and device information.
- Define retention and deletion policies before production use.
- Do not claim audit integrity or threat detection is operational until implemented and tested.

## 10. Dependencies and implementation

- Review dependency compatibility, maintenance and security before adding packages.
- Avoid unnecessary dependencies.
- Do not install or introduce a database, provider SDK or security service outside the approved phase scope.
- Preserve existing functionality and tests when changing code.
- Verify changes with appropriate tests and evidence.
- Do not commit, push, deploy or modify shared resources without explicit authorization.

## 11. Implementation status

The Phase 2.1 documents describe the intended security architecture and controls.

They do not establish that the following features are operational:

- Authentication and account recovery.
- Role and resource authorization.
- Device registration and verification.
- Session creation and revocation.
- Credential encryption and key management.
- Audit persistence and threat detection.
- Secure provider integration.
- Automated security testing.

Each feature must be implemented, tested and reviewed before being represented as available.

## 12. Related documentation

- `docs/architecture/overview.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/architecture.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/credential-vault.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`