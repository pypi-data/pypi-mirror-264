from typing import Dict, List


def make_cf_tags(tags: Dict[str, str]) -> List[Dict[str, str]]:
    _tags = []
    for key, value in tags.items():
        _tags.append({"Key": key, "Value": value})
    return _tags
