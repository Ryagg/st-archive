import os
import ssl
from functools import wraps
from bson.objectid import ObjectId
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Markup)
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_talisman import Talisman
from flask_seasurf import SeaSurf
from flask_paginate import Pagination, get_page_args
import cloudinary as Cloud
# needed because the file won't be found after deployment to heroku
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
# prevent cross-site request forgery
csrf = SeaSurf(app)

# whitelist domains for content security policy
csp = {
    'base-uri': [
        '\'unsafe-inline\' \'self\'',
    ],
    'default-src': [
        '\'unsafe-inline\' \'self\'',
        '*.fontawesome.com',
        '*.herokuapp.com',
        '*.jsdelivr.net'
    ],
    'img-src': '*',
    'script-src': [
        # unsafe-eval needed for FontTracking
        '\'unsafe-inline\' \'unsafe-eval\' \'self\'',
        '*.fontawesome.com',
        '*.herokuapp.com',
        '*.jquery.com',
        '*.jsdelivr.net'
    ],
    'script-src-elem': [
        '\'unsafe-inline\' \'self\'',
        '*.fontawesome.com',
        '*.herokuapp.com',
        '*.jquery.com',
        '*.jsdelivr.net'
    ]
}

# add HTTP security headers and nonce
Talisman(app, content_security_policy=csp,
         content_security_policy_nonce_in=['script-src', 'script-src-elem'])

# mailtrap credentials
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_AUTH'] = ['PLAIN', 'LOGIN', 'CRAM-MD5']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# cloudinary credentials
Cloud.config.update = ({
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})

# pass keyword param to avoid pymongo error 'SSL: CERTIFICATE_VERIFY_FAILED'
mongo = PyMongo(app, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)


# Books pagination limit
PER_PAGE = 6

# Pagination
"""Credit: Ed Bradley
@ https://github.com/Edb83/self-isolution/blob/master/app.py
"""


def paginate(books):
    # pylint: disable=unbalanced-tuple-unpacking
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    offset = page * PER_PAGE - PER_PAGE
    return books[offset: offset + PER_PAGE]


def pagination_args(books):
    """Credit for pylint comment:
    Amy OShea
    @ https://github.com/AmyOShea/MS3-Cocktail-Hour/blob/master/app.py
    """
    # pylint: disable=unbalanced-tuple-unpacking
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = len(books)
    return Pagination(page=page, per_page=PER_PAGE, total=total)


"""
End Credit
"""

# NO REGISTRATION REQUIRED


# homepage
@app.route("/")
def index():
    """Render the index page."""
    st_series = list(mongo.db.series.find())
    return render_template("index.html.jinja", series=st_series)


# search function
@app.route("/search", methods=["GET", "POST"])
def search():
    """Text search within titles and blurbs."""
    st_series = list(mongo.db.series.find())
    # books = list(mongo.db.books.find())
    query = request.form.get("query")
    books = list(mongo.db.books.find({"$text": {"$search": query}}))
    books_paginate = paginate(books)
    pagination = pagination_args(books)

    return render_template("all_books.html.jinja", series=st_series,
                           books=books_paginate, pagination=pagination,
                           )


# all books sorted by title
@app.route("/all_books/")
def all_books():
    """Display information about books in the db.

    Show book cover, title, number, info about available bookformats.
    Display blurb.
    Let user mark book as finished, or add it to favourites
    or user's wish list.
    """
    st_series = list(mongo.db.series.find())
    books = list(mongo.db.books.find().sort("title", 1))
    books_paginate = paginate(books)
    pagination = pagination_args(books)

    return render_template("all_books.html.jinja/", books=books_paginate,
                           pagination=pagination, series=st_series,
                           )


# all books in the selected series sorted by number
@app.route("/series/<series_code>", methods=["GET", "POST"])
def series(series_code):
    """Displays all books for the selected series."""
    st_series = list(mongo.db.series.find())
    shows = list(mongo.db.series.find())
    show = mongo.db.series.find_one({"_id": ObjectId(series_code)})
    books = list(mongo.db.books.find(
        {"series_code": show["series_code"]})
    )
    books_paginate = paginate(books)
    pagination = pagination_args(books)

    return render_template("series.html.jinja/", show=show, shows=shows,
                           books=books_paginate, pagination=pagination,
                           series=st_series
                           )


# all reviews
@app.route("/reviews")
def reviews():
    """Render page with all reviews.

    Sort by series and within a series by number.
    """

    st_series = list(mongo.db.series.find())
    all_reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html.jinja", series=st_series,
                           all_reviews=all_reviews)


# contact form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Collect data from the contact form and forward to admin as email."""
    if request.method == "POST":
        try:
            msg = Message("Message from user",
                          sender=request.form.get("email"),
                          recipients=['sev2275@gmx.com'])
            msg.body = request.form.get("message")
            mail.send(msg)
            flash(Markup("<i class='fal fa-satellite-dish'></i> "
                         "Subspace message received. Thank you. "
                         "We will answer as soon as possible. "
                         "Closing subspace link."
                         ))
        except Exception as ex:
            flash(Markup(
                "<i class='fal fa-exclamation-circle has-text-danger'></i> "
                "Information: Your message could not be sent. "
                "Please try again later. Thank you. "
                "<i class='fal fa-exclamation-circle has-text-danger'></i>"))
        # remove before submitting?
        else:
            print("message sent")
    st_series = list(mongo.db.series.find())
    return render_template("contact.html.jinja", series=st_series)


# copyrights
@app.route("/copyrights")
def copyrights():
    """Render page with info about copyrights and licenses."""
    st_series = list(mongo.db.series.find())

    return render_template("copyrights.html.jinja", series=st_series)


# USER ACCOUNT

# login decorator
def login_required(function):
    """Add route protection by restricting access
        to authenticated users only."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash(Markup("<i class='fas fa-siren-on has-text-danger pr-2'></i>"
                         "Security alert: Access restricted. "
                         "Authentication required. "
                         "Enter credentials. "
                         "<i class='fas fa-siren-on has-text-danger'></i>"))
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return decorated_function


# register
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
            flash(Markup(
                "<i class='fas fa-do-not-enter has-text-danger'></i>"
                " Security alert: incorrect Username and/or Password. "
                "Access denied. "
                "<i class='fas fa-do-not-enter has-text-danger'></i>"))
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
            "is_admin": False
        }
        mongo.db.users.insert_one(user_register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        session["admin"] = False
        flash(Markup('Registration successful! Welcome to ST-Archive, '
              f'{request.form.get("username").capitalize()} '
                     '<i class="far fa-handshake"></i>'))
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html.jinja", series=st_series)


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Let existing users log in if they enter the correct password.

    Display a generic error message for users who are either not in the
    database or who entered an incorrect password.
    """
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
                # add admin status to 'session' cookie
                session["admin"] = existing_user["is_admin"]
                flash(f'Welcome, {request.form.get("username").capitalize()}!')
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash(Markup(
                    "<i class='fal fa-info-circle has-text-danger'></i>"
                    " Incorrect Username and/or Password "
                    "<i class='fal fa-info-circle has-text-danger'></i>"))
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash(Markup(
                "<i class='fal fa-info-circle has-text-danger'></i>"
                " Incorrect Username and/or Password "
                "<i class='fal fa-info-circle has-text-danger'></i>"))
            return redirect(url_for("login"))
    return render_template("login.html.jinja", series=st_series)


# profile
@app.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    """Return user's profile page.

    Fetch only the username from the db and redirect user in session
        to the profile page.
    Return user not in session to the login page.
    """
    st_series = list(mongo.db.series.find())
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    username = user["username"]
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

    return render_template("profile.html.jinja", username=username, user=user,
                           favourites_series=favourites_series,
                           user_reviews=user_reviews, series=st_series,
                           favourites_books=favourites_books,
                           wishlist=wishlist,
                           finished_books=finished_books)


# logout
@app.route("/logout")
@login_required
def logout():
    """Logs users out and clears session cookies."""
    # remove user from session cookies
    flash(Markup("You have been logged out. "
                 "<i class='fal fa-sign-out-alt'></i>"))
    session.clear()

    return redirect(url_for("login"))


# USER ACTIONS REGARDING BOOKS OR SERIES

# add selected series to favourites
@app.route("/add_fav_series/<series_id>", methods=["GET", "POST"])
@login_required
def add_fav_series(series_id):
    """Add series to array favourites_series in users collection.

    Only add series that are not already in the user's favourites_series array.
    """
    show = mongo.db.series.find_one({"_id": ObjectId(series_id)})
    show_name = show["series_name"]
    user = mongo.db.users.find_one(
        {"username": session["user"]})
    if show_name in user["favourites_series"]:
        flash(Markup("<i class='fal fa-exclamation-circle'></i> "
                     f"Information: '{show_name}' is already in your "
                     "favourites. Adding it multiple times to your favourites "
                     "is not logical. Request denied."))
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"favourites_series": show_name}}
        )
        flash(Markup("<i class='fal fa-info-square'></i> "
                     "Incoming message from ST-Archive: "
                     f"'{show_name}' has been added to your favourites! "
                     "ST-Archive out."))
    return redirect(url_for("profile", username=session["user"]))


# mark selected book as finished
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
        flash(Markup("<i class='fal fa-exclamation-circle'></i> "
                     f"Information: You have already marked '{title}' "
                     "as finished. Request denied."))
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"finished_books": ObjectId(book_id)}}
        )
        flash(Markup("<i class='fal fa-info-square'></i> "
                     "Incoming message from ST-Archive: "
                     f"'{title}' has been marked as finished! "
                     "ST-Archive out."))

    return redirect(url_for("profile", username=session["user"]))


# add selected book to favourites
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
        flash(Markup("<i class='fal fa-exclamation-circle'></i> "
                     f"Information: '{title}' is already in your favourites "
                     "list. Request denied."))
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"favourites_books": ObjectId(book_id)}}
        )
        flash(Markup("<i class='fal fa-info-square'></i> "
                     "Incoming message from ST-Archive: "
                     f"'{title}' has been added to your favourites! "
                     "ST-Archive out."))
    return redirect(url_for("profile", username=session["user"]))


# add selected book to wish list
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
        flash(Markup("<i class='fal fa-exclamation-circle'></i> "
                     f"'{title}' is already in your wish list. "
                     "Adding it to your wishlist is not logical. "
                     "Request denied."))
    else:
        mongo.db.users.find_one_and_update(
            {"username": session["user"]},
            {"$push": {"wishlist": ObjectId(book_id)}}
        )
        flash(Markup("<i class='fal fa-info-square'></i> "
                     "Incoming message from ST-Archive: "
                     f"'{title}' has been added to your wishlist! "
                     "ST-Archive out."))
    return redirect(url_for("profile", username=session["user"]))


# write a review for a selected book
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
        flash(Markup("<i class='fal fa-check-circle has-text-success'></i> "
                     "Incoming message from ST-Archive: "
                     "Your review has been successfuly transmitted! "
                     "ST-Archive out."))
        return redirect(url_for("all_books"))

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    st_series = list(mongo.db.series.find())
    review_book = request.args['title']
    book_series = mongo.db.books.find_one(
        {"title": review_book})["series_code"]

    return render_template("review.html.jinja", username=username,
                           series=st_series, review_book=review_book,
                           book_series=book_series)


# edit selected review
@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
@login_required
def edit_review(review_id):
    """Update user's own review.

    Update review both in the user profile and reviews page.
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    st_series = list(mongo.db.series.find())
    # prevent users from editing reviews from other users
    if session["user"].capitalize() == review["created_by"]:
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
            flash(Markup("<i class='fal fa-check-circle has-text-success'></i>"
                         " Incoming message from ST-Archive: "
                         "Your update to your review has been successfuly "
                         "transmitted! ST-Archive out."))
            return redirect(url_for("profile", username=session["user"]))
    else:
        flash(Markup(
            "<i class='fas fa-do-not-enter has-text-danger'></i>"
            " Security alert: Insufficient privileges. Access denied. "
            "<i class='fas fa-do-not-enter has-text-danger'></i>"))
        return redirect(url_for("profile", username=session["user"]))

    return render_template("edit_review.html.jinja",
                           series=st_series, username=username, review=review)


# delete selected review
@app.route("/delete_review/<review_id>")
# decorator unnecessary because functionality only available on profile page?
@login_required
def delete_review(review_id):
    """Allow user to delete his or her own reviews.

    Show confirmation dialogue before actually deleting the review.
    Give user the ability to cancel the process and return to the profile page.
    """
    mongo.db.reviews.delete_one({"_id": ObjectId(review_id)})
    flash(Markup("<i class='fal fa-info-square'></i>"
                 "Message from ST-Archive incoming: "
                 "Review successfully deleted from memory banks."))
    return redirect(url_for("profile", username=session["user"]))


# ADMIN SECTION

# admin decorator
def admin_required(function):
    """Add route protection by restricting access
        to authenticated users with admin privileges only."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not session["admin"]:
            flash(Markup(
                "<i class='fas fa-do-not-enter has-text-danger'></i>"
                " Security alert: Authorisation Alpha-Theta required."
                " Access denied. "
                "<i class='fas fa-do-not-enter has-text-danger'></i>"))
            return redirect(url_for("profile", username=session["user"]))
        return function(*args, **kwargs)
    return decorated_function


# add series to collection
@app.route("/add_series", methods=["GET", "POST"])
@login_required
@admin_required
def add_series():
    """Add new series to the database."""
    if request.method == "POST":
        new_series = {
            "series_name": request.form.get("new_series_name"),
            "series_code": request.form.get("new_series_code"),
            "series_ended": False
        }
        mongo.db.series.insert_one(new_series)
        flash(Markup("<i class='fal fa-database'></i> "
                     "Incoming message from ST-Archive: "
                     "New entry added to database. Thank you. "
                     "ST-Archive out."))
        return redirect(url_for("profile", username=session["user"]))

    st_series = list(mongo.db.series.find())
    return render_template("add_series.html.jinja", series=st_series,
                           username=session["user"])


# add book to collection
@app.route("/add_book", methods=["GET", "POST"])
@login_required
@admin_required
def add_book():
    """Add new book to the database."""
    if request.method == "POST":
        new_book = {
            "title": request.form.get("new_book_title"),
            "series_code": request.form.get("new_book_series_code").upper(),
            "number": request.form.get("new_book_number"),
            "e_book": request.form.get("new_book_e_book"),
            "paper_book": request.form.get("new_book_paper_book"),
            "audio_book": request.form.get("new_book_audio_book"),
            "part_of_mini_series": request.form.get("new_book_mini_series"),
            "blurb": request.form.get("new_book_blurb"),
            "cover": request.form.get("new_book_cover"),
            "isbn": request.form.get("new_book_isbn"),
            "timespan_start": request.form.get("new_book_timespan_start"),
            "status": request.form.get("new_book_status")
        }
        mongo.db.books.insert_one(new_book)
        flash(Markup("<i class='fal fa-database'></i> "
                     "Incoming message from ST-Archive: "
                     "New entry added to database. Thank you. "
                     "ST-Archive out."))
        return redirect(url_for("profile", username=session["user"]))

    st_series = list(mongo.db.series.find())
    return render_template("add_book.html.jinja", series=st_series,
                           username=session["user"])


# GENERAL DATA PROTECTION REGULATION

@app.route("/site_notice")
def site_notice():
    """Render site notice in compliance with GDPR."""
    st_series = list(mongo.db.series.find())
    return render_template("site_notice.html.jinja", series=st_series)


@app.route("/privacy_policy")
def privacy_policy():
    """Render privacy policy in compliance with GDPR."""
    st_series = list(mongo.db.series.find())
    return render_template("privacy_policy.html.jinja", series=st_series)


# ERROR PAGES

# 404 page
@app.errorhandler(404)
def page_not_found(error):
    """Display 404 page with link to homepage."""
    return render_template("404.html.jinja")


# 500 page
@app.errorhandler(500)
def server_error(error):
    """Display 500 page with link to homepage."""
    return render_template("500.html.jinja")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
