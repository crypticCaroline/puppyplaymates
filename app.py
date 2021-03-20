import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api
import random
import string
from flask_mail import Mail, Message
import time
from datetime import datetime
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
app.config['MAIL_USE_SSL'] = os.environ.get("MAIL_USE_SSL")
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")

mongo = PyMongo(app)
mail = Mail(app)


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")


# registration pages 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username/ email already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        if existing_email:
            flash("This email is already registered, please head to the login page")
            return redirect(url_for("register"))

        # checks to see if both passwords match
        if request.form['password'] != request.form['repeat-password']:
            flash("Passwords did not match, please try again")
            return redirect(url_for("register"))
        
        # gets values from fields for registration
        register = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "dog_liker": [{"dog_name": "Puppy Playmates"}],
            "image_url":
            "https://res.cloudinary.com/puppyplaymates/image/upload/dog_avatar_uskzh1.png",
            "all_images": [],
            "comments": [],
            "next_walk": {
                'date': "",
                'time': "",
                'place': "",
                'walk_description': ""
            }}

        # inserts new user into database
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")

        # sends user a welcome message
        user_email = request.form.get('email')
        msg = Message("Welcome to Puppyplaymates",
                        html="<p>Hello  %s </p><p>Thank you for registering with us at PuppyPlaymates.</p><p>We are excited to have you join us and hope you have success finding a playmate for your Pup!</p> <p>The Team at PuppyPlaymates</p>" % session['user'],
                        sender="thepuppyplaymates@gmail.com",
                        recipients=[user_email])
        mail.send(msg)

        return redirect(url_for("build_profile", username=session["user"]))
    return render_template("register.html")


@app.route("/build_profile/<username>", methods=["GET", "POST"])
def build_profile(username):
    if session:
        # finds user
        user = mongo.db.users.find_one({"username": session['user']})
        # updates the database with dog details
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
                    "puppy_love": request.form.get('puppy_love'),
                    "fertile": request.form.get('fertile')
                }}
            )
            return redirect(url_for("profile",  username=session[
                "user"]))
        return render_template("build_profile.html", username=session[
            "user"], user=user)
    return render_template("homepage.html")


# login
@ app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # checks to see if user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        existing_email = mongo.db.users.find_one(
            {"username": request.form.get('username')})

        if existing_user or existing_email:
            # ensure hash matches then logs user in
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username")
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


# allows users to search for certain parameters
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("all_users.html", users=users)


# log the user out
@ app.route("/logout")
def logout():
    session.pop("user")
    flash("You have been logged out")
    return redirect(url_for("login"))


