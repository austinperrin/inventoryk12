from collections.abc import Sequence

CodeSeedRow = dict[str, object]


RACE_CODE_SEEDS: Sequence[CodeSeedRow] = (
    {
        "code": "american_indian",
        "label": "American Indian or Alaska Native",
        "sort_order": 10,
    },
    {"code": "asian", "label": "Asian", "sort_order": 20},
    {"code": "black", "label": "Black or African American", "sort_order": 30},
    {
        "code": "pacific_islander",
        "label": "Native Hawaiian or Other Pacific Islander",
        "sort_order": 40,
    },
    {"code": "white", "label": "White", "sort_order": 50},
    {"code": "two_or_more", "label": "Two or More Races", "sort_order": 60},
    {"code": "unknown", "label": "Unknown", "sort_order": 70},
)
