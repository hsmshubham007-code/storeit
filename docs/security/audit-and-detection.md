# PSI Audit and Threat Detection Architecture

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Proposed audit and detection controls; no audit pipeline or threat detection engine is currently implemented.

## 1. Purpose

This document defines how PSI records security-relevant activity, detects suspicious behavior, supports incident investigation and protects audit integrity.

The audit system must provide accountability without collecting or exposing secrets unnecessarily.

Audit logging and threat detection are separate responsibilities:

- Audit records establish what security-relevant action was attempted or completed.
- Threat detection evaluates events and patterns to identify suspicious activity.
- Incident response uses verified evidence to contain and recover from security events.

## 2. Security principles

1. Security-relevant actions must produce auditable events.
2. Audit records must not contain passwords, tokens, private keys, OTP values or plaintext credentials.
3. Audit access must be restricted and authorized.
4. Audit records must be protected against unauthorized alteration and deletion.
5. Failed and denied security operations must be recorded where appropriate.
6. Detection must distinguish suspicious signals from confirmed compromise.
7. Detection failures must not silently disable essential authorization controls.
8. Audit records must support investigation through timestamps and correlation identifiers.
9. Sensitive information must be minimized and retained only under an approved policy.
10. Security alerts must not reveal secrets or unnecessary personal information.

## 3. Proposed architecture

The proposed design contains four responsibilities.

### 3.1 Event producers

Security-relevant backend components emit structured events.

Examples include:

- Identity and authentication.
- Permission Engine.
- Device Identity.
- Invitation and OTP workflows.
- Session Management.
- Credential Vault.
- Drive Management.
- Transfer Management.
- Sharing Management.
- Recovery operations.

Business modules must emit events through documented interfaces rather than writing directly to audit storage.

### 3.2 Audit service

The audit service validates, normalizes and persists security events.

It must:

- Validate event structure.
- Attach trusted server-side timestamps.
- Assign or preserve correlation identifiers.
- Apply data-minimization rules.
- Reject or redact prohibited secret fields.
- Store records in an access-controlled audit repository.
- Expose authorized query operations.

### 3.3 Threat detection

The detection component evaluates individual events and event patterns.

It may use:

- Threshold-based rules.
- Repeated-failure detection.
- Unusual activity patterns.
- Device and session risk signals.
- Permission-change monitoring.
- Credential and invitation lifecycle events.

Detection results are signals requiring appropriate handling. They are not automatically proof of malicious activity.

### 3.4 Alerting and incident response

Alerts should be delivered to the Owner through an approved notification mechanism.

The Owner or authorized security administrator can review the event, investigate and take an authorized action.

Notification delivery must not expose secrets or sensitive resource contents.

## 4. Audit event structure

A proposed audit event contains:

| Field | Purpose |
|---|---|
| Event ID | Unique event identifier |
| Event type | Normalized event category |
| Timestamp | Trusted server-side event time |
| Actor ID | User or service initiating the action, when known |
| Actor type | Owner, user, system or service |
| Target type | Resource type affected |
| Target ID | Internal target identifier where appropriate |
| Action | Operation attempted or performed |
| Outcome | Success, failure, denied or pending |
| Reason code | Safe, non-secret outcome explanation |
| Source device ID | Verified device reference where available |
| Session ID | Internal session reference where appropriate |
| Correlation ID | Identifier connecting related operations |
| Risk indicators | Relevant non-secret detection signals |

Do not include:

- Passwords or password hashes.
- OTP values or delivery codes.
- Access or refresh tokens.
- Session credentials.
- Private keys.
- Encryption keys.
- Authorization codes.
- Plaintext provider credentials.
- Full sensitive file contents.
- Unnecessary personal data.

IP addresses and other potentially identifying metadata must be collected only when justified by security requirements and handled under an approved retention and privacy policy.

## 5. Event categories

The following event categories should be supported.

### 5.1 Authentication events

- Authentication succeeded.
- Authentication failed.
- Additional verification required.
- Account locked or suspended.
- Authentication method changed.
- Recovery initiated or completed.

### 5.2 Device events

- Device enrollment started.
- Device registration succeeded or failed.
- Device approval granted or rejected.
- Device suspended.
- Device revoked.
- Device verification failed.

### 5.3 Session events

- Session created.
- Session renewed.
- Session expired.
- Session logout.
- Session revoked.
- Session validation failed.

### 5.4 Permission events

- Role assigned or changed.
- Resource permission granted.
- Resource permission changed.
- Resource permission revoked.
- Authorization denied.
- Privileged operation attempted.

### 5.5 Invitation and OTP events

- Invitation created.
- Invitation delivered.
- OTP challenge issued.
- OTP verification succeeded or failed.
- OTP challenge expired.
- Invitation redeemed.
- Invitation revoked.
- Invitation redemption rejected.

OTP values and complete delivery payloads must never be recorded.

### 5.6 Credential events

- Provider authorization completed.
- Credential stored or replaced.
- Credential refresh attempted.
- Credential refresh failed.
- Credential revoked.
- Credential access denied.

Credential values must never be recorded.

### 5.7 Sharing and recovery events

- Sharing permission created or changed.
- Sharing access revoked.
- Recovery operation requested.
- Recovery operation completed or failed.
- Recovery verification failed.

