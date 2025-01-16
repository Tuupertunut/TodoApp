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