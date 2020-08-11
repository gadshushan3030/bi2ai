from validator import Required, Length, In, Range, Pattern, validate

rules = {
    "/login": {
        "username": [Required, Length(1)],
        "password": [Required, Range(0, 1000000)]
    }
}


def is_valid_payload(payload, group="/allocate/hls1"):
    if rules.get(group) is not None:
        is_valid = validate(rules.get(group), payload)
        return is_valid
    return True, []
