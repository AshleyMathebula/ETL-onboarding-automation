import re


def extract_client_name(body):
    match = re.search(
        r"Client Name:\s*(.*?)(?=\s+MSISDN:|\s+Package:|\n|$)",
        body,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return "unknown_client"


def extract_numbers_from_email(email_data):
    body = email_data["body"]
    client_name = extract_client_name(body)

    numbers = re.findall(r"\b\d{5,}\b", body)

    records = []
    seen = set()

    for number in numbers:
        formatted_number = normalize_number(number)

        if formatted_number and formatted_number not in seen:
            seen.add(formatted_number)

            records.append({
                "client_name": client_name,
                "original_number": number,
                "whitelist_number": formatted_number
            })

    return records


def normalize_number(number):
    number = number.strip()

    if len(number) == 5:
        return number

    if len(number) == 10 and number.startswith("0"):
        return "27" + number[1:]

    if len(number) == 11 and number.startswith("27"):
        return number

    if len(number) == 9:
        return "27" + number

    return None