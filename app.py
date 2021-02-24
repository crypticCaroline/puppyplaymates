import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        flash("Registration Successful!")
        return redirect(url_for("buildprofile", username=session["user"]))
    return render_template("register.html")


@app.route("/buildprofile/<username>", methods=["GET", "POST"])
def buildprofile(username):

    user = mongo.db.users.find_one({"username": username})
    puppy_love = "WOOF WOOF" if request.form.get("puppy_love") else "Not for Me"
    fertile = "I got the goods" if request.form.get("fertile") else "Had the Snip"
    
    if request.method == "POST":
        mongo.db.users.update_one(
            {"username": session["user"]},
            {"$set": {
                "dog_name": request.form.get("dog_name"),
                "dog_description": request.form.get("dog_description"),
                "dog_breed": request.form.get("dog_breed"),
                "dog_gender": request.form.get("dog_gender"),
                "dog_location": request.form.get("dog_location"),
                "dog_size": request.form.get("dog_size"),
                "dog_dob": request.form.get("dog_dob"),
                "puppy_love": puppy_love,
                "fertile": fertile
            }}
        )

        flash("Task Successfully Updated")
        return redirect(url_for("profile",  username=session[
            "user"], user=user))

    return render_template("buildprofile.html", username=session[
        "user"], user=user)


@ app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    user = mongo.db.users.find_one({"username": username})
    print(user)

    if session["user"]:
        return render_template("profile.html", username=username, user=user)

    return redirect(url_for('homepage'))


@app.route("/all_users")
def all_users():
    users = mongo.db.users.find()
    return render_template("all_users.html", users=users)


@ app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user=mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            # ensure hash matches
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"]=request.form.get("username")
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@ app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host = os.environ.get("IP"),
            port = int(os.environ.get("PORT")),
            debug = True)


# @app.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     return 'bad request!', 400
