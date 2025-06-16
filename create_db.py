import sqlite3
import os

# --- Configuration ---
DB_FILE = "music_library.db"

# --- Main Functions ---

def create_connection(db_file):
    """ Create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to SQLite version: {sqlite3.version}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def execute_sql(conn, sql_statement):
    """ Execute a SQL statement """
    try:
        c = conn.cursor()
        c.execute(sql_statement)
    except sqlite3.Error as e:
        print(f"Error executing SQL: {e}")

def create_tables(conn):
    """ Create the database tables """
    # SQL for creating the Artists table
    create_artists_table = """
    CREATE TABLE IF NOT EXISTS Artists (
        ArtistId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL
    );
    """

    # SQL for creating the Albums table
    create_albums_table = """
    CREATE TABLE IF NOT EXISTS Albums (
        AlbumId INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        ArtistId INTEGER NOT NULL,
        FOREIGN KEY (ArtistId) REFERENCES Artists (ArtistId)
    );
    """

    # SQL for creating the Tracks table
    create_tracks_table = """
    CREATE TABLE IF NOT EXISTS Tracks (
        TrackId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        AlbumId INTEGER NOT NULL,
        Milliseconds INTEGER,
        FOREIGN KEY (AlbumId) REFERENCES Albums (AlbumId)
    );
    """
    
    print("Creating tables...")
    execute_sql(conn, create_artists_table)
    execute_sql(conn, create_albums_table)
    execute_sql(conn, create_tracks_table)
    print("Tables created successfully.")


def insert_dummy_data(conn):
    """ Insert dummy data into the tables """
    cursor = conn.cursor()
    
    print("Inserting data...")

    try:
        # --- Artists ---
        artists = [
            (1, 'Queen'),
            (2, 'Led Zeppelin'),
            (3, 'The Beatles')
        ]
        cursor.executemany("INSERT OR IGNORE INTO Artists (ArtistId, Name) VALUES (?,?);", artists)

        # --- Albums ---
        albums = [
            (1, 'A Night at the Opera', 1),
            (2, 'News of the World', 1),
            (3, 'Led Zeppelin IV', 2),
            (4, 'Abbey Road', 3)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Albums (AlbumId, Title, ArtistId) VALUES (?,?,?);", albums)
        
        # --- Tracks ---
        tracks = [
            # Queen - A Night at the Opera
            (1, 'Bohemian Rhapsody', 1, 354320),
            (2, 'You''re My Best Friend', 1, 170000),
            # Queen - News of the World
            (3, 'We Will Rock You', 2, 122000),
            (4, 'We Are the Champions', 2, 177000),
            # Led Zeppelin - Led Zeppelin IV
            (5, 'Stairway to Heaven', 3, 482000),
            (6, 'Black Dog', 3, 294000),
            # The Beatles - Abbey Road
            (7, 'Come Together', 4, 260000),
            (8, 'Something', 4, 182000),
            (9, 'Here Comes the Sun', 4, 185000)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Tracks (TrackId, Name, AlbumId, Milliseconds) VALUES (?,?,?,?);", tracks)
        
        conn.commit()
        print("Dummy data inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()


def main():
    """ Main function to set up the database """
    # Delete the old DB file if it exists to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed old database file: {DB_FILE}")

    # Create a database connection
    conn = create_connection(DB_FILE)

    if conn is not None:
        # Create tables
        create_tables(conn)
        # Insert data
        insert_dummy_data(conn)
        # Close the connection
        conn.close()
        print("Database setup complete.")
    else:
        print("Error! Cannot create the database connection.")

# --- Run the script ---
if __name__ == '__main__':
    main()
