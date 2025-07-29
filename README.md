# Project Laon

A DOST STARTer Project, tackling the agricultural sector's problem in handling highly perishable goods by providing a platform for farmers to eliminate the need for middlemen.

## How to setup backend

### 1. Clone the repo

```bash
git clone https://github.com/kenjinessdev/project-laon.git
```

### 2. setup python virtual environment

```bash
cd project-laon/
python -m venv .venv
# activate venv
.venv\scripts\activate

```

### 3. install python libraries

```bash
pip install -r .\backend\requirements.txt
```

### 4. create `.env` file in `backend/` directory

```bash
cd ./backend/

```

*create* `.env` *file*

```bash

GOOGLE_CLIENT_ID=google-client-id
GOOGLE_CLIENT_SECRET=google-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

FACEBOOK_CLIENT_ID=facebook-client-id
FACEBOOK_CLIENT_SECRET=wow
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/v1/auth/facebook/callback

JWT_SECRET="mcDRfPao1LsKPTeUDJJO96URrhiTi2BeYIh-8ihjdZU"
SESSION_SECRET="m6aDYVIED0zNcvYLvStiJm6EjBxSRIKUfLZDBY2ArTY"
DATABASE_URL="postgresql://postgres:test@localhost:5432/test"
DIRECT_URL="supabase database direct url"

SUPABASE_URL="supbase base url"
SUPABASE_SERVICE_KEY="supabse service key"

DEBUG=true
```

### 4. run prisma migration

```bash
prisma migrate
prisma generate
```

### 5. run app

```bash
# make sure you are in backend/ directory
uvicorn src.main:app --reload
```
then go to the link provided

## 📘 API Documentation

For full API reference, see the [API Docs](./backend/docs/api-docs.md).

