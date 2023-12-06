# movie.py
from database import fetchall, fetchone, execute

def create_movie(data):
    title = data.get("title")
    genre = data.get("genre")
    release_date = data.get("release_date")
    capacity = data.get("capacity")

    query = "INSERT INTO movies (title, genre, release_date, capacity) VALUES (%s, %s, %s, %s)"
    values = (title, genre, release_date, capacity)
    fetchone(query, values)

def get_movie_by_id_with_capacity(movie_id):
    return fetchone("""
        SELECT *, capacity - COALESCE(SUM(num_tickets), 0) AS available_capacity
        FROM movies
        LEFT JOIN bookings ON movies.id = bookings.movie_id
        WHERE movies.id = %s
        GROUP BY movies.id
    """, (movie_id,))

def get_all_movies():
    return fetchall("SELECT * FROM movies")

def get_movie_by_id(movie_id):
    return fetchone("SELECT * FROM movies WHERE id = %s", (movie_id,))

def update_movie(movie_id, data):
    print(f"Updating movie with ID: {movie_id}")
    print(f"Data received: {data}")
    execute("UPDATE movies SET title=%s, genre=%s, release_date=%s, capacity=%s WHERE id=%s",
            (data["title"], data["genre"], data["release_date"], data["capacity"], movie_id))

def delete_movie(movie_id):
    execute("DELETE FROM movies WHERE id=%s", (movie_id,))

