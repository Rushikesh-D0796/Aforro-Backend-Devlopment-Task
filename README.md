🏗 Aforro Backend Assignment

A modular Django backend implementing a store–inventory–order system with search, caching, async processing, and containerized setup.

This project focuses on:

Transaction-safe order processing

Query optimization

Search APIs

Redis caching

Celery async tasks

Scalable structure

🚀 Tech Stack

Django + DRF

PostgreSQL

Redis (cache + broker)

Celery

Docker

📂 Project Structure
apps/
  products/
  stores/
  orders/
  search/
tests/
project/
docker-compose.yml

⚙️ Setup (Local)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

DB

Create PostgreSQL DB:

CREATE DATABASE aforro;
CREATE USER aforro_user WITH PASSWORD 'aforro_pass';
GRANT ALL PRIVILEGES ON DATABASE aforro TO aforro_user;


Run:

python manage.py migrate
python manage.py runserver

🔴 Redis

Start Redis:

redis-server

🧵 Celery Worker
celery -A project worker --loglevel=info --pool=solo

🌱 Seed Data
python manage.py seed_data


Generates:

10+ categories

1000+ products

20+ stores

Inventory data

📡 API Endpoints
Feature	Endpoint
Create Order	POST /api/orders/
List Store Orders	GET /api/stores/{id}/orders/
Inventory List	GET /api/stores/{id}/inventory/
Product Search	GET /api/search/products/
Autocomplete	GET /api/search/suggest/?q=
⚡ Caching

Inventory API responses are cached using Redis for 5 minutes.

🧵 Async Task

Celery processes background tasks such as order confirmation handling.

🧪 Tests

Run:

python manage.py test


Covers:

Order stock validation

Order rejection

Inventory API

Search API

🐳 Docker
docker-compose up --build


Services started:

API

PostgreSQL

Redis

Celery worker

🧠 Scalability Notes

Uses DB transactions + row locks for stock consistency

Query optimization via select_related, annotate

Redis caching for read-heavy endpoints

Async tasks separated via Celery
