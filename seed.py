"""
Seed script for the IRCTC Railway Ticketing System.
Populates the trains table with fictional train records.
Run once after creating the database: python seed.py
"""

import mysql.connector
from mysql.connector import Error

from db_config import DB_CONFIG


# At least 15 fictional trains for demonstration
SAMPLE_TRAINS = [
    ("12001", "Kolkata Mail Express", "New Delhi", "Howrah", 1850.00, 200, 200),
    ("12002", "New Delhi Mail Express", "Howrah", "New Delhi", 1850.00, 200, 200),
    ("12101", "Rajdhani Express", "New Delhi", "Mumbai", 2200.00, 150, 150),
    ("12102", "Mumbai Rajdhani", "Mumbai", "New Delhi", 2200.00, 150, 150),
    ("12201", "Garib Rath Express", "Kolkata", "Chennai", 950.00, 300, 300),
    ("12202", "Chennai Garib Rath", "Chennai", "Kolkata", 950.00, 300, 300),
    ("12301", "Shatabdi Express", "Mumbai", "Bengaluru", 1650.00, 120, 120),
    ("12302", "Bengaluru Shatabdi", "Bengaluru", "Mumbai", 1650.00, 120, 120),
    ("12401", "Duronto Express", "New Delhi", "Chennai", 2450.00, 180, 180),
    ("12402", "Chennai Duronto", "Chennai", "New Delhi", 2450.00, 180, 180),
    ("12501", "Intercity Express", "Jaipur", "Ahmedabad", 780.00, 250, 250),
    ("12502", "Ahmedabad Intercity", "Ahmedabad", "Jaipur", 780.00, 250, 250),
    ("12601", "Superfast Express", "Hyderabad", "Pune", 1420.00, 220, 220),
    ("12602", "Pune Superfast", "Pune", "Hyderabad", 1420.00, 220, 220),
    ("12701", "Patna Mail Express", "Lucknow", "Patna", 650.00, 280, 280),
    ("12702", "Lucknow Mail Express", "Patna", "Lucknow", 650.00, 280, 280),
    ("12801", "Jan Shatabdi Express", "Bhopal", "Indore", 420.00, 100, 100),
]


def seed_trains():
    """Insert trains or update names if the train number already exists."""
    connection = None
    cursor = None
    inserted = 0
    updated = 0
    skipped = 0

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO trains (train_no, train_name, source, destination, fare, total_seats, available_seats)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        update_name_query = "UPDATE trains SET train_name = %s WHERE train_no = %s"
        check_query = "SELECT train_name FROM trains WHERE train_no = %s"

        for train in SAMPLE_TRAINS:
            train_no, train_name = train[0], train[1]
            cursor.execute(check_query, (train_no,))
            existing = cursor.fetchone()

            if existing:
                if existing[0] != train_name:
                    cursor.execute(update_name_query, (train_name, train_no))
                    updated += 1
                else:
                    skipped += 1
                continue

            cursor.execute(insert_query, train)
            inserted += 1

        connection.commit()
        print("=" * 50)
        print("       TRAIN SEEDER COMPLETE")
        print("=" * 50)
        print(f"Trains inserted : {inserted}")
        print(f"Trains updated  : {updated}")
        print(f"Trains skipped  : {skipped} (already up to date)")
        print(f"Total in list   : {len(SAMPLE_TRAINS)}")
        print("=" * 50)

    except Error as err:
        print(f"Database error: {err}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    seed_trains()
