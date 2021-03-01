import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_socketio import SocketIO, send, emit
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

socketio = SocketIO(app)

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
    if session:

        user = mongo.db.users.find_one({"username": username})
        puppy_love = "WOOF WOOF" if request.form.get(
            "puppy_love") else "Flying Solo"
        fertile = "Had the Snip" if request.form.get(
            "fertile") else "I got the goods"

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
                    "fertile": fertile,
                    "dog_liker": []
                }}
            )

            flash("Task Successfully Updated")
            return redirect(url_for("profile",  username=session[
                "user"], user=user))

        return render_template("buildprofile.html", username=session[
            "user"], user=user)
    return render_template("homepage.html")


@ app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    if session:
        user = mongo.db.users.find_one({"username": username})
        likers = mongo.db.users.find_one({"username": session['user']})

        if request.method == "POST":
            liker_btn = request.form.get("liker_btn")
            unliker_btn = request.form.get("unliker_btn")
            print(liker_btn)
            print(unliker_btn)

            if liker_btn:
                mongo.db.users.update_one(
                    {"username": username},
                    {"$addToSet": {"dog_liker": likers["dog_name"]}})

                return render_template(
                    "profile.html", username=username, user=user,
                    dog_like=True)

            if unliker_btn:
                mongo.db.users.update_one(
                    {"username": username},
                    {"$pull": {"dog_liker": likers["dog_name"]}})

                return render_template(
                    "profile.html", username=username, user=user,
                    dog_like=False)

        for dogo in user["dog_liker"]:
            if likers["dog_name"] == dogo:
                return render_template(
                    "profile.html",
                    username=username, user=user, dog_like=True)
        return render_template(
            "profile.html",
            username=username, user=user, dog_like=False)

    return redirect(url_for('homepage'))


@app.route("/all_users")
def all_users():
    users = mongo.db.users.find()
    return render_template("all_users.html", users=users)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("all_users.html", users=users)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            # ensure hash matches
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username")
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


@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():

    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"]})
        mongo.db.users.remove(user)
        session.pop(session["user"])
        flash("Category Successfully Removed")
        return redirect(url_for("homepage"))
    return render_template("delete_profile.html")


@app.route('/woofchat', methods=["GET", "POST"])
def woof_chat():
    return render_template('woof_chat.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('message')
def handle_message(message):
    send(message, namespace='/chat')


@socketio.on('my event')
def handle_my_custom_event(username, methods=['GET', 'POST']):
    emit('my response', username=username, namespace='/chat')


@socketio.on("event")
def my_event(message):
    print('my response', {'data': 'got it!'})


if __name__ == "__main__":
    socketio.run(app,
                 host=os.environ.get("IP"),
                 port=int(os.environ.get("PORT")),
                 debug=True)


# @app.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     return 'bad request!', 400
