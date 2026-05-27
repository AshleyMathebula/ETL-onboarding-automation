from imapclient import IMAPClient
import email
from email.header import decode_header

from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, MAILBOX


def decode_text(value):
    if not value:
        return ""

    decoded_parts = decode_header(value)
    text = ""

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            text += part.decode(encoding or "utf-8", errors="ignore")
        else:
            text += part

    return text


def get_email_body(message):
    body = ""

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode(errors="ignore")
    else:
        payload = message.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore")

    return body.strip()


def fetch_unread_emails(limit=5):
    emails = []

    with IMAPClient(EMAIL_HOST, port=EMAIL_PORT, ssl=True) as client:
        client.login(EMAIL_USER, EMAIL_PASSWORD)
        client.select_folder(MAILBOX)

        message_ids = client.search(["UNSEEN"])
        message_ids = message_ids[:limit]

        for message_id in message_ids:
            raw_message = client.fetch([message_id], ["RFC822"])[message_id][b"RFC822"]
            parsed_message = email.message_from_bytes(raw_message)

            email_data = {
                "id": message_id,
                "from": decode_text(parsed_message.get("From")),
                "subject": decode_text(parsed_message.get("Subject")),
                "body": get_email_body(parsed_message),
            }

            emails.append(email_data)

    return emails