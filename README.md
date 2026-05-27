# Email ETL Onboarding Automation

Python ETL automation tool that reads onboarding emails from Gmail, extracts whitelist numbers, formats them into upload-ready files, and generates one file per client.

## Features

- Gmail inbox integration (IMAP)
- Automatic email extraction
- Short code + long code normalization
- Whitelist formatting
- One output file per client
- FastAPI webhook
- Automatic inbox polling

## Example

Email body:

Client Name: Vodacom SA

78412
0731234567
912345678
27831234567

Generated file:

?,?,78412
?,?,27731234567
?,?,27912345678
?,?,27831234567

## Tech Stack

- Python
- FastAPI
- Gmail IMAP
- python-dotenv
- IMAPClient
- pytest

## Run

Create venv

pip install -r requirements.txt

Start API

uvicorn app.main:app --reload
