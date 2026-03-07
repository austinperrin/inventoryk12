from collections.abc import Sequence

CodeSeedRow = dict[str, object]


PREFIX_CODE_SEEDS: Sequence[CodeSeedRow] = (
    {"code": "mr", "label": "Mr.", "sort_order": 10},
    {"code": "mrs", "label": "Mrs.", "sort_order": 20},
    {"code": "ms", "label": "Ms.", "sort_order": 30},
    {"code": "miss", "label": "Miss", "sort_order": 40},
    {"code": "mx", "label": "Mx.", "sort_order": 50},
    {"code": "dr", "label": "Dr.", "sort_order": 60},
)
