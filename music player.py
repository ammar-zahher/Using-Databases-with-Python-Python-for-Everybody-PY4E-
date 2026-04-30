import sqlite3
import os


socket = sqlite3.connect("trac03ks.sqlite")
cur = socket.cursor()

cur.executescript(
    """
    DROP TABLE IF EXISTS Track;
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Genre;

    CREATE TABLE "Artist" (
        "id"    INTEGER,
        "name"  TEXT UNIQUE,
        PRIMARY KEY("id")
    );

    CREATE TABLE "Genre" (
        "id"    INTEGER,
        "name"  TEXT UNIQUE,
        PRIMARY KEY("id")
    );

    CREATE TABLE "Album" (
        "id"    INTEGER,
        "artist_id" INTEGER,
        "title" TEXT UNIQUE,
        PRIMARY KEY("id")
    );

    CREATE TABLE "Track" (
        "id"    INTEGER,
        "album_id"  INTEGER,
        "genre_id"  INTEGER,
        "title" TEXT UNIQUE,
        "len"   INTEGER,
        "rating"    INTEGER,
        "count" INTEGER,
        PRIMARY KEY("id")
    );
    """
)

file = open(r"C:\Users\hesha\Downloads\tracks\tracks\tracks.csv")
for line in file:
    line = line.strip()
    pieces_csv = line.split(",")

    if len(pieces_csv) < 7:
        continue

    name = pieces_csv[0]
    artist = pieces_csv[1]
    album = pieces_csv[2]
    count = pieces_csv[3]
    rating = pieces_csv[4]
    length = pieces_csv[5]
    genre = pieces_csv[6]

    cur.execute("""INSERT OR IGNORE INTO Artist (name) VALUES (?)""", (artist,))
    cur.execute("""SELECT id FROM Artist WHERE name=?""", (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute("""INSERT OR IGNORE INTO Genre (name) VALUES (?)""", (genre,))
    cur.execute("""SELECT id FROM Genre WHERE name=?""", (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute(
        """INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)""",
        (album, artist_id),
    )
    cur.execute("""SELECT id FROM Album WHERE title=?""", (album,))
    album_id = cur.fetchone()[0]

    cur.execute(
        """INSERT OR REPLACE INTO Track 
        (title, album_id, genre_id, len, rating, count) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        (name, album_id, genre_id, length, rating, count),
    )

socket.commit()

print(os.getcwd())
