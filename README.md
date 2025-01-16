## What is it

This is a web app for storing and viewing todo-list items in a database. Its purpose is to pass the university course "Tietokannat ja web-ohjelmointi" as quickly as possible.

## Features

- Multiple users
- Create/delete todo-list items
- Search items by keywords
- Mark items as "in progress" or "done"

## How to run

Create venv:

```bash
python3 -m venv venv
```

Activate venv:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create database:

```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

Run the app:

```bash
TODOAPP_SECRET_KEY="your secret here" flask run
```