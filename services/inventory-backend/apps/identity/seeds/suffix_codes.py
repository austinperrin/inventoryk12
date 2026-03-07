from collections.abc import Sequence

CodeSeedRow = dict[str, object]


SUFFIX_CODE_SEEDS: Sequence[CodeSeedRow] = (
    {"code": "jr", "label": "Jr.", "sort_order": 10},
    {"code": "sr", "label": "Sr.", "sort_order": 20},
    {"code": "ii", "label": "II", "sort_order": 30},
    {"code": "iii", "label": "III", "sort_order": 40},
    {"code": "iv", "label": "IV", "sort_order": 50},
    {"code": "phd", "label": "Ph.D.", "sort_order": 60},
    {"code": "md", "label": "M.D.", "sort_order": 70},
)