# edit pages
# edit dog
@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username):
    if session:

        user_profile = mongo.db.users.find_one({"username": username})

        # lets users change some details of their dog 
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {
                    "dog_description": request.form.get("dog_description"),
                    "dog_location": request.form.get("dog_location"),
                    "dog_size": request.form.get("dog_size"),
                    "puppy_love": request.form.get('puppy_love'),
                    "fertile": request.form.get('fertile')
                }}
            )
            return redirect(url_for("profile",  username=session[
                "user"]))
        return render_template("edit_profile.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


# edit human
@app.route("/edit_human/<username>", methods=["GET", "POST"])
def edit_human(username):
    if session:

        user_profile = mongo.db.users.find_one({"username": username})
        # edits human details in database
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {
                    "human_name": request.form.get("human_name"),
                    "human_description": request.form.get("human_description")
                }}
            )
            return redirect(url_for("profile",  username=session[
                "user"]))
        return render_template("edit_human.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


# edit images
@app.route("/edit_images/<username>", methods=["GET", "POST"])
def edit_images(username):
    if session:
        user_profile = mongo.db.users.find_one({"username": username})

        return render_template("profile.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


@app.route("/edit_images/profile_photo/<username>", methods=["GET", "POST"])
def profile_photo(username):
    if session:
        # finds instance in datebase to set the profile picture
        user_profile = mongo.db.users.find_one({"username": username})
        image = request.form.get('submit')

        if request.method == 'POST':
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {"image_url": request.form.get('photo')}})
            return redirect(url_for('profile', username=username))
        return render_template("profile.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


# deletes images
@app.route("/delete_images/<username>", methods=["GET", "POST"])
def delete_images(username):
    if session:
        user_profile = mongo.db.users.find_one({"username": username})
        if request.method == 'POST':
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$pull": {"all_images": request.form.get('photo')}})
            return redirect(url_for('profile', username=username))
        return render_template("profile.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


# uploads images to database
@app.route("/edit_images/<username>/upload/", methods=["GET", "POST"])
def upload_image(username):
    if session:
        if request.method == 'POST':
            # get file from form
            for item in request.files.getlist("image_file"):
                # creates a string for the file name to upload to cloudinary
                filename = secure_filename(item.filename)
                filename, file_extension = os.path.splitext(filename)
                public_id = (username + '/' + filename)
                # uploads to cloudinary
                cloudinary.uploader.unsigned_upload(
                    item, "puppy_image", cloud_name='puppyplaymate',
                    folder='/user_images/', public_id=public_id)
                # sets a url for image to be saved to the database
                image_url = (
                    "https://res.cloudinary.com/puppyplaymate/image/upload/user_images/"
                    + public_id + file_extension)
                # adds the url to the database
                mongo.db.users.update_one(
                    {"username": session["user"]},
                    {"$addToSet": {"all_images": image_url}})
                # if the user click the profile check it will set it as their profile image
                if request.form.get('profile_check'):
                    mongo.db.users.update_one(
                        {"username": session["user"]},
                        {"$set": {"image_url": image_url}})

            return redirect(url_for('edit_images', username=username))
        return render_template("edit_images.html", username=username)
    flash("You need to be sign in to view this page")
    return render_template('homepage.html')


@ app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    if session:
        user_profile = mongo.db.users.find_one({"username": username})
        user_session = mongo.db.users.find_one({"username": session['user']})
        dog_like = False

        for dogs_like in user_profile["dog_liker"]:
            dog_name = dogs_like['dog_name']
            if user_session["dog_name"] == dog_name:
                dog_like = True

        if request.method == "POST":
            liker_btn = request.form.get("liker_btn")
            unliker_btn = request.form.get("unliker_btn")

            if liker_btn:
                return redirect(url_for(
                    'likes', username=username))

            if unliker_btn:
                return redirect(url_for(
                    'dislikes', username=username))

        return render_template(
            "profile.html",
            username=username, user_profile=user_profile,
            user_session=user_session, dog_like=dog_like)
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# liker function 
@app.route("/profile/<username>/liker")
def likes(username):
    # finds the users and profile details
    user_session = mongo.db.users.find_one({"username": session['user']})
    user_profile = mongo.db.users.find_one({"username": username})

    # adds the liker to the profiles users array
    mongo.db.users.update_one(
        {"username": username},
        {"$addToSet": {"dog_liker": {
                       'user': user_session['_id'],
                       'image_url': user_session['image_url'],
                       'dog_name': user_session['dog_name'],
                       'username': user_session['username']
                       }}})

    # adds the profile the session users has liked to they liked array 
    mongo.db.users.update_one(
        {"username": user_session['username']},
        {"$addToSet": {"dogs_liked": {
                       'user': user_profile['_id'],
                       'image_url': user_profile['image_url'],
                       'dog_name': user_profile['dog_name'],
                       'username': user_profile['username']
                       }}})
    # uses time.sleep so the user sees the overlay
    time.sleep(2)
    return redirect(url_for('profile', username=username))


# disliker function
@app.route('/profile/<username>/disliker')
def dislikes(username):
    # finds the users and profile details
    user_session = mongo.db.users.find_one({"username": session['user']})
    user_profile = mongo.db.users.find_one({"username": username})

    # removes the user form the array 
    mongo.db.users.update_many(
        {"username": username},
        {"$pull": {"dog_liker": {"user": ObjectId(user_session["_id"])}}})

    # removes the profile from the liked array
    mongo.db.users.update_many(
        {"username": user_session['username']},
        {"$pull": {"dogs_liked": {
            'user': ObjectId(user_profile['_id'])
        }}})
    # delays the redirect so the user gets to see the overlay animation 
    time.sleep(2)
    return redirect(url_for('profile', username=username))


# displays all the users
@app.route("/all_users")
def all_users():
    if session:
        users = mongo.db.users.find()
        return render_template("all_users.html", users=users)
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))





# lets the user add a walk to their profile
@app.route("/profile/<username>/add_walk", methods=["GET", "POST"])
def add_walk(username):

    if session:
        user_profile = mongo.db.users.find_one({"username": username})

        if request.method == "POST":
            # updates the users walk details in the database
            mongo.db.users.update_one(
                {"username": username},
                {"$set": {
                 "next_walk": {
                     'date': request.form.get('date'),
                     'time': request.form.get('time'),
                     'place': request.form.get('place'),
                     'walk_description': request.form.get('walk_description')
                    }}})
            return redirect(url_for('profile', username=username))
        return render_template("add_walk.html", username=session[
            "user"], user_profile=user_profile)
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# Comments
# Adds a comment to the users profile 
@app.route("/profile/<username>/comment", methods=["GET", "POST"])
def add_comment(username):

    if session:
        user_session = mongo.db.users.find_one({"username": session['user']})

        # Adds a comment to the users profile
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": username},
                {"$addToSet": {"comments": {
                    '_id': ObjectId(),
                    'date': datetime.now().strftime("%m/%d/%Y, %H:%M"),
                    'author': user_session['username'],
                    'author_dog': user_session['dog_name'],
                    'text': request.form.get('add_comment'),
                    'private': request.form.get('private')
                }}})
            return redirect(url_for('profile', username=username))

    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# edits comment
@app.route("/profile/<username>/edit_comment/<comment_id>", methods=["GET", "POST"])
def edit_comment(username, comment_id):

    if session:
        user_session = mongo.db.users.find_one({"username": session['user']})

        # lets the user edit the comment
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": username},
                {"$pull": {"comments": {"_id": ObjectId(comment_id)}}})

            mongo.db.users.update_one(
                {"username": username},
                {"$addToSet": {"comments":
                    {"_id": ObjectId(comment_id),
                    'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    'author': user_session['username'],
                    'author_dog': user_session['dog_name'],
                    'text': request.form.get('edit_comment'),
                    'private': request.form.get('private')
                }}})
        return redirect(url_for('profile', username=username))
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# deletes comment
@app.route("/profile/<username>/delete_comment/<comment_id>", methods=["GET", "POST"])
def delete_comment(username, comment_id):

    if session:
        # removes the comment from the database
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": username},
                {"$pull": {"comments": {"_id": ObjectId(comment_id)}}})

        return redirect(url_for('profile', username=username))
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage')) 


# deletes the users profile 
@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():
    if session: 
        # removes the user from the database
        if request.method == "POST":
            user = mongo.db.users.find_one({"username": session["user"]})
            session.pop("user")
            mongo.db.users.remove(user)
            flash("Profile Removed")
            return redirect(url_for("homepage"))
        return render_template("delete_profile.html")
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# mail
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if session:
        # creates a temporary password and sets it in the database
        if request.method == 'POST':
            temp_password = get_random_string(14)
            user = mongo.db.users.find_one(
                {"email": request.form.get("email")})

            if user:
                user_email = user['email']
                mongo.db.users.update_one(
                    {"email": request.form.get('email')},
                    {"$set": {
                        "temp_password": generate_password_hash(temp_password)}})

                # emails the temp password to the user 
                msg = Message("Reset Password",
                            html="<p>You look like you need to reset your password</p><p>This is your <b>Temporary password:</b> %s </p><a href='https://8080-bronze-catfish-6qabji6o.ws-eu03.gitpod.io/change_password'>Reset Password Link</a><p>If you didn't request this email to be sent it might be work logging into your account and changing your password</p><p>The Team at PuppyPlaymates</p>" % temp_password,
                            sender="thepuppyplaymates@gmail.com",
                            recipients=[user_email])

                mail.send(msg)
                return render_template("reset_sent.html")
            else:
                flash("Incorrect Username and/or Password, if you have forgotten your password you can reset it")
        return render_template("reset_password.html")
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# generates a random string for creating tempoary passwords 
def get_random_string(length):
    items = string.printable
    result_str = ''.join(random.choice(items) for i in range(length))
    return result_str


