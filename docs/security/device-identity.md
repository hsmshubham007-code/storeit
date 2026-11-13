# PSI Device Identity Architecture

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Proposed device identity controls; not yet implemented.

## 1. Purpose

This document defines how PSI registers, verifies, manages and revokes devices associated with user identities.

Device identity is a security control separate from account authentication. A valid account credential alone must not establish that a request originates from an approved device.

The design supports the initial browser-based application and a future Android client.

## 2. Device identity principles

1. Device identity must rely on cryptographic proof.
2. Private keys must remain on the device.
3. The backend stores public-key material and device registration metadata.
4. Device registration must be associated with an authenticated or verified enrollment flow.
5. Device revocation must prevent future use of that device's credentials.
6. Sessions must be associated with registered device identity where device binding is required.
7. IP addresses and browser fingerprints are risk signals, not proof of identity.
8. New-device enrollment may require Owner approval according to account policy.
9. Device recovery and replacement must not silently bypass verification.
10. Device operations must produce audit events.

## 3. Supported client environments

### 3.1 Browser client

The React web application is expected to use WebAuthn/passkeys for cryptographic authentication and device-associated proof.

WebAuthn uses a registered credential and a challenge-response protocol. The browser and authenticator protect the private key material.

The backend verifies the response using the registered public-key information and the expected challenge and origin.

The application must validate:

- Challenge freshness and single use.
- Expected origin.
- Expected relying-party identifier.
- Credential identifier.
- Signature validity.
- User-verification requirements where configured.
- Credential registration status.
- Credential revocation status.

A browser profile or browser fingerprint alone is not a cryptographic device identity.

### 3.2 Future Android client

The future Android application is expected to use Android Keystore-backed cryptographic keys.

Requirements:

- Generate device keys using Android platform cryptographic facilities.
- Keep private keys within the protected Keystore boundary.
- Register corresponding public-key material with PSI.
- Use challenge-response verification.
- Apply appropriate key-use restrictions.
- Support device revocation and re-enrollment.

Hardware-backed protection may be used when supported by the device. The application must not falsely claim hardware-backed security when the device does not provide it.

## 4. Device registration

A device registration record should include:

- Device identifier.
- Associated user identifier.
- Public-key or WebAuthn credential reference.
- Client platform and application type.
- Registration timestamp.
- Last verified timestamp.
- Device status.
- Approval status.
- Revocation timestamp, if applicable.
- Relevant authenticator or credential metadata.

Do not store device private keys on the backend.

Do not treat IP address, user-agent string or browser fingerprint as sufficient device proof.

## 5. Device enrollment workflow

The proposed enrollment sequence is:

1. User completes the required account authentication or verified invitation flow.
2. PSI checks whether new-device approval is required.
3. The client generates or uses a cryptographic key pair through its supported authenticator.
4. PSI issues a fresh enrollment challenge.
5. The client proves possession of the private key.
6. The backend verifies the challenge response.
7. The backend validates the enrollment context and applicable origin or application identity.
8. PSI registers the public key or credential reference.
9. PSI associates the device with the authenticated principal.
10. Required Owner approval is recorded.
11. The device becomes active.
12. PSI records the enrollment event in the audit system.

Failed verification must not create an active trusted device.

## 6. Device-bound invitation redemption

The approved Option B invitation workflow requires device binding.

The device-binding sequence is:

1. Recipient opens the unique invitation link on the first device.
2. PSI validates invitation status and expiry.
3. OTP is delivered only to the pre-registered destination.
4. Recipient verifies the OTP.
5. The device establishes cryptographic identity.
6. PSI registers or associates the device credential with the redemption.
7. PSI issues a limited device-bound session.
8. The Permission Engine enforces the invitation's resource and action scope.
9. PSI records redemption and device enrollment.

Forwarding the invitation link alone must not authorize another device.

If the invitation is already redeemed, subsequent redemption attempts must be rejected unless the Owner explicitly issues a new invitation.

## 7. Device verification

A protected request requiring device verification must establish:

- The device is registered.
- Its credential is active.
- The challenge is fresh.
- The cryptographic proof is valid.
- The credential belongs to the expected principal.
- The device is not suspended or revoked.
- The session is associated with the verified device where required.

Challenge values must be unpredictable, single-use and time-limited.

## 8. Device status lifecycle

Proposed device states:

| State | Meaning |
|---|---|
| Pending | Registration started but not approved or completed |
| Active | Registration verified and permitted |
| Suspended | Temporarily prevented from use |
| Revoked | Permanently denied under the current registration |
| Expired | Credential or registration no longer valid under policy |

State transitions must be validated by the backend and audited.

A revoked device must not become active merely by replaying an old enrollment request.

## 9. Device revocation

The Owner or an appropriately authorized security administrator may revoke a device.

Revocation must:

1. Mark the device revoked.
2. Reject future device proofs from that credential.
3. Invalidate sessions associated with the device.
4. Prevent associated refresh credentials from being used.
5. Reassess pending jobs initiated by that device.
6. Record the revocation event.
7. Notify the Owner when appropriate.

Revocation prevents future authorized access. It cannot guarantee removal of files already downloaded to the device.

## 10. Lost-device and replacement workflow

When a device is lost, stolen or compromised:

1. The Owner starts a verified recovery process from another trusted authentication context.
2. PSI identifies the affected device.
3. The Owner confirms revocation.
4. PSI revokes the device and associated sessions.
5. Related credentials are invalidated.
6. Security events are reviewed.
7. A replacement device completes a new enrollment process.
8. The replacement device receives a new cryptographic identity.

The replacement process must not copy or recover the old device's private key from the server.

## 11. Device limits and approval

Device limits are policy-controlled.

Trusted recurring users may have explicit device limits. New-device enrollment may require Owner approval.

Temporary Recipients receive the device scope associated with their invitation.

Administrators do not automatically bypass device approval policies.

Any exception must be explicit, authorized and audited.

## 12. Risk signals

PSI may consider the following as supporting risk signals:

- Unusual IP address or network.
- Unexpected location change.
- Browser or application version change.
- Unusual authentication pattern.
- Repeated failed device proofs.
- Unexpected concurrent sessions.

These signals may trigger additional verification, alerts or restrictions.

They must not independently establish device identity or automatically prove malicious activity.

## 13. Security and privacy requirements

- Do not store private device keys in application databases.
- Do not log cryptographic secrets or authentication assertions containing sensitive material.
- Avoid collecting unnecessary device information.
- Protect public-key registration and device metadata from unauthorized changes.
- Validate all enrollment requests server-side.
- Require authorization for device listing, suspension and revocation.
- Record device lifecycle events without recording secrets.

## 14. Implementation status

| Capability | Status |
|---|---|
| Browser WebAuthn/passkey design | Documented |
| Android Keystore design | Documented |
| Public-key registration model | Documented |
| Challenge-response verification | Designed |
| Device approval policy | Designed |
| Device lifecycle | Documented |
| Device revocation | Designed |
| Session invalidation on revocation | Planned |
| Device audit events | Planned |
| Device implementation and tests | Not implemented |

## 15. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`