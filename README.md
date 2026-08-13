# E-Commerce API

A production-ready e-commerce backend API built with Django REST Framework.

## Features

- **User Authentication** — Phone-based registration with OTP verification, JWT tokens
- **Product Catalog** — Full-text search (PostgreSQL), filtering by specs, price, brand
- **Shopping Cart** — Guest cart with session support, merge on login
- **Reviews** — Rating and comments with purchase verification
- **Order Checkout** — Stock deduction, price snapshot, cart clearing
- **AI Assistant** — Natural language product search and FAQ answering (Farsi)

## Tech Stack

- Python 3.12 / Django 6.0 / Django REST Framework
- PostgreSQL with full-text search
- JWT Authentication (Simple JWT)
- S3-compatible cloud storage
- Hugging Face / OpenAI API for AI chat
- Redis for sessions

## Installation

git clone https://github.com/suleimanparizadi/E-commerce.git
cd E-commerce
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


Create a .env file in the project root:

SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=your_bucket
AWS_S3_ENDPOINT_URL=your_endpoint
GAPGPT_API_TOKEN=your_ai_token
