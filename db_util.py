
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


def search_by_vehicle_number(vehicle_number):
    """Search for all entries of a specific vehicle number."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, vehicle_number, in_time, out_time
        FROM vehiclelogs
        WHERE vehicle_number = %s
        ORDER BY in_time DESC
        """,
        (vehicle_number,)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    # Format results
    formatted_results = []
    for row in results:
        formatted_results.append({
            "id": row[0],
            "vehicle_number": row[1],
            "in_time": row[2].strftime('%Y-%m-%d %H:%M:%S'),
            "out_time": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None
        })
    return formatted_results

def search_by_timeperiod(start_time, end_time):
    """Search for all vehicles within a specific time period."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, vehicle_number, in_time, out_time
        FROM vehiclelogs
        WHERE (in_time BETWEEN %s AND %s)
        OR (out_time BETWEEN %s AND %s)
        OR (in_time <= %s AND (out_time >= %s OR out_time IS NULL))
        ORDER BY in_time DESC
        """,
        (start_time, end_time, start_time, end_time, start_time, end_time)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    # Format results
    formatted_results = []
    for row in results:
        formatted_results.append({
            "id": row[0],
            "vehicle_number": row[1],
            "in_time": row[2].strftime('%Y-%m-%d %H:%M:%S'),
            "out_time": row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None
        })
    return formatted_results