### 5.8 Administrative events

- Security policy changed.
- Account suspended or restored.
- Audit access attempted.
- Security alert reviewed.
- Incident response action performed.

## 6. Threat detection rules

Initial detection rules should include:

| Signal | Detection approach | Possible response |
|---|---|---|
| Repeated OTP failures | Count failures within a defined time window | Rate-limit, temporarily block challenge and alert |
| Repeated login failures | Threshold by account and relevant risk signals | Throttle and require additional verification |
| Unexpected device proof failures | Detect repeated invalid proofs | Reject attempts and alert |
| Forwarded invitation attempts | Detect redemption from an already-used invitation | Reject and record |
| Repeated session validation failures | Detect abnormal invalid-session patterns | Rate-limit and investigate |
| Unexpected permission escalation | Detect sensitive role or permission changes | Require authorization and notify Owner |
| Revoked credential use | Detect attempted use after revocation | Deny and investigate |
| Unusual transfer or sharing activity | Evaluate volume, frequency and policy deviations | Apply configured restrictions and alert |
| Audit access anomalies | Detect unauthorized or unusual audit queries | Deny and alert |
| Repeated recovery failures | Detect suspicious recovery attempts | Rate-limit and require additional verification |

Thresholds and time windows must be configurable and reviewed before implementation.

Detection must avoid treating a single unusual IP address, location or browser fingerprint as proof of compromise.

## 7. Audit integrity and protection

Audit storage must be protected from ordinary business-module write access.

Requirements:

- Use a dedicated audit-service interface.
- Restrict direct database write privileges.
- Separate audit administration from ordinary user administration.
- Protect stored records against unauthorized modification.
- Record attempts to access or change audit records.
- Apply backups and recovery controls.
- Validate audit integrity during investigation.

An append-only logical interface is recommended.

Additional tamper-evidence mechanisms, such as chained event hashes or externally protected integrity checkpoints, may be evaluated during implementation.

A hash chain alone does not guarantee tamper-proof storage if an attacker controls both the records and the verification material.

## 8. Audit access and retention

Audit access must follow least privilege.

Proposed access:

- Owner: review account security events.
- Authorized security administrator: review events within delegated scope.
- Trusted User: no general access to account-wide security audit records.
- Temporary Recipient: no general audit access.
- Viewer: no general audit access.

Audit queries must be scoped and authorized by the backend.

Retention duration, export policy, deletion rules and legal obligations remain open decisions. No fixed retention period is finalized in Phase 2.1.

## 9. Alert handling

A security alert should contain:

- Alert identifier.
- Event or detection rule reference.
- Severity.
- Detection timestamp.
- Affected account or resource reference.
- Safe summary.
- Recommended review action.
- Current status.

Alert states may include:

- New.
- Acknowledged.
- Under investigation.
- Resolved.
- False positive.

Alerts must not contain secrets or unnecessary file content.

The system must not claim that an incident is resolved merely because an alert was acknowledged.

## 10. Incident response workflow

The proposed incident workflow is:

1. Detect a suspicious event or receive a security report.
2. Create an alert with a correlation reference.
3. Validate the available evidence.
4. Determine affected users, devices, sessions, credentials and resources.
5. Contain the incident using authorized controls.
6. Revoke compromised sessions or devices where appropriate.
7. Revoke affected credentials through supported provider mechanisms where possible.
8. Review pending operations and prevent unsafe execution.
9. Restore access only after the relevant security checks succeed.
10. Record actions, outcomes and unresolved risks.
11. Review the incident for required policy or control improvements.

Recovery actions must be verified. The system must not claim that an attacker has lost access unless the relevant credentials and sessions have actually been invalidated.

## 11. Failure handling

The implementation must define behavior when:

- Audit persistence is unavailable.
- An event fails validation.
- A detection rule cannot execute.
- Alert delivery fails.
- Audit integrity verification fails.

Security-critical actions should not silently bypass mandatory audit requirements.

Where audit persistence is unavailable, sensitive operations should generally fail closed or be safely deferred according to an explicitly approved availability policy.

The system must avoid creating unsafe partial operations merely to preserve availability.

## 12. Implementation status

| Capability | Status |
|---|---|
| Audit architecture | Documented |
| Event schema | Proposed |
| Event categories | Documented |
| Secret-redaction requirements | Documented |
| Audit access control | Designed |
| Audit integrity protection | Designed |
| Threat detection rules | Proposed |
| Alert workflow | Designed |
| Incident response workflow | Documented |
| Audit persistence | Not implemented |
| Automated detection engine | Not implemented |
| Security alert delivery | Not implemented |

## 13. Open decisions

Before implementation, decide:

- Audit database and storage strategy.
- Retention and deletion policy.
- Privacy and legal requirements.
- Event volume and performance targets.
- Detection thresholds and time windows.
- Alert delivery channel.
- Tamper-evidence and external integrity strategy.
- Incident response responsibilities.
- Audit export and backup policy.

These decisions must not be treated as finalized without review.

## 14. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/threat-model.md`
- `docs/security/identity-and-access.md`
- `docs/security/device-identity.md`
- `docs/security/credential-vault.md`
- `docs/security/sessions.md`
- `docs/security/testing-strategy.md`