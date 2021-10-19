import os
import ssl
from bson.objectid import ObjectId
from functools import wraps
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
# needed because the file won't be found after deployment to heroku
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# pass keyword parameter to avoid pymongo error 'SSL: CERTIFICATE_VERIFY_FAILED'
mongo = PyMongo(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)


def login_required(function):
    """Add route protection by restricting access to authenticated users only."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Security alert: Access restricted. Authentication required. Enter credentials.")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    st_series = list(mongo.db.series.find())
    return render_template("index.html", series=st_series)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Add newly created users to the database.

    Return empty strings as values for favourites_series, favourites_books and wishlist
    since they will be added to the database at a later point.
    Set 'is_admin' to false by default for all users.
    """
    st_series = list(mongo.db.series.find())
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("You have entered an invalid username or password")
            return redirect(url_for("register"))

        # create dictionary to be inserted into the database
        user_register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower(),
            "favourites_series": "",
            "favourites_books": "",
            "wishlist": "",
            "is_admin": "False"
        }
        mongo.db.users.insert_one(user_register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash(f'Registration successful! Welcome to ST-Archive, {request.form.get("username").capitalize()}')
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html", series=st_series)


@app.route("/login", methods=["GET", "POST"])
def login():
    """sumary_line"""
    st_series = list(mongo.db.series.find())
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f'Welcome, {request.form.get("username").capitalize()}!')
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html", series=st_series)


@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    """Return user's profile page.

    Fetch only the username from the db and redirect user in session to the profile page.
    Return user not in session to the login page.
    """
    st_series = list(mongo.db.series.find())
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user_reviews = list(mongo.db.reviews.find(
        {"created_by": session["user"].capitalize()}
    ))
    if session["user"]:
        return render_template("profile.html", username=username,
        user_reviews=user_reviews, series=st_series)

    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    st_series = list(mongo.db.series.find())
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/copyrights")
def copyrights():
    """Render page with info about copyrights and licenses."""
    st_series = list(mongo.db.series.find())
    return render_template("copyrights.html", series=st_series)


@app.route("/series/")
def series():
    """Display information about books in the db.

    Show book cover, title, number, info about available bookformats.
    Display blurb.
    Let user mark book as finished, or add it to favourites or user's wish list.
    """
    st_series = list(mongo.db.series.find())
    books = list(mongo.db.books.find())

    return render_template("series.html/", series=st_series, books=books)


@app.route("/add_review/", methods=["GET", "POST"])
@login_required
def add_review():
    """Get user review and add it to the db."""
    if request.method == "POST":
        review = {
            "book_series": request.form.get("book_series"),
            "book_title": request.form.get("book_title"),
            "review_text": request.form.get("review_text"),
            "created_by": session["user"].capitalize()
        }
        mongo.db.reviews.insert_one(review)
        flash("Incoming message from ST-Archive:"
        "Your review has been successfuly transmitted! ST-Archive out.")
        return redirect(url_for("series"))

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    st_series = list(mongo.db.series.find())
    review_book = request.args['title']
    book_series = mongo.db.books.find_one(
        {"title": review_book})["series_code"]

    return render_template("review.html", username=username,
    series=st_series, review_book=review_book, book_series=book_series)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
# decorator unnecessary because functionality only available on profile page?
@login_required
def edit_review(review_id):
    """Update user's own review and update it in the user profile and reviews page."""
    if request.method == "POST":
        updated_review = {
            "book_series": request.form.get("book_series"),
            "book_title": request.form.get("book_title"),
            "review_text": request.form.get("review_text"),
            "created_by": session["user"].capitalize()
        }
        mongo.db.reviews.update_one(
            {"_id": ObjectId(review_id)},
            {"$set":
            {"review_text": updated_review["review_text"]
            }}
            )
        flash("Incoming message from ST-Archive:"
        "Your update to your review has been successfuly transmitted! ST-Archive out.")
        return redirect(url_for("profile", username=session["user"]))

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    st_series = list(mongo.db.series.find())
    return render_template("edit_review.html", series=st_series, username=username, review=review)


@app.route("/delete_review/<review_id>")
# decorator unnecessary because functionality only available on profile page?
@login_required
def delete_review(review_id):
    """Allow user to delete his or her own reviews.

    Show confirmation dialogue before actually deleting the review.
    Give user the ability to cancel the process and return to the profile page.
    """
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash("Message from ST-Archive incoming: Review successfully deleted from memory banks")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/reviews")
def reviews():
    """Render page with all reviews sorted by series and within a series by number."""

    st_series = list(mongo.db.series.find())
    all_reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", series=st_series, all_reviews=all_reviews)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
