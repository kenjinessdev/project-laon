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
```
# ok ra ni bisag unsa, wla pa nako ni na setup
JWT_SECRET="carrots"

# supabase database prisma ORM url
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
uvicorn main:app --reload
```
then go to the link provided


