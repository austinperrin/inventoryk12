from collections.abc import Sequence

CodeSeedRow = dict[str, object]


ETHNICITY_CODE_SEEDS: Sequence[CodeSeedRow] = (
    {"code": "hispanic_latino", "label": "Hispanic or Latino", "sort_order": 10},
    {
        "code": "not_hispanic_latino",
        "label": "Not Hispanic or Latino",
        "sort_order": 20,
    },
    {"code": "unknown", "label": "Unknown", "sort_order": 30},
    {"code": "unspecified", "label": "Unspecified", "sort_order": 40},
)
