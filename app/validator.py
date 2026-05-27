def validate_record(record):
    number = record.get("whitelist_number")

    if not number:
        raise ValueError("Whitelist number is missing")

    if not number.isdigit():
        raise ValueError("Whitelist number must contain digits only")

    if len(number) == 5:
        return True

    if len(number) == 11 and number.startswith("27"):
        return True

    raise ValueError(f"Invalid whitelist number format: {number}")