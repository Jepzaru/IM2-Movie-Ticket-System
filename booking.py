from database import fetchone, execute

def create_booking(movie_id, booker_name, num_tickets, total_price):
    query = "INSERT INTO bookings (movie_id, booker_name, num_tickets, total_price) VALUES (%s, %s, %s, %s)"
    values = (movie_id, booker_name, num_tickets, total_price)
    
    try:
        fetchone(query, values)
        return True  
    except Exception as e:
        print(f"Error creating booking: {e}")
        return False

def get_booking_info_with_movie_title(booking_id):
    query = """
        SELECT bookings.*, movies.title as movie_title
        FROM bookings
        JOIN movies ON bookings.movie_id = movies.id
        WHERE bookings.booking_id = %s
    """
    values = (booking_id,)
    
    return fetchone(query, values)

def cancel_booking(booking_id):
    booking = get_booking_info_with_movie_title(booking_id)
    
    if booking:
       
        booking_id_column = "booking_id"  

        movie_id = booking["movie_id"]
        num_tickets = booking["num_tickets"]
        execute(f"DELETE FROM bookings WHERE {booking_id_column} = %s", (booking_id,))
        
        execute("UPDATE movies SET capacity = capacity + %s WHERE id = %s", (num_tickets, movie_id))

        return True
    else:
        return False

def calculate_total_price(num_tickets, price):
    try:
        num_tickets = int(num_tickets)
        if price is not None:
            movie_price = float(price)
            total_price = num_tickets * movie_price
            return total_price
        else:
            return None
    except ValueError:
        return None