# PSI Identity and Access Architecture

**Status:** Phase 2.1 — Design documentation
**Implementation status:** Proposed identity and authorization design; not yet implemented.

## 1. Purpose

This document defines how PSI identifies users, assigns roles, grants resource access and enforces authorization.

The design separates identity, role assignment and resource-specific permissions. Authentication establishes who is making a request; authorization determines what that identity may do.

## 2. Identity categories and roles

PSI distinguishes three principal access categories:

- **Owner:** The primary account owner with ultimate control.
- **Trusted User:** A recurring user with explicitly granted permissions.
- **Temporary Recipient:** A recipient with limited, time-bound access.

PSI also defines five authorization roles:

| Role | Purpose |
|---|---|
| Owner | Full control of the PSI account and security configuration |
| Administrator | Explicitly delegated administrative responsibilities |
| Trusted User | Recurring access within assigned permissions |
| Temporary Recipient | Limited access established through an invitation |
| Viewer | Read-only access within assigned resource boundaries |

Identity category and authorization role are related but not interchangeable. A Trusted User, for example, may receive Viewer-level access to one resource and additional explicitly granted actions on another.

An Administrator does not automatically become the Owner and must not receive Owner-only authority by default.

## 3. Authorization principles

The Permission Engine must enforce:

1. Deny by default.
2. Least privilege.
3. Backend-side authorization.
4. Resource-specific permission checks.
5. Action-level restrictions.
6. Permission expiry and revocation.
7. Separation of administrative and ownership authority.
8. Additional approval for designated sensitive operations.
9. Revalidation of permissions before delayed or background operations.

Frontend visibility and client-supplied role values are never authoritative.

## 4. Role-based access control

RBAC provides the baseline authorization layer.

Proposed role capabilities:

| Capability | Owner | Administrator | Trusted User | Temporary Recipient | Viewer |
|---|---|---|---|---|---|
| Manage Owner account | Yes | No | No | No | No |
| Manage delegated users | Yes | Limited delegation | No | No | No |
| Manage security policies | Yes | Only if delegated | No | No | No |
| Manage devices | Yes | Only if delegated | Own device, subject to policy | Own registered device | No |
| Manage resource permissions | Yes | Only if delegated | Only if explicitly granted | No | No |
| Read assigned resources | Yes | If authorized | If granted | If granted | If granted |
| Modify assigned resources | Yes | If authorized | If granted | If granted | No |
| Create invitations | Yes | Only if delegated | Only if explicitly granted | No | No |
| Revoke Owner account access | Yes | No | No | No | No |

This is a proposed baseline. Resource-level restrictions and explicit policy decisions may further limit any role.

## 5. Resource-specific permissions

RBAC alone is insufficient for PSI because users may have different access to different drives, folders and files.

Every resource grant should identify:

- Principal receiving access.
- Resource identifier.
- Allowed actions.
- Granting identity.
- Creation time.
- Start time, if scheduled.
- Expiry time, if applicable.
- Device restrictions, if applicable.
- Approval requirements.
- Current status.
- Revocation information.

Example permission actions:

| Action | Meaning |
|---|---|
| `read` | View permitted resource information |
| `download` | Download an authorized file |
| `upload` | Add files to an authorized destination |
| `modify` | Modify permitted resource metadata or content |
| `share` | Share a resource when explicitly permitted |
| `manage_permissions` | Manage grants within delegated scope |
| `delete` | Delete a resource when explicitly authorized |

Actions must be evaluated independently. Read permission does not automatically grant download, modification, sharing or deletion.

## 6. Authorization decision model

The Permission Engine should evaluate:

1. Authenticated principal.
2. Active account status.
3. Assigned role.
4. Requested resource.
5. Requested action.
6. Resource ownership and scope.
7. Explicit permission grants.
8. Grant start and expiry.
9. Schedule restrictions.
10. Registered device status.
11. Session validity.
12. Required Owner approval.
13. Relevant security restrictions.

A request is permitted only when all mandatory checks succeed.

Missing, ambiguous, expired or invalid authorization evidence must result in denial.

## 7. One-time invitation workflow — approved Option B

PSI uses a one-time, device-bound invitation process.

### 7.1 Invitation creation

The Owner specifies:

- Intended recipient.
- Resource or application scope.
- Permitted actions.
- Expiry.
- Pre-registered OTP delivery destination.
- Whether OTP delivery is automatic or requires Owner approval.

