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
GOOGLE_CLIENT_ID=google-client
GOOGLE_CLIENT_SECRET=secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

JWT_SECRET="mcDRfPao1LsKPTeUDJJO96URrhiTi2BeYIh-8ihjdZU"
SESSION_SECRET="m6aDYVIED0zNcvYLvStiJm6EjBxSRIKUfLZDBY2ArTY"

# replace with actual database link
DATABASE_URL="postgresql://test:test!@localhost:5432/test"
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

