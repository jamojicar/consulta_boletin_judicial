# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python application that monitors legal bulletins from the Morelos State Judicial System (TSJ Morelos) and sends notifications via Telegram when specific names are found. The application is designed to run as an AWS Lambda function.

## Key Components

- `consulta.py`: Main application logic for web scraping, data processing, and AWS DynamoDB integration
- `mensaje.py`: Telegram notification module containing bot token and messaging functions

## Architecture

The application follows this flow:
1. Queries the judicial bulletin system with date ranges and district parameters
2. Scrapes HTML responses using BeautifulSoup to find specific names
3. Normalizes text using unidecode for case-insensitive matching
4. Stores results in DynamoDB to prevent duplicate notifications (6-day deduplication window)
5. Sends Telegram notifications for new matches

## Development Environment

- Python 3.11 with virtual environment in `venv/`
- To activate virtual environment: `source venv/bin/activate`
- Required dependencies: requests, beautifulsoup4, unidecode, pytz, boto3

## AWS Integration

- Uses DynamoDB table named 'boletin' for record deduplication
- Configured as Lambda function with `lambda_handler` as entry point
- Requires AWS credentials and DynamoDB permissions

## Search Configuration

The application currently monitors two districts (1 and 9) for hardcoded names:
- "Paola Samantha Dominguez Melendez" 
- "Juan Amador Mojica"

Search parameters:
- Date range: Current date minus 26 days to current date
- Target URL: http://sica.tsjmorelos2.gob.mx/boletin/DT/dat_consulta.php
- Mexico City timezone (America/Mexico_City)

## Telegram Integration

- Bot token and chat IDs are hardcoded in `mensaje.py`
- Sends notifications to personal chat ID: -656922368
- Uses Telegram Bot API for message delivery