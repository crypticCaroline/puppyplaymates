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
from flask_mail import Mail
from flask_mail import Message
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
app.config['MAIL_DEFAULT_SENDER']: os.environ.get("MAIL_DEFAULT_SENDER")

mongo = PyMongo(app)
mail = Mail(app)


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

        if request.form['new-password'] != request.form['repeat-password2']:
            flash("Passwords did not match. Please enter passwords again.") 

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

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        flash("Registration Successful!")
        return redirect(url_for("build_profile", username=session["user"]))
    return render_template("register.html")


@app.route("/build_profile/<username>", methods=["GET", "POST"])
def build_profile(username):
    if session:

        user = mongo.db.users.find_one({"username": username})

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

            flash("Task Successfully Updated")
            return redirect(url_for("profile",  username=session[
                "user"]))

        return render_template("build_profile.html", username=session[
            "user"], user=user)
    return render_template("homepage.html")


@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username):
    if session:

        user_profile = mongo.db.users.find_one({"username": username})

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

            flash("Task Successfully Updated")
            return redirect(url_for("profile",  username=session[
                "user"]))

        return render_template("edit_profile.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


@app.route("/edit_human/<username>", methods=["GET", "POST"])
def edit_human(username):
    if session:

        user_profile = mongo.db.users.find_one({"username": username})

        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {
                    "human_name": request.form.get("human_name"),
                    "human_description": request.form.get("human_description")
                }}
            )

            flash("Task Successfully Updated")
            return redirect(url_for("profile",  username=session[
                "user"]))

        return render_template("edit_human.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


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
        user_profile = mongo.db.users.find_one({"username": username})
        image = request.form.get('submit')
        if request.method == 'POST':
            print(image)
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {"image_url": request.form.get('photo')}})
            return redirect(url_for('profile', username=username))
        return render_template("profile.html", username=session[
            "user"], user_profile=user_profile)
    return render_template("homepage.html")


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


@app.route("/edit_images/<username>/upload/", methods=["GET", "POST"])
def upload_image(username):

    if request.method == 'POST':
        for item in request.files.getlist("image_file"):
            filename = secure_filename(item.filename)
            filename, file_extension = os.path.splitext(filename)
            public_id = (username + '/' + filename)
            cloudinary.uploader.unsigned_upload(
                item, "puppy_image", cloud_name='puppyplaymate',
                folder='/user_images/', public_id=public_id)
            image_url = (
                "https://res.cloudinary.com/puppyplaymate/image/upload/user_images/"
                + public_id + file_extension)
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$addToSet": {"all_images": image_url}})

            if request.form.get('profile_check'):
                mongo.db.users.update_one(
                    {"username": session["user"]},
                    {"$set": {"image_url": image_url}})

        return redirect(url_for('edit_images', username=username))
    return render_template("edit_images.html", username=username)


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

    return redirect(url_for('homepage'))


@app.route("/profile/<username>/liker")
def likes(username):
    user_session = mongo.db.users.find_one({"username": session['user']})
    user_profile = mongo.db.users.find_one({"username": username})

    mongo.db.users.update_one(
        {"username": username},
        {"$addToSet": {"dog_liker": {
                       'user': user_session['_id'],
                       'image_url': user_session['image_url'],
                       'dog_name': user_session['dog_name'],
                       'username': user_session['username']
                       }}})

    mongo.db.users.update_one(
        {"username": user_session['username']},
        {"$addToSet": {"dogs_liked": {
                       'user': user_profile['_id'],
                       'image_url': user_profile['image_url'],
                       'dog_name': user_profile['dog_name'],
                       'username': user_profile['username']
                       }}})
    time.sleep(2)
    return redirect(url_for('profile', username=username))


@app.route('/profile/<username>/disliker')
def dislikes(username):
    user_session = mongo.db.users.find_one({"username": session['user']})
    user_profile = mongo.db.users.find_one({"username": username})
    print(user_session['_id'])

    mongo.db.users.update_many(
        {"username": username},
        {"$pull": {"dog_liker": {"user": ObjectId(user_session["_id"])}}})

    mongo.db.users.update_many(
        {"username": user_session['username']},
        {"$pull": {"dogs_liked": {
            'user': ObjectId(user_profile['_id'])
        }}})

    time.sleep(2)
    return redirect(url_for('profile', username=username))


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