The destination must be registered or verified through an Owner-controlled process. A visitor must not be able to substitute an arbitrary destination.

### 7.2 Invitation redemption

1. PSI generates a unique, high-entropy invitation token.
2. The invitation is stored in protected form.
3. The recipient opens the invitation on the first device.
4. PSI validates invitation status and expiry.
5. PSI sends an OTP to the pre-registered destination, subject to the Owner's delivery-approval setting.
6. The recipient submits the OTP.
7. PSI validates the OTP and attempt limit.
8. The device establishes cryptographic identity.
9. PSI associates the device with the invitation redemption.
10. PSI creates a limited session.
11. The Permission Engine enforces the invitation's resource and action scope.
12. PSI records redemption and access establishment in the audit system.

### 7.3 Invitation security requirements

- Invitation tokens must be unpredictable.
- Store protected token verifiers rather than reusable plaintext tokens.
- Invitations must expire.
- Redemption must be single-use.
- Attempts must be rate-limited.
- Revoked invitations must be rejected.
- OTP challenges must be single-use.
- OTP delivery must use the approved destination.
- Device identity must be cryptographically verified.
- Forwarding the invitation link alone must not authorize another device.

## 8. OTP policy

Proposed defaults:

| Control | Default |
|---|---|
| OTP validity | 5 minutes |
| Maximum verification attempts | 5 |
| Challenge reuse | Not permitted |
| Destination selection | Owner-controlled |
| Delivery channels | WhatsApp or email |
| Optional fallback | SMS |

Expired, consumed or invalidated challenges must be rejected.

Repeated failures must trigger rate limiting and security monitoring.

The actual delivery provider and cost remain open decisions.

## 9. Access Request Gateway

A visitor may submit an access request for the application or a particular resource.

A request may include:

- Requested resource.
- Reason for access.
- Contact information.
- Device registration information.

The Owner can approve or reject the request.

An approval must specify:

- Authorized principal.
- Resource scope.
- Permitted actions.
- Duration.
- Device restrictions, where required.
- Additional verification requirements.

Approval must not allow a visitor to choose an arbitrary OTP destination.

## 10. Trusted recurring access

Trusted User access is an approved PSI requirement and must remain part of the architecture.

The design supports:

- Persistent or time-limited access.
- Granular resource permissions.
- Scheduled access.
- Action restrictions.
- Device limits.
- Owner approval for new devices where required.
- OTP re-verification where required.
- Suspension and revocation.
- Auditable permission changes.

Trusted User access may be implemented in a later release without removing it from the approved design.

## 11. Permission changes and revocation

Permission changes must be validated by the backend.

Sensitive changes may require Owner approval.

Revocation must:

1. Mark the affected grant inactive.
2. Prevent future authorization under that grant.
3. Revalidate active sessions and pending jobs where relevant.
4. Revoke related invitations if applicable.
5. Record the change in the audit system.

Revocation cannot erase files already downloaded by a recipient.

## 12. Separation of application access and resource access

PSI must distinguish:

- Access to the PSI application.
- Access to a particular storage drive.
- Access to a folder.
- Access to an individual file.
- Permission to perform a particular action.

Having a valid application session does not automatically grant access to every connected drive or file.

## 13. Authorization failure handling

The backend must reject requests when:

- The identity is unknown or disabled.
- The session is invalid or expired.
- The device is revoked or unverified.
- The requested role does not permit the operation.
- No matching resource grant exists.
- A grant has expired or is not yet active.
- Required approval is missing.
- An invitation has already been redeemed.
- OTP verification fails.
- The requested action exceeds the approved scope.

Responses must not disclose sensitive internal policy details.

## 14. Implementation status

| Capability | Status |
|---|---|
| Identity categories and roles | Documented |
| RBAC design | Documented |
| Resource-specific permission model | Documented |
| Invitation workflow | Documented |
| OTP policy | Proposed defaults documented |
| Access Request Gateway | Designed, not implemented |
| Trusted recurring access | Approved requirement, not implemented |
| Permission Engine | Planned |
| Permission audit integration | Planned |

## 15. Related documents

- `docs/security/architecture.md`
- `docs/architecture/security-boundaries.md`
- `docs/security/threat-model.md`
- `docs/security/device-identity.md`
- `docs/security/sessions.md`
- `docs/security/audit-and-detection.md`
- `docs/security/testing-strategy.md`