from collections.abc import Sequence

SYSTEM_MANAGED_ROLE_SEEDS: Sequence[str] = (
    # Role order is intentional: system_admin is the top district-scoped role.
    "system_admin",
    "district_admin",
    "site_admin",
    "principal",
    "teacher",
    "counselor",
    "aide",
    "proctor",
    "student",
    "parent",
    "guardian",
    "relative",
)
