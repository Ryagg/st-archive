import os
import ssl
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

@app.route("/")
def index():
    series = list(mongo.db.series.find())
    return render_template("index.html", series=series)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Add newly created users to the database.

    Return empty strings as values for favourites_series, favourites_books and wishlist
    since they will be added to the database at a later point.
    Set 'is_admin' to false by default for all users.
    """
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
        flash(f'Registration successful! Welcome to ST-Archive, {request.form.get("username")}')
        # return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """sumary_line"""
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f'Welcome, {request.form.get("username")}!')
                return redirect(url_for("index", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/copyrights")
def copyrights():
    """Render page with info about copyrights and licenses."""
    return render_template("copyrights.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
