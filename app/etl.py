from app.config import validate_config
from app.extractor import fetch_unread_emails
from app.transformer import extract_numbers_from_email
from app.validator import validate_record
from app.generator import generate_output_files_by_client


def run_etl(limit=10):
    validate_config()

    emails = fetch_unread_emails(limit=limit)

    if not emails:
        return {
            "status": "success",
            "message": "No unread emails found.",
            "emails_processed": 0,
            "valid_records": 0,
            "failed_records": [],
            "files_generated": []
        }

    records = []
    failed_records = []

    for email_data in emails:
        extracted_records = extract_numbers_from_email(email_data)

        for record in extracted_records:
            try:
                validate_record(record)
                records.append(record)

            except ValueError as error:
                failed_records.append({
                    "client_name": record.get("client_name"),
                    "number": record.get("whitelist_number"),
                    "error": str(error)
                })

    generated_files = []

    if records:
        output_files = generate_output_files_by_client(records)
        generated_files = [str(file_path) for file_path in output_files]

    return {
        "status": "success",
        "emails_processed": len(emails),
        "valid_records": len(records),
        "failed_records": failed_records,
        "files_generated": generated_files
    }