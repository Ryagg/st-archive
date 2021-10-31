import os
import ssl
from functools import wraps
from bson.objectid import ObjectId
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import re
# needed because the file won't be found after deployment to heroku
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# pass keyword param to avoid pymongo error 'SSL: CERTIFICATE_VERIFY_FAILED'
mongo = PyMongo(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)


def login_required(function):
    """Add route protection by restricting access
        to authenticated users only."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Security alert: Access restricted. Authentication required."
                  "Enter credentials.")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    st_series = list(mongo.db.series.find())
    return render_template("index.html", series=st_series)


@app.route("/search", methods=["GET", "POST"])
def search():
    st_series = list(mongo.db.series.find())
    books = list(mongo.db.books.find())
    query = request.form.get("query")
    result = list(mongo.db.books.find({"$text": {"$search": query}}))

    return render_template("series.html", series=st_series, books=books,
                            result=result)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Add newly created users to the database.

    Return empty arrays as values for favourites_series, favourites_books,
    finished books, and wishlist since they will be added to the database
    at a later point.
    Set 'is_admin' to false by default for all users.
    """
    st_series = list(mongo.db.series.find())
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Security alert: incorrect Username and/or Password."
                  "Access denied.")
            return redirect(url_for("register"))

        # create dictionary to be inserted into the database
        user_register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower(),
            "favourites_series": [],
            "favourites_books": [],
            "wishlist": [],
            "finished_books": [],
            "is_admin": "False"
        }
        mongo.db.users.insert_one(user_register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash('Registration successful! Welcome to ST-Archive, '
              f'{request.form.get("username").capitalize()}')
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

    Fetch only the username from the db and redirect user in session
        to the profile page.
    Return user not in session to the login page.
    """
    st_series = list(mongo.db.series.find())
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    fav_series_list = user["favourites_series"]
    favourites_series = list(
        mongo.db.series.find({"series_name": {"$in": fav_series_list}})
    )
    user_reviews = list(mongo.db.reviews.find(
        {"created_by": session["user"].capitalize()}
    ))
    fav_books_list = user["favourites_books"]
    favourites_books = list(
        mongo.db.books.find({"_id": {"$in": fav_books_list}}
                            ))
    books_wishlist = user["wishlist"]
    wishlist = list(mongo.db.books.find({"_id": {"$in": books_wishlist}}))
    finished_books_list = user["finished_books"]
    finished_books = list(mongo.db.books.find(
        {"_id": {"$in": finished_books_list}})
        )
    if session["user"]:
        return render_template("profile.html", username=username, user=user,
                               favourites_series=favourites_series,
                               user_reviews=user_reviews, series=st_series,
                               favourites_books=favourites_books,
                               wishlist=wishlist,
                               finished_books=finished_books)

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
    Let user mark book as finished, or add it to favourites
    or user's wish list.
    """
    st_series = list(mongo.db.series.find())
    books = list(mongo.db.books.find())
    # result = list(mongo.db.books.find())


    return render_template("series.html/", series=st_series, books=books
                            )


@app.route("/add_fav_series/", methods=["GET", "POST"])
@login_required
def add_fav_series():
    """Add series to array favourites_series in users collection.

    Only add series that are not already in the user's favourites_series array.
    """
    show_name = request.args["name"]
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    if show_name in user["favourites_series"]:
        flash(f"Information: '{show_name}' is already in your favourites. "
              "Adding it multiple times to your favourites is not logical. "
              "Request denied.")
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"favourites_series": show_name}}
            )
        flash("Incoming message from ST-Archive: "
              f"'{show_name}' has been added to your favourites! "
              "ST-Archive out.")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/mark_book_as_finished/<book_id>", methods=["GET", "POST"])
@login_required
def mark_book_as_finished(book_id):
    """Add book to array finished_books in users collection.

    Only add books that have not already been marked as finished.
    """
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    title = book["title"]
    if ObjectId(book_id) in user["finished_books"]:
        flash(f"Information: You have already marked '{title}' as finished. "
              "Request denied.")
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"finished_books": ObjectId(book_id)}}
        )
        flash("Incoming message from ST-Archive: "
              f"'{title}' has been marked as finished! "
              "ST-Archive out.")

    return redirect(url_for("profile", username=session["user"]))


@app.route("/add_book_to_favs/<book_id>", methods=["GET", "POST"])
@login_required
def add_book_to_favs(book_id):
    """Add book to array favourites_books in users collection.

    Check first whether to book in question is not already in the user's
    favourites list.
    """
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    title = book["title"]
    if ObjectId(book_id) in user["favourites_books"]:
        flash(f"Information: '{title}' is already in your favourites list. "
              "Request denied.")
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"favourites_books": ObjectId(book_id)}}
        )
        flash("Incoming message from ST-Archive: "
              f"'{title}' has been added to your favourites! "
              "ST-Archive out.")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/add_book_to_wishlist/<book_id>", methods=["GET", "POST"])
@login_required
def add_book_to_wishlist(book_id):
    """Add book to array wishlist in users collection.

    Check whether the book is already in the user's wish list.
    Only add books to the wishlist that are not in the wish list.
    """
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    title = book["title"]
    if ObjectId(book_id) in user["wishlist"]:
        flash(f"'{title}' is already in your wish list. "
              "Adding it to your wishlist is not logical. Request denied.")
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"wishlist": ObjectId(book_id)}}
        )
        flash("Incoming message from ST-Archive: "
              f"'{title}' has been added to your wishlist! ST-Archive out.")
    return redirect(url_for("profile", username=session["user"]))


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
                           series=st_series, review_book=review_book,
                           book_series=book_series)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
# decorator unnecessary because functionality only available on profile page?
@login_required
def edit_review(review_id):
    """Update user's own review.

    Update review both in the user profile and reviews page.
    """
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
              "Your update to your review has been successfuly transmitted!"
              "ST-Archive out.")
        return redirect(url_for("profile", username=session["user"]))

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    st_series = list(mongo.db.series.find())
    return render_template("edit_review.html",
                           series=st_series, username=username, review=review)


@app.route("/delete_review/<review_id>")
# decorator unnecessary because functionality only available on profile page?
@login_required
def delete_review(review_id):
    """Allow user to delete his or her own reviews.

    Show confirmation dialogue before actually deleting the review.
    Give user the ability to cancel the process and return to the profile page.
    """
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash("Message from ST-Archive incoming:"
          "Review successfully deleted from memory banks")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/reviews")
def reviews():
    """Render page with all reviews.

    Sort by series and within a series by number.
    """

    st_series = list(mongo.db.series.find())
    all_reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", series=st_series,
                           all_reviews=all_reviews)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
