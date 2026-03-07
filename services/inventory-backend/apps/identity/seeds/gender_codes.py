from collections.abc import Sequence

CodeSeedRow = dict[str, object]


GENDER_CODE_SEEDS: Sequence[CodeSeedRow] = (
    {"code": "male", "label": "Male", "sort_order": 10},
    {"code": "female", "label": "Female", "sort_order": 20},
    {"code": "nonbinary", "label": "Nonbinary", "sort_order": 30},
    {"code": "other", "label": "Other", "sort_order": 40},
    {"code": "unknown", "label": "Unknown", "sort_order": 50},
    {"code": "unspecified", "label": "Unspecified", "sort_order": 60},
)