@app.route("/profile/<username>/add_walk", methods=["GET", "POST"])
def add_walk(username):

    if session:

        user_profile = mongo.db.users.find_one({"username": username})

        if request.method == "POST":
            print(request.form.get('date'))

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

    return render_template("homepage.html")


@app.route("/profile/<username>/comment", methods=["GET", "POST"])
def add_comment(username):

    if session:
        user_session = mongo.db.users.find_one({"username": session['user']})

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

    return render_template("homepage.html")


@app.route("/profile/<username>/edit_comment/<comment_id>", methods=["GET", "POST"])
def edit_comment(username, comment_id):

    if session:
        user_session = mongo.db.users.find_one({"username": session['user']})
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


@app.route("/profile/<username>/delete_comment/<comment_id>", methods=["GET", "POST"])
def delete_comment(username, comment_id):

    if session:

        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": username},
                {"$pull": {"comments": {"_id": ObjectId(comment_id)}}})

    return redirect(url_for('profile', username=username))


@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():

    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"]})
        session.pop("user")
        mongo.db.users.remove(user)
        flash("Profile Removed")
        return redirect(url_for("homepage"))
    return render_template("delete_profile.html")

# mail


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

    if request.method == 'POST':
        temp_password = get_random_string(14)
        user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if user:

            mongo.db.users.update_one(
                {"email": request.form.get('email')},
                {"$set": {
                    "temp_password": generate_password_hash(temp_password)}})

            msg = Message("Reset Password",
                          html="<p>You look like you need to reset your password</p><p>This is your <b>Temporary password:</b> %s </p><a href='https://8080-bronze-catfish-6qabji6o.ws-eu03.gitpod.io/change_password'>Reset Password Link</a><p>If you didn't request this email to be sent it might be work logging into your account and changing your password</p><p>The Team at PuppyPlaymates</p>" % temp_password,
                          sender="thepuppyplaymates@gmail.com",
                          recipients=[user.email])

            mail.send(msg) 
            return render_template("reset_sent.html")
        else:
            flash("Incorrect Username and/or Password, if you have forgotten your password you can reset it")

    return render_template("reset_password.html")


def get_random_string(length):
    letters = string.printable
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


  
@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if request.method == 'POST':
        if request.method == "POST":
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username")})

        if request.form['new-password'] != request.form['repeat-password']:
            flash("Passwords did not match. Please enter passwords again.")
            return render_template("change_password.html")

        if existing_user:
            # ensure hash matches
            if check_password_hash(
                existing_user["password"], request.form.get("current-password")):
                mongo.db.users.update_one(
                    {"username": request.form.get('username')},
                    {"$set": {
                        "password": generate_password_hash(request.form.get('new-password')),
                        "temp_password": get_random_string(14)}})
                session["user"] = request.form.get("username")

                return redirect(url_for(
                    "profile", username=session["user"]))

            elif check_password_hash(existing_user["temp_password"], request.form.get("current-password")):
                mongo.db.users.update_one(
                        {"username": request.form.get('username')},
                        {"$set": {
                            "password": generate_password_hash(request.form.get('new_password')),
                            "temp_password": get_random_string(14)}})
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


@app.route("/report_user", methods=["GET", "POST"])
def report_user():

    if session:

        user_session = mongo.db.users.find_one(
                {"username": session['user']})
                

        if request.method == 'POST':
            
            user_report = request.form.get('report-user')
            user_text = request.form.get('report-text')
            user_email = user_session['email']
            print(user_email)

            report = (user_report + " with the following message: " + user_text)

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

        flash("You need to be logged in to view this page")
    return redirect(url_for('homepage'))


@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():

    if request.method == 'POST':
        
        user_email = request.form.get('email')
        user_text = request.form.get('message-text')
        

        message = ("Thank you for sending us the following message:" +  user_text)

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
