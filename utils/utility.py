import re


def clean_dict(data: dict[str, str]) -> dict[str, str]:
    """
    Remove None or empty string values from a dictionary and strip whitespace from string values.
    """
    cleaned_data = {}
    for k, v in data.items():
        if v is None or v == "":
            continue
        if isinstance(v, str):
            cleaned_data[k] = v.strip()
        else:
            cleaned_data[k] = v
    return cleaned_data


def is_valid_email(email: str) -> bool:
    """
    Validate if the given string is a valid email address.
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+(?<!\.)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None