# change password section 
@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if session:
        if request.method == "POST":
        
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username")})

            # checks if the repeat password and new match
            if request.form['new-password'] != request.form['repeat-password']:
                flash("Passwords did not match. Please enter passwords again.")
                return render_template("change_password.html")

            if existing_user:
                # ensure hash matches their current password
                if check_password_hash(
                    existing_user["password"], request.form.get("current-password")):
                    # inserts new password in the database and assigns a new random temp password
                    mongo.db.users.update_one(
                        {"username": request.form.get('username')},
                        {"$set": {
                            "password": generate_password_hash(request.form.get('new-password')),
                            "temp_password": generate_password_hash(get_random_string(14))}})
                    session["user"] = request.form.get("username")
                    return redirect(url_for(
                        "profile", username=session["user"]))

                # ensures the hash matches if the user is using the temp password 
                elif check_password_hash(existing_user["temp_password"], request.form.get("current-password")):
                    # inserts the new password and resets the random temp password 
                    mongo.db.users.update_one(
                            {"username": request.form.get('username')},
                            {"$set": {
                                "password": generate_password_hash(request.form.get('new-password')),
                                "temp_password": generate_password_hash(get_random_string(14))}})
                    session['user'] = request.form.get("username")
                    return redirect(url_for(
                        "profile", username=session["user"]))
                else:
                    flash("Incorrect Username and/or Password")
                    return redirect(url_for("change_password"))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("change_password"))
        return render_template("change_password.html")
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# reprt user 
@app.route("/report_user", methods=["GET", "POST"])
def report_user():

    if session:
        user_session = mongo.db.users.find_one(
                {"username": session['user']})

        if request.method == 'POST':
            # gets the users deatils and report
            user_report = request.form.get('report-user')
            user_text = request.form.get('report-text')
            user_email = user_session['email']

            # creates a report string 
            report = (user_report + " with the following message: " + user_text)

            # sends email to company owners and ccs in reporter
            msg = Message("Report user",
                          html="<p>You have reported %s We will take a look into the users activity and take the appropriate action. <p>The Team at PuppyPlaymates</p>" % report,
                          sender="thepuppyplaymates@gmail.com",
                          cc=[user_email],
                          recipients=["thepuppyplaymates@gmail.com"])
            mail.send(msg)
            return render_template("report_user.html")

        else:
            flash(
                "Incorrect Username and/or Password, if you have forgotten your password you can reset it")
        return render_template("report_user.html")
    flash("You need to signed in to view this page")
    return redirect(url_for('homepage'))


# contact form
@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():

    if request.method == 'POST':
        user_email = request.form.get('email')
        user_text = request.form.get('message-text')

        message = ("Thank you for sending us the following message:" + user_text)

        # sends email to user
        msg = Message("Thank you for contacting us",
                      html="<p> %s </p><p>We will endevour to get back to you within 48hr</p> <p>The Team at PuppyPlaymates</p>" % message,
                      sender="thepuppyplaymates@gmail.com",
                      cc=[user_email],
                      recipients=["thepuppyplaymates@gmail.com"])
        mail.send(msg)
        flash("Email sent successfully")
        return render_template("contact_us.html")
    return render_template("contact_us.html")



# error handlers

@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host = os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)



# @app.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     return 'bad request!', 400
