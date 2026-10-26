"""
IRCTC Railway Ticketing System - Terminal-based menu application.
School project demo: view trains, search, book, view, and cancel tickets.
"""

import random
import string
from datetime import datetime

import mysql.connector
from mysql.connector import Error

from db_config import DB_CONFIG

MAX_PASSENGERS = 4


def connect_db():
    """Connect to MySQL using settings from the .env file."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as err:
        print(f"\nDatabase connection failed: {err}")
        print("Please check MySQL is running and your .env file has correct credentials.\n")
        return None


def display_menu():
    """Print the main menu options."""
    print("\n" + "=" * 40)
    print("       IRCTC RAILWAY TICKETING SYSTEM")
    print("=" * 40)
    print("1. View All Trains")
    print("2. Search Trains")
    print("3. Book Ticket")
    print("4. View Ticket")
    print("5. Cancel Ticket")
    print("6. Exit")
    print("=" * 40)


def print_train_row(train):
    """Format and print one train record."""
    train_no, train_name, source, destination, fare, available_seats = train
    print(
        f"{train_no:<10} {train_name:<28} {source:<15} {destination:<15} "
        f"Rs.{fare:<8.2f} {available_seats}"
    )


def print_train_header():
    """Print column headings for train listings."""
    print(
        f"{'Train No':<10} {'Train Name':<28} {'Source':<15} {'Destination':<15} "
        f"{'Fare':<12} {'Seats'}"
    )
    print("-" * 95)


def view_trains():
    """Display all trains with details and available seats."""
    connection = connect_db()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        query = """
            SELECT train_no, train_name, source, destination, fare, available_seats
            FROM trains
            ORDER BY train_no
        """
        cursor.execute(query)
        trains = cursor.fetchall()

        if not trains:
            print("\nNo trains found. Run seed.py to add trains.\n")
            return

        print("\n--- All Trains ---")
        print_train_header()
        for train in trains:
            print_train_row(train)
        print(f"\nTotal trains: {len(trains)}\n")

    except Error as err:
        print(f"\nError fetching trains: {err}\n")
    finally:
        cursor.close()
        connection.close()


def search_trains():
    """Search trains by source and destination stations."""
    source = input("Enter source station: ").strip()
    destination = input("Enter destination station: ").strip()

    if not source or not destination:
        print("\nSource and destination cannot be empty.\n")
        return

    connection = connect_db()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        query = """
            SELECT train_no, train_name, source, destination, fare, available_seats
            FROM trains
            WHERE LOWER(source) = LOWER(%s) AND LOWER(destination) = LOWER(%s)
            ORDER BY train_no
        """
        cursor.execute(query, (source, destination))
        trains = cursor.fetchall()

        if not trains:
            print(f"\nNo trains found from '{source}' to '{destination}'.\n")
            return

        print(f"\n--- Trains from {source} to {destination} ---")
        print_train_header()
        for train in trains:
            print_train_row(train)
        print(f"\nFound {len(trains)} train(s).\n")

    except Error as err:
        print(f"\nError searching trains: {err}\n")
    finally:
        cursor.close()
        connection.close()


def generate_pnr():
    """Generate a unique PNR/booking ID."""
    date_part = datetime.now().strftime("%y%m%d")
    random_part = "".join(random.choices(string.digits, k=6))
    return f"PNR{date_part}{random_part}"


def fetch_train_by_number(cursor, train_no):
    """Return train details by train number, or None if not found."""
    cursor.execute(
        """
        SELECT train_no, train_name, source, destination, fare, available_seats
        FROM trains
        WHERE train_no = %s
        """,
        (train_no,),
    )
    return cursor.fetchone()


def fetch_trains_by_route(cursor, source, destination):
    """Return all trains matching source and destination."""
    cursor.execute(
        """
        SELECT train_no, train_name, source, destination, fare, available_seats
        FROM trains
        WHERE LOWER(source) = LOWER(%s) AND LOWER(destination) = LOWER(%s)
        ORDER BY train_no
        """,
        (source, destination),
    )
    return cursor.fetchall()


def select_train_for_booking(cursor):
    """
    Let the user pick a train by number or by source/destination.
    Returns train row or None if invalid / not found.
    """
    print("\nHow do you want to select the train?")
    print("1. Enter train number")
    print("2. Enter source and destination")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        train_no = input("Enter train number: ").strip()
        if not train_no:
            print("\nError: Train number cannot be empty.\n")
            return None

        train = fetch_train_by_number(cursor, train_no)
        if not train:
            print(f"\nError: Train '{train_no}' not found.\n")
            return None
        return train

    if choice == "2":
        source = input("Enter source station: ").strip()
        destination = input("Enter destination station: ").strip()

        if not source or not destination:
            print("\nError: Source and destination cannot be empty.\n")
            return None

        trains = fetch_trains_by_route(cursor, source, destination)
        if not trains:
            print(f"\nError: No trains found from '{source}' to '{destination}'.\n")
            return None

        if len(trains) == 1:
            return trains[0]

        print(f"\n--- Trains from {source} to {destination} ---")
        print_train_header()
        for train in trains:
            print_train_row(train)

        valid_numbers = {train[0] for train in trains}
        train_no = input("\nEnter train number from the list above: ").strip()
        if train_no not in valid_numbers:
            print(f"\nError: Train '{train_no}' is not available on this route.\n")
            return None

        for train in trains:
            if train[0] == train_no:
                return train

        print(f"\nError: Train '{train_no}' not found.\n")
        return None

    print("\nError: Invalid choice. Please enter 1 or 2.\n")
    return None


def get_passenger_count():
    """Ask for number of passengers (1 to MAX_PASSENGERS)."""
    count_input = input(f"Enter number of passengers (1-{MAX_PASSENGERS}): ").strip()
    try:
        count = int(count_input)
    except ValueError:
        print("\nError: Please enter a valid number.\n")
        return None

    if count < 1 or count > MAX_PASSENGERS:
        print(f"\nError: Number of passengers must be between 1 and {MAX_PASSENGERS}.\n")
        return None

    return count


def get_passenger_details(count):
    """Collect name and age for each passenger."""
    passengers = []
    for i in range(1, count + 1):
        print(f"\nPassenger {i}:")
        name = input("  Name: ").strip()
        age_input = input("  Age: ").strip()

        if not name:
            print("\nError: Passenger name cannot be empty.\n")
            return None

        try:
            age = int(age_input)
            if age <= 0 or age > 120:
                print("\nError: Age must be between 1 and 120.\n")
                return None
        except ValueError:
            print("\nError: Please enter a valid age.\n")
            return None

        passengers.append((name, age))

    return passengers


def book_ticket():
    """Book tickets for up to 4 passengers on one train."""
    connection = connect_db()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        train = select_train_for_booking(cursor)
        if not train:
            return

        train_no, train_name, source, destination, fare, available_seats = train

        passenger_count = get_passenger_count()
        if not passenger_count:
            return

        passengers = get_passenger_details(passenger_count)
        if not passengers:
            return

        # End read-only queries; booking writes run in a fresh transaction
        connection.rollback()

        # Re-check seats with row lock before booking
        cursor.execute(
            """
            SELECT train_name, source, destination, fare, available_seats
            FROM trains
            WHERE train_no = %s
            FOR UPDATE
            """,
            (train_no,),
        )
        locked_train = cursor.fetchone()

        if not locked_train:
            connection.rollback()
            print(f"\nError: Train '{train_no}' not found.\n")
            return

        train_name, source, destination, fare, available_seats = locked_train

        if available_seats < passenger_count:
            connection.rollback()
            print(
                f"\nError: Only {available_seats} seat(s) available on train {train_no}, "
                f"but you requested {passenger_count}.\n"
            )
            return

        pnr = generate_pnr()
        for _ in range(5):
            cursor.execute("SELECT 1 FROM bookings WHERE pnr = %s LIMIT 1", (pnr,))
            if not cursor.fetchone():
                break
            pnr = generate_pnr()
        else:
            connection.rollback()
            print("\nError: Could not generate a unique PNR. Please try again.\n")
            return

        insert_query = """
            INSERT INTO bookings (pnr, train_no, passenger_name, passenger_age, status)
            VALUES (%s, %s, %s, %s, 'CONFIRMED')
        """
        for name, age in passengers:
            cursor.execute(insert_query, (pnr, train_no, name, age))

        cursor.execute(
            """
            UPDATE trains
            SET available_seats = available_seats - %s
            WHERE train_no = %s
            """,
            (passenger_count, train_no),
        )

        connection.commit()

        total_fare = fare * passenger_count
        print("\n" + "=" * 40)
        print("       TICKET BOOKED SUCCESSFULLY")
        print("=" * 40)
        print(f"PNR            : {pnr}")
        print(f"Status         : CONFIRMED")
        print(f"Train No       : {train_no}")
        print(f"Train Name     : {train_name}")
        print(f"Route          : {source} -> {destination}")
        print(f"Passengers     : {passenger_count}")
        print(f"Fare per person: Rs.{fare:.2f}")
        print(f"Total Fare     : Rs.{total_fare:.2f}")
        print("-" * 40)
        for index, (name, age) in enumerate(passengers, start=1):
            print(f"  {index}. {name} (Age: {age})")
        print("=" * 40 + "\n")

    except Error as err:
        connection.rollback()
        print(f"\nBooking failed: {err}\n")
    finally:
        cursor.close()
        connection.close()


def view_ticket():
    """Display booking details for a given PNR (all passengers)."""
    pnr = input("Enter PNR: ").strip().upper()

    if not pnr:
        print("\nPNR cannot be empty.\n")
        return

    connection = connect_db()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        query = """
            SELECT b.pnr, b.status, b.passenger_name, b.passenger_age,
                   t.train_no, t.train_name, t.source, t.destination, t.fare
            FROM bookings b
            JOIN trains t ON b.train_no = t.train_no
            WHERE b.pnr = %s
            ORDER BY b.booking_id
        """
        cursor.execute(query, (pnr,))
        rows = cursor.fetchall()

        if not rows:
            print(f"\nError: No ticket found for PNR '{pnr}'.\n")
            return

        first = rows[0]
        pnr_val, status, _, _, train_no, train_name, source, destination, fare = first
        passenger_count = len(rows)
        total_fare = fare * passenger_count

        print("\n" + "=" * 40)
        print("       TICKET DETAILS")
        print("=" * 40)
        print(f"PNR            : {pnr_val}")
        print(f"Status         : {status}")
        print(f"Train No       : {train_no}")
        print(f"Train Name     : {train_name}")
        print(f"Route          : {source} -> {destination}")
        print(f"Passengers     : {passenger_count}")
        print(f"Fare per person: Rs.{fare:.2f}")
        print(f"Total Fare     : Rs.{total_fare:.2f}")
        print("-" * 40)
        for index, row in enumerate(rows, start=1):
            _, _, passenger_name, passenger_age, *_ = row
            print(f"  {index}. {passenger_name} (Age: {passenger_age})")
        print("=" * 40 + "\n")

    except Error as err:
        print(f"\nError fetching ticket: {err}\n")
    finally:
        cursor.close()
        connection.close()


def cancel_ticket():
    """Cancel all passengers on a PNR and restore seats."""
    pnr = input("Enter PNR to cancel: ").strip().upper()

    if not pnr:
        print("\nPNR cannot be empty.\n")
        return

    connection = connect_db()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT train_no, status
            FROM bookings
            WHERE pnr = %s
            FOR UPDATE
            """,
            (pnr,),
        )
        rows = cursor.fetchall()

        if not rows:
            connection.rollback()
            print(f"\nError: No booking found for PNR '{pnr}'.\n")
            return

        if rows[0][1] == "CANCELLED":
            connection.rollback()
            print(f"\nError: Ticket {pnr} is already cancelled.\n")
            return

        train_no = rows[0][0]
        passenger_count = len(rows)

        cursor.execute(
            "UPDATE bookings SET status = 'CANCELLED' WHERE pnr = %s",
            (pnr,),
        )

        cursor.execute(
            """
            UPDATE trains
            SET available_seats = available_seats + %s
            WHERE train_no = %s
            """,
            (passenger_count, train_no),
        )

        connection.commit()
        print(f"\nTicket {pnr} has been cancelled successfully.")
        print(f"{passenger_count} seat(s) have been restored to the train.\n")

    except Error as err:
        connection.rollback()
        print(f"\nCancellation failed: {err}\n")
    finally:
        cursor.close()
        connection.close()


def main():
    """Main program loop: show menu until user chooses Exit."""
    print("\nWelcome to IRCTC Railway Ticketing System\n")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_trains()
        elif choice == "2":
            search_trains()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_ticket()
        elif choice == "5":
            cancel_ticket()
        elif choice == "6":
            print("\nThank you for using IRCTC Railway Ticketing System. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.\n")


if __name__ == "__main__":
    main()
