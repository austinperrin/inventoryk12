# ADR 0012: Contacts Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering, Security + Compliance

## Context
Contacts holds person-to-person and person-to-contact endpoint relationships.
It must remain cleanly separated from canonical location ownership.

## Decision
1. Keep reusable contact endpoint type tables in `contacts.EmailCode` and
   `contacts.PhoneCode`.
2. Keep user contact endpoints in `contacts.Email` and `contacts.Phone`.
3. Keep user-address linking in `contacts.UserAddress` while referencing
   canonical address records from `locations.Address`.
4. Keep relationship entities in this domain:
   `contacts.StudentRelationship`,
   `contacts.StudentGuardianRelationship`,
   `contacts.StaffAssignment`.
5. Preserve constraints for primary endpoint flags and valid date windows.
6. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Shared inherited fields for all models in this ADR:
- `id` (internal primary key, `BigAutoField`)
- `uuid` (external identifier, `UUIDField`)
- `created_at`, `updated_at`
- `created_by`, `updated_by`

`EmailCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`Email`:
- `user` (FK), `email_code` (FK)
- `email_address`
- `is_primary`, `is_notification_enabled`
- `sort_order`

`PhoneCode`:
- `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`Phone`:
- `user` (FK), `phone_code` (FK)
- `phone_number`, `extension`
- `is_primary`, `is_sms_capable`, `is_sms_opted_out`, `sms_opted_out_at`
- `sort_order`

`UserAddress`:
- `user` (FK), `address` (FK to `locations.Address`)
- `address_type`, `is_primary`
- `source_system`, `source_record_id`
- `starts_on`, `ends_on`

`StudentRelationship`:
- `student` (FK), `related_student` (FK)
- `relationship_label`
- `starts_on`, `ends_on`

`StudentGuardianRelationship`:
- `student` (FK), `guardian` (FK)
- `relationship_label`, `is_primary_contact`
- `starts_on`, `ends_on`

`StaffAssignment`:
- `staff` (FK)
- `organization` (FK, nullable)
- `facility` (FK, nullable)
- `starts_on`, `ends_on`
- `is_primary`

## Consequences
- Clarifies boundary between contact relationships and canonical addresses.
- Supports future consent and communication policy expansion.
- Increases coordination with identity/locations for joined reads.

## Alternatives Considered
- Move address linkage and relationships into `identity`.
- Keep all contact and address records in one domain table set.

## Follow-Up
- Add API contract ADR for contact endpoint exposure and PII controls.
- Confirm naming and constraint semantics during review gate completion.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0005-contact-and-address-model-v1.md`
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `services/inventory-backend/apps/contacts/models/email.py`
- `services/inventory-backend/apps/contacts/models/phone.py`
- `services/inventory-backend/apps/contacts/models/address.py`
- `services/inventory-backend/apps/contacts/models/relationships.py`
- `services/inventory-backend/apps/contacts/migrations/0001_initial.py`
