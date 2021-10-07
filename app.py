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


@app.route("/copyright")
def copyright():
    return render_template("copyright.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
