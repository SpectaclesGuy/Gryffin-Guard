import psycopg2
from datetime import datetime

def get_db_connection():
    """Establish a database connection."""
    return psycopg2.connect(
        dbname='vehicle_database',
        user='postgres',
        password='$Mtyagi@2002',
        host='localhost',
        port='5432'
    )

def insert_vehicle(vehicle_number, in_time):
    """Insert a new vehicle entry with in_time and return the new entry ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO vehiclelogs (vehicle_number, in_time)
        VALUES (%s, %s) RETURNING id
        """,
        (vehicle_number, in_time)
    )
    conn.commit()
    vehicle_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return vehicle_id

def update_exit_time(entry_id, exit_time):
    """Update the exit time for a specific vehicle entry."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE vehiclelogs
        SET out_time = %s
        WHERE id = %s
        """,
        (exit_time, entry_id)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_active_vehicle_entry(vehicle_number):
    """Fetch an active entry (without out_time) for the given vehicle number."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, in_time
        FROM vehiclelogs
        WHERE vehicle_number = %s AND out_time IS NULL
        """,
        (vehicle_number,)
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result  # Returns (id, in_time) if found, otherwise None
