"""Generate PROJECT_BRIEF.pdf for school project submission."""

from fpdf import FPDF


def add_section_title(pdf, title):
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def add_body(pdf, text):
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(pdf.epw, 6, text)
    pdf.ln(2)


def add_qa(pdf, question, answer):
    pdf.set_font("Helvetica", "B", 11)
    pdf.multi_cell(pdf.epw, 6, question)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 6, answer)
    pdf.ln(2)


def build_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "IRCTC Railway Ticketing System", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    add_section_title(pdf, "1. Project Brief")
    add_body(
        pdf,
        "This is a terminal-based Railway Ticketing System built as a school project "
        "using Python and MySQL. Users can view trains, search by route, book tickets "
        "(with a unique PNR), view ticket details, and cancel bookings.\n\n"
        "It uses sample/fictional train data and is NOT connected to the real IRCTC website.",
    )

    add_section_title(pdf, "2. Folder Structure")
    pdf.set_font("Courier", "", 10)
    pdf.multi_cell(
        pdf.epw,
        5,
        "irctc_ticketing/\n"
        "|-- main.py          # Menu loop + all ticketing functions\n"
        "|-- db_config.py     # Loads DB settings from .env\n"
        "|-- database.sql     # Creates railway_db and tables\n"
        "|-- seed.py          # Inserts sample train data (seeder)\n"
        "|-- requirements.txt # Python packages\n"
        "|-- .env.example     # Example DB config\n"
        "|-- .env             # Your local DB password (private)",
    )
    pdf.ln(3)

    add_section_title(pdf, "3. Full Application Flow")
    add_body(
        pdf,
        "START -> python main.py\n"
        "  -> main() shows welcome message\n"
        "  -> display_menu() prints options 1 to 6\n"
        "  -> User enters choice in a while True loop\n\n"
        "Option 1 (View Trains):\n"
        "  connect_db() -> view_trains() -> SELECT all from trains -> print list\n\n"
        "Option 2 (Search Trains):\n"
        "  search_trains() -> user enters source & destination\n"
        "  -> SELECT trains WHERE source AND destination match -> print results\n\n"
        "Option 3 (Book Ticket):\n"
        "  book_ticket() -> select train -> get passenger count & details\n"
        "  -> lock train row (FOR UPDATE) -> check seats -> generate_pnr()\n"
        "  -> INSERT into bookings -> UPDATE available_seats -> commit\n\n"
        "Option 4 (View Ticket):\n"
        "  view_ticket() -> user enters PNR -> JOIN bookings + trains -> print details\n\n"
        "Option 5 (Cancel Ticket):\n"
        "  cancel_ticket() -> lock booking -> set status CANCELLED\n"
        "  -> add seats back to train -> commit\n\n"
        "Option 6 (Exit): break loop and close program",
    )

    add_section_title(pdf, "4. Setup Flow (Before Running main.py)")
    add_body(
        pdf,
        "Step 1: mysql < database.sql  -> creates railway_db, trains & bookings tables\n"
        "Step 2: python seed.py        -> seed_trains() inserts 17 sample trains\n"
        "Step 3: python main.py        -> starts the menu application",
    )

    add_section_title(pdf, "5. Questions & Answers - Program Flow & Methods")

    qa = [
        (
            "Q1. What does main() do?",
            "A: main() is the entry point. It runs an infinite loop that shows the menu "
            "using display_menu(), reads the user's choice, and calls the matching function "
            "(view_trains, search_trains, book_ticket, view_ticket, cancel_ticket). "
            "It stops when the user picks option 6 (Exit).",
        ),
        (
            "Q2. What does connect_db() do?",
            "A: connect_db() reads DB settings from db_config.py (loaded from .env file) "
            "and opens a MySQL connection using mysql.connector.connect(). "
            "If connection fails, it prints an error and returns None.",
        ),
        (
            "Q3. What does view_trains() do?",
            "A: It connects to the database, runs SELECT on the trains table to fetch "
            "train number, name, source, destination, fare, and available seats. "
            "It prints them in a formatted table using print_train_header() and print_train_row().",
        ),
        (
            "Q4. What does search_trains() do?",
            "A: It asks the user for source and destination stations. Then it runs a "
            "parameterized SQL query with LOWER() so search is case-insensitive. "
            "Only trains matching both stations are shown.",
        ),
        (
            "Q5. What does seed.py (seeder) do?",
            "A: seed.py contains a list of 17 fictional sample trains in SAMPLE_TRAINS. "
            "The seed_trains() function loops through each train and checks if the train "
            "number already exists in the database. If new, it INSERTs the train. "
            "If it exists with a different name, it UPDATEs the name. "
            "If already present and same, it skips. This way seed.py can be run multiple "
            "times safely without duplicating trains.",
        ),
        (
            "Q6. How does book_ticket() work step by step?",
            "A: Step 1 - connect_db() and open cursor.\n"
            "Step 2 - select_train_for_booking() lets user pick train by number OR by route.\n"
            "Step 3 - get_passenger_count() asks for 1 to 4 passengers.\n"
            "Step 4 - get_passenger_details() collects name and age for each passenger.\n"
            "Step 5 - SELECT train FOR UPDATE locks the row and re-checks available seats.\n"
            "Step 6 - generate_pnr() creates a unique booking ID.\n"
            "Step 7 - INSERT one row per passenger into bookings with status CONFIRMED.\n"
            "Step 8 - UPDATE trains SET available_seats = available_seats - count.\n"
            "Step 9 - connection.commit() saves everything. If any step fails, rollback() "
            "undoes the changes.",
        ),
        (
            "Q7. How is PNR generated?",
            "A: generate_pnr() creates the PNR in two parts:\n"
            "  - date_part = today's date in YYMMDD format (e.g. 261026)\n"
            "  - random_part = 6 random digits\n"
            "  Final PNR looks like: PNR261026483921\n"
            "After generating, the code checks the database to make sure this PNR does not "
            "already exist. If it exists, it generates a new one (up to 5 tries).",
        ),
        (
            "Q8. What does select_train_for_booking() do?",
            "A: It gives two options: (1) enter train number directly using "
            "fetch_train_by_number(), or (2) enter source and destination using "
            "fetch_trains_by_route(). If multiple trains match the route, it shows the "
            "list and asks the user to pick one train number from that list.",
        ),
        (
            "Q9. What does view_ticket() do?",
            "A: User enters a PNR. The function runs a JOIN query between bookings and "
            "trains tables to get train details and all passengers on that PNR. "
            "It shows PNR, status, train info, route, fare per person, total fare, "
            "and a list of all passenger names and ages.",
        ),
        (
            "Q10. What does cancel_ticket() do?",
            "A: User enters PNR. The function locks the booking rows with FOR UPDATE. "
            "If PNR not found -> error. If already CANCELLED -> error.\n"
            "Otherwise it: (1) UPDATE bookings SET status = 'CANCELLED' for that PNR, "
            "(2) UPDATE trains SET available_seats = available_seats + passenger_count, "
            "(3) commit(). All passengers on the same PNR are cancelled together and "
            "seats are restored.",
        ),
        (
            "Q11. Why do we use FOR UPDATE and commit/rollback?",
            "A: FOR UPDATE locks the database row during booking/cancellation so two "
            "users cannot book the last seat at the same time. commit() saves changes "
            "permanently. rollback() cancels all changes if something goes wrong, "
            "keeping seat counts correct.",
        ),
        (
            "Q12. Why do we use parameterized queries (%s)?",
            "A: User input (station names, PNR, train number) is passed as parameters "
            "instead of being pasted into the SQL string. This prevents SQL injection "
            "attacks where someone could run harmful SQL through input fields.",
        ),
        (
            "Q13. What is stored in the trains table?",
            "A: train_no (PK), train_name, source, destination, fare, total_seats, "
            "and available_seats. When a ticket is booked, available_seats decreases. "
            "When cancelled, it increases back.",
        ),
        (
            "Q14. What is stored in the bookings table?",
            "A: booking_id (auto increment PK), pnr (same for all passengers on one ticket), "
            "train_no (FK to trains), passenger_name, passenger_age, and status "
            "(CONFIRMED or CANCELLED). One PNR can have up to 4 rows (one per passenger).",
        ),
        (
            "Q15. Is this connected to real IRCTC?",
            "A: No. This is a demo school project with fictional trains and a local MySQL "
            "database. It does not use any IRCTC website or API.",
        ),
    ]

    for question, answer in qa:
        if pdf.get_y() > 250:
            pdf.add_page()
        add_qa(pdf, question, answer)

    pdf.output("PROJECT_BRIEF.pdf")
    print("Created PROJECT_BRIEF.pdf")


if __name__ == "__main__":
    build_pdf()
