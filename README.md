# IRCTC Railway Ticketing System

A simple **terminal-based railway ticketing system** built with **Python** and **MySQL** for school projects and viva demonstrations.

This is a **sample demo project** — it uses fictional train data and is **not connected to the real IRCTC website or APIs**.

## Requirements

- **Python 3.8+**
- **MySQL Server** (installed and running)
- **pip** (Python package manager)

On Ubuntu/Debian you may also need:

```bash
sudo apt install python3-venv mysql-server
```

## How to Run Locally

### 1. Clone the project and go to the folder

```bash
cd irctc_ticketing
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up the database config

Copy the example env file and add your MySQL details:

```bash
cp .env.example .env
```

Edit `.env` and set your MySQL username and password:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=railway_db
```

> **Note:** Never commit the `.env` file to GitHub. Only `.env.example` is shared.

### 4. Create the database and tables

```bash
mysql -u root -p < database.sql
```

### 5. Add sample train data

```bash
python seed.py
```

### 6. Run the application

```bash
python main.py
```

## Menu Options

1. View All Trains
2. Search Trains (by source and destination)
3. Book Ticket
4. View Ticket (by PNR)
5. Cancel Ticket
6. Exit

## Project Structure

```
irctc_ticketing/
├── main.py          # Main menu and ticketing logic
├── db_config.py     # Loads DB settings from .env
├── database.sql     # Creates railway_db and tables
├── migrate.sql      # Migration for older setups
├── seed.py          # Inserts sample train data
├── requirements.txt # Python dependencies
├── .env.example     # Example environment variables (safe to push)
├── .env             # Your local DB credentials (do NOT push)
└── README.md        # This file
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `externally-managed-environment` | Use a virtual environment (see step 2) |
| Database connection failed | Check MySQL is running and `.env` credentials are correct |
| No trains found | Run `python seed.py` after creating the database |
| `railway_db` does not exist | Run `mysql -u root -p < database.sql` first |

## License

This project is for educational purposes only.
