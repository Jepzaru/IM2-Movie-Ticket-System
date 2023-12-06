from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from database import set_database, fetchone, fetchall
from movie import create_movie, get_all_movies, get_movie_by_id, update_movie, delete_movie
from booking import create_booking, cancel_booking
from users import create_user

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "JeffConson210!"
app.config["MYSQL_DB"] = "movie_ticketing"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_AUTOCOMMIT"] = True

app.config["SECRET_KEY"] = 'your_secret_key'

mysql = MySQL(app)
set_database(mysql)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Convert email to lowercase for case-insensitive comparison
        email = email.lower()

        user = fetchone("SELECT * FROM users WHERE email = %s", (email,))

        if user and user["password"] == password:
            user_obj = User()
            user_obj.id = user["id"]
            login_user(user_obj)
            flash("Logged in successfully", "success")
            return redirect(url_for('movies'))
        else:
            flash("Invalid email or password", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        email = email.lower()

        user_data = {
            "name": name,
            "email": email,
            "password": password
        }

        create_user(user_data)
        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template("create_account.html")


@app.route("/movies", methods=["GET", "POST"])
@login_required
def movies():
    if request.method == "POST":
        data = request.get_json()
        create_movie(data)
        return redirect(url_for('movies'))
    else:
        search_query = request.args.get("search")
        
        if search_query:
    
            result = fetchall("SELECT * FROM movies WHERE title LIKE %s", (f"%{search_query}%",))
        else:
           
            result = get_all_movies()
        
        return render_template("movies.html", movies=result)

@app.route("/movies/<id>", methods=["GET"])
def movie_details(id):
    movie = get_movie_by_id(id)
    return render_template("movie_details.html", movie=movie)

@app.route("/movies/<id>/book", methods=["GET", "POST"])
@login_required
def book_movie(id):
    if request.method == "POST":
        movie_id = id
        booker_name = request.form.get("booker_name")
        num_tickets = request.form.get("num_tickets")

        
        create_booking(movie_id, booker_name, num_tickets)

       
        return redirect(url_for('booking_confirmation', movie_id=movie_id, booker_name=booker_name, num_tickets=num_tickets))
    else:
        movie = get_movie_by_id(id)
        return render_template("movie_details.html", movie=movie)

@app.route("/booking_confirmation/<movie_id>/<booker_name>/<num_tickets>", methods=["GET"])
def booking_confirmation(movie_id, booker_name, num_tickets):
    return render_template("booking_confirmation.html", movie_id=movie_id, booker_name=booker_name, num_tickets=num_tickets)


@app.route("/movies/create", methods=["GET"])
def create_movie_form():
    return render_template("create_movie.html")


@app.route("/movies/update/<id>", methods=["GET", "POST"])
def update_movie_form(id):
    if request.method == "POST":
        data = request.get_json()
        update_movie(id, data)
        return redirect(url_for('movies'))
    else:
        movie = get_movie_by_id(id)
        return render_template("update_movie.html", movie=movie)


@app.route("/movies/delete/<id>", methods=["POST"])
def delete_movie_handler(id):
    delete_movie(id)
    return redirect(url_for('movies'))

@app.route("/view_bookings", methods=["GET"])
@login_required
def view_bookings():
    
    bookings = fetchall("SELECT * FROM view_bookings")
    
    return render_template("view_bookings.html", bookings=bookings)

@app.route("/cancel_booking/<booking_id>", methods=["POST"])
@login_required
def cancel_booking_route(booking_id):
    if cancel_booking(booking_id):
        flash("Booking canceled successfully", "success")
    else:
        flash("Booking not found", "error")

    return redirect(url_for('view_bookings'))

if __name__ == "__main__":
    app.run(debug=True)
