# PSI Credential Vault Architecture

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Proposed credential-protection design; no credential vault or provider integration is currently implemented.

## 1. Purpose

This document defines how PSI will protect sensitive credentials used to authenticate with external storage providers and other integrated services.

The Credential Vault must prevent credentials from being exposed through frontend code, logs, API responses, source control, database queries or unauthorized internal modules.

The design is intended for future provider integrations. No real provider credentials are required or permitted as part of Phase 2.1.

## 2. Security principles

1. Provider credentials must never be exposed to frontend clients.
2. Plaintext credentials must not be stored in persistent application data.
3. Encryption keys must be separated from encrypted credential records.
4. Only explicitly authorized backend components may request credential operations.
5. Access must follow least privilege.
6. Credentials must not appear in logs, audit events, exceptions or API responses.
7. Provider tokens must be revocable and replaceable.
8. Credentials must be protected in backups and during recovery.
9. Compromise of the database alone should not automatically reveal plaintext credentials.
10. Credential operations must be attributable and auditable.

## 3. Protected credential types

The future vault may protect:

- OAuth access tokens.
- OAuth refresh tokens.
- Provider API credentials where applicable.
- Provider-specific authorization material.
- Other integration secrets explicitly approved for storage.

Passwords, device private keys and Owner authentication credentials have separate security requirements. They must not be treated as ordinary provider tokens.

## 4. Proposed architecture

The Credential Vault is a restricted backend security module.

Business modules request narrowly scoped credential operations through documented interfaces. They do not directly read encrypted credential records or encryption keys.

Proposed flow:

1. A provider integration requests authorization.
2. The OAuth or provider authorization flow completes.
3. The backend validates the authorization response.
4. The Credential Vault receives the credential material.
5. The vault encrypts the credential before persistent storage.
6. Encrypted data and required non-secret metadata are stored.
7. An authorized backend operation requests a credential when needed.
8. The vault checks the requesting component's authorization.
9. The vault decrypts the credential within the protected backend execution boundary.
10. The authorized provider adapter uses the credential.
11. Credential use and lifecycle changes are audited without recording the secret.

## 5. Encryption design

### 5.1 Authenticated encryption

The proposed encryption baseline is AES-256-GCM.

It provides confidentiality and integrity protection for credential data.

Each encryption operation must use a unique nonce with the required algorithm-specific length and usage limits.

The stored encrypted record should include:

- Ciphertext.
- Nonce.
- Authentication tag, if stored separately by the chosen implementation.
- Encryption algorithm identifier.
- Key version identifier.
- Credential record identifier.
- Non-secret metadata required for retrieval and migration.

Authenticated decryption must fail if ciphertext, nonce, tag or authenticated metadata has been modified.

### 5.2 Envelope encryption

The proposed design uses envelope encryption:

- A Data Encryption Key (DEK) encrypts an individual credential or credential group.
- A Key Encryption Key (KEK) protects the DEK.
- Encrypted credential data and the protected DEK may be stored together.
- The KEK must be managed separately from the application database.

The KEK must not be stored in the same database as the encrypted credentials.

### 5.3 Key management

Production KEK storage and management remain an open architecture decision.

Potential options include:

- An operating-system-protected local key store for an appropriately limited local deployment.
- A dedicated secrets-management service.
- A managed Key Management Service (KMS).
- A hardware security module where justified.

The selected option must be evaluated for availability, recovery, access control, cost and operational complexity before implementation.

A plain environment variable containing the production KEK is not an adequate long-term production key-management strategy.

## 6. Credential storage model

A proposed credential record may contain:

| Field | Purpose |
|---|---|
| Credential ID | Unique internal identifier |
| Owner ID | Account owner association |
| Provider ID | Connected provider reference |
| Credential type | Access token, refresh token or other type |
| Ciphertext | Encrypted credential material |
| Nonce | Encryption nonce |
| Key version | Encryption-key version reference |
| Scopes | Granted provider scopes |
| Created at | Record creation time |
| Updated at | Last credential update |
| Expires at | Provider credential expiry, if known |
| Status | Active, expired, revoked or failed |
| Revoked at | Revocation timestamp, if applicable |

Do not store plaintext access tokens or refresh tokens in these records.

Do not place secrets in filenames, database identifiers or searchable metadata.

## 7. Access control

Credential access must be restricted to explicitly authorized backend operations.

Requirements:

- Frontend requests must never receive provider tokens.
- Business modules must not access KEKs directly.
- Credential operations must validate the requesting component and relevant account ownership.
- Access must be limited to the required provider and credential.
- Credential retrieval must not be exposed as a general-purpose API endpoint.
- Credential access must be auditable.
- Administrative access must not automatically grant plaintext credential visibility.

The vault should expose narrowly scoped operations such as:

- Store a newly authorized credential.
- Retrieve a credential for an authorized provider operation.
- Refresh or replace a credential.
- Revoke a credential.
- Delete a credential according to approved retention policy.

## 8. OAuth token lifecycle

When a provider integration is implemented, the lifecycle should be:

1. Begin an approved provider authorization flow.
2. Validate the authorization response and state.
3. Exchange the authorization code through the backend.
4. Validate the provider response.
5. Store tokens through the Credential Vault.
6. Use access tokens only for authorized provider requests.
7. Refresh tokens through the backend when appropriate.
8. Rotate stored token material after successful refresh.
9. Revoke provider authorization when the Owner disconnects the account, where supported.
10. Record lifecycle events without recording token values.

Provider-specific refresh and revocation behavior must be verified against each provider's documented API.

## 9. Rotation and revocation

### 9.1 Credential rotation

Rotation should support:

- Replacing expired or compromised provider tokens.
- Re-encrypting credential data after encryption-key changes.
- Tracking encryption-key versions.
- Migrating records without exposing plaintext outside the protected execution boundary.

Rotation must not leave the only usable credential copy in an incomplete or unverified state.

### 9.2 Credential revocation

When a credential is revoked:

1. Mark the credential inactive.
2. Prevent future vault retrieval.
3. Stop relevant provider operations where possible.
4. Revoke the provider token through the provider's supported mechanism where appropriate.
5. Remove or retain encrypted data according to the approved retention policy.
6. Record the revocation event.

Revoking a PSI credential does not necessarily revoke a token already stolen by an attacker. Provider-side revocation is required where supported.

## 10. Logging and audit protection

The vault must never log:

- Access-token values.
- Refresh-token values.
- Passwords.
- Private keys.
- Encryption keys.
- OTP values.
- Authorization codes.
- Plaintext credential payloads.

Audit events may record:

- Credential identifier.
- Provider identifier.
- Initiating identity or service.
- Operation type.
- Timestamp.
- Outcome.
- Relevant correlation identifier.

Audit records must not contain the credential itself or a reversible representation of it.

## 11. Backup and recovery

Encrypted credential records and their key-management dependencies must be handled separately but consistently.

Requirements:

- Protect encrypted credential backups.
- Protect KEKs independently.
- Restrict backup access.
- Test recovery procedures.
- Verify integrity before restoring credentials.
- Document key-version compatibility.
- Prevent backup restoration from silently reactivating revoked credentials.

A backup containing encrypted credentials is not recoverable unless the required authorized key material is also available.

## 12. Threats and failure handling

The vault must fail securely when:

- Encryption fails.
- Authenticated decryption fails.
- A key version is unavailable.
- The requesting component is unauthorized.
- A credential is expired or revoked.
- A provider refresh operation fails.
- Credential integrity cannot be established.

The application must not fall back to plaintext storage or expose secrets in error messages.

## 13. Implementation status

| Capability | Status |
|---|---|
| Credential Vault architecture | Documented |
| AES-256-GCM proposal | Documented |
| Envelope encryption proposal | Documented |
| KEK management selection | Open decision |
| Encrypted credential storage | Not implemented |
| Credential access controls | Planned |
| OAuth integration | Deferred |
| Token rotation | Planned |
| Token revocation | Planned |
| Credential audit events | Planned |
| Backup and key recovery | Design required |

## 14. Open decisions

Before implementation, decide:

- Production KEK storage mechanism.
- Local-development key handling.
- Whether a dedicated KMS is justified.
- Key rotation intervals and triggers.
- Credential retention after provider disconnection.
- Provider-specific token refresh and revocation behavior.
- Backup retention and recovery responsibilities.
- Whether end-to-end encryption is required for user files.

These decisions must not be silently treated as finalized.

## 15. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`