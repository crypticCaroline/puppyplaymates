import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_mail import Mail
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api
import time
from datetime import date, datetime
from main.mail import *
from main.app_utils import *
from main.validators import *
from main.variables.variables import (cloudinary_url, default_image_url)
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


@app.route("/playmates")
def playmates():
    """ Finds all users within the database
    and returns them to be displayed on the playmates page
    """
    users = mongo.db.users.find()
    return render_template("playmates.html", users=users)


@ app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """ Profile page
    Finds the profile from the username returns - user_profile
    If the profile is not found user is redirect to profile_not_found.html
    Finds user from the session['user'] cookie - returns user_session
    If user not in session directs to login.html
    The age function is called and check dob - returns age
    The birthday function is called checked from the dob - returns boolean
    The session user is checked if a liker of profile - returns boolean
    If the like/unlike button is pressed the like/unlike functions are called
    """

    if session:
        user_profile = mongo.db.users.find_one({"username": username})
        if not user_profile:
            return render_template('profile_not_found.html')

        user_session = mongo.db.users.find_one({"username": session['user']})
        dog_dob = user_profile['dog_dob']
        dog_liked = False

        age = check_age(dog_dob)
        birthday = check_birthday(dog_dob)
        dog_liked = dog_liker(user_profile, user_session)

        if request.method == "POST":
            liker_btn = request.form.get("liker_btn")
            unliker_btn = request.form.get("unliker_btn")
            if liker_btn:
                return redirect(url_for(
                    'likes',
                    username=username))

            if unliker_btn:
                return redirect(url_for(
                    'dislikes',
                    username=username))

        return render_template(
            "profile.html",
            username=username,
            user_profile=user_profile,
            user_session=user_session,
            dog_liked=dog_liked,
            birthday=birthday,
            age=age)

    flash(flash_login)
    return redirect(url_for('login'))


# registration pages
@app.route("/register", methods=["GET", "POST"])
def register():
    """ Checks to see if all fields are valid
    Checkes to see if the username or email address are taken
    If they are flash message to show already exists
    Gets infomation from the user inputs and creates a document
    Adds a session cookie so user is now logged in
    User is sent a welcome email
    Redirected to build profile at the end
    """

    if request.method == "POST":
        if check_not_valid_registration():
            return redirect(url_for("register"))

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            flash(flash_username_exists)
            return redirect(url_for("register"))
        if existing_email:
            flash(flash_email_registered)
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "image_url": default_image_url,
            "dog_name": "",
            "dog_description": "",
            "dog_breed": "",
            "dog_gender": "",
            "dog_location": "",
            "dog_size": "",
            "dog_dob": "",
            "puppy_love": False,
            "fertile": False,
            "human_name": "",
            "human_description": "",
            "dog_liker": [],
            "all_images": [],
            "comments": [],
            "next_walk": {
                'date': "",
                'time': "",
                'place': "",
                'walk_description': ""
            }}

        mongo.db.users.insert_one(register)  # inserts new user into database
        session["user"] = request.form.get("username")  # adds 'session' cookie
        welcome_email()  # sends user a welcome email

        return redirect(url_for("build_profile",
                                username=session["user"]))
    return render_template("register.html")


@app.route("/build_profile/<username>", methods=["GET", "POST"])
def build_profile(username):
    """ Finds the users details
    will use the useres details to fill out the input fields if they exist
    Users the dog_dob to set the current datepicker value
    when posted get the details from the forms
    configures the date to match the schema
    checks to make sure valid input
    if valid sends to database and sends user to their profile page
    """
    if session:
        user = mongo.db.users.find_one(
            {"username": session['user']})  # finds user
        dog_dob = user['dog_dob']  # finds user dob for date picker
        if not (dog_dob == ""):
            user_dog_dob = dog_dob.date()
        else:
            user_dog_dob = ""

        if request.method == "POST":  # updates the database with dog details
            if check_not_valid_build():
                return render_template("build_profile.html",
                                       username=session[
                                           "user"],
                                       user=user)

            dob = datetime.strptime(request.form.get("dog_dob"), "%Y-%m-%d")
            fertile = request.form.get("fertile")
            if fertile == "on":
                fertile = True
            else:
                fertile = False
            puppy_love = request.form.get("puppy_love")
            if puppy_love == "on":
                puppy_love = True
            else:
                puppy_love = False

            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {
                    "dog_name": request.form.get("dog_name"),
                    "dog_description": request.form.get("dog_description"),
                    "dog_breed": request.form.get("dog_breed"),
                    "dog_gender": request.form.get("dog_gender"),
                    "dog_location": request.form.get("dog_location"),
                    "dog_size": request.form.get("dog_size"),
                    "dog_dob": dob,
                    "puppy_love": puppy_love,
                    "fertile": fertile,
                    "human_name": request.form.get("human_name"),
                    "human_description": request.form.get("human_description")
                }}
            )
            return redirect(url_for("profile",
                                    username=session["user"]))
        return render_template("build_profile.html",
                               username=session["user"],
                               user=user,
                               user_dog_dob=user_dog_dob)
    flash(flash_login)
    return render_template("login.html")


# login
@ app.route("/login", methods=["GET", "POST"])
def login():
    """ Checks if existing username or email
    If the password matches username or email will assign session cookie
    If it doesn't match user will get a flash message
    """

    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get('username')})

        if existing_user:
            # ensure hash matches then logs user in
            if check_password_hash(
                    existing_user["password"],
                    request.form.get("password")):
                session["user"] = request.form.get("username")
                return redirect(url_for("profile",
                                        username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        elif existing_email:
            if check_password_hash(
                    existing_email["password"], request.form.get("password")):
                session["user"] = existing_email["username"]
                return redirect(url_for(
                    "profile",
                    username=session["user"]))
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
    """ Passes querys from form
    searches the Database index for matching criteria
    """
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("playmates.html", users=users)


# log the user out
@ app.route("/logout")
def logout():
    """ Removes session cookie and tells user they are logged out
    """
    session.pop("user")
    flash(flash_logout)
    return redirect(url_for("login"))


# edit pages
# edit dog
@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username):
    """ Finds users dog profile and add info to input fields
    Users can only edit their own profiles
    Checks to make sure userinputs are valid
    formats data prior to being added to the datebase
    Updates database accordingly and redirect user back to profile
    """
    if session:
        user_profile = mongo.db.users.find_one({"username": session['user']})

        # lets users change some details of their dog
        if request.method == "POST":
            if check_not_valid_edit():
                return redirect(url_for("profile",
                                        username=session["user"]))

            fertile = request.form.get("fertile")
            if fertile == "on":
                fertile = True
            else:
                fertile = False

            puppy_love = request.form.get("puppy_love")
            if puppy_love == "on":
                puppy_love = True
            else:
                puppy_love = False

            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {
                    "dog_name": request.form.get("dog_name"),
                    "dog_description": request.form.get("dog_description"),
                    "dog_location": request.form.get("dog_location"),
                    "dog_size": request.form.get("dog_size"),
                    "puppy_love": puppy_love,
                    "fertile": fertile
                }}
            )
            return redirect(url_for("profile",
                                    username=session["user"]))
        return render_template("edit_profile.html",
                               username=session["user"],
                               user_profile=user_profile)
    flash(flash_login)                           
    return render_template("login.html")


# edit human
@app.route("/edit_human/<username>", methods=["GET", "POST"])
def edit_human(username):
    """ Finds users human profile and add info to input fields
    Users can only edit their own profiles
    Checks to make sure userinputs are valid
    Updates database accordingly and redirect user back to profile
    """
    if session:
        user_profile = mongo.db.users.find_one({"username": username})

        # edits human details in database
        if request.method == "POST":
            if check_not_valid_edit_human():
                return redirect(url_for("profile",
                                        username=session["user"]))

            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {
                    "human_name": request.form.get("human_name"),
                    "human_description": request.form.get("human_description")
                }}
            )
            return redirect(url_for("profile",
                                    username=session["user"]))
        return render_template("edit_human.html",
                               username=session["user"],
                               user_profile=user_profile)
    return render_template("homepage.html")


# uploads images to database
@app.route("/edit_images/<username>/upload/", methods=["GET", "POST"])
def upload_image(username):
    """ Allows user to add an image
    When the users submits the file it checks for allowed extentions
    It then creates a string from the filename and extention
    The image is uploaded to cloudinary
    An image URL is created using the cludinary url + filename + extention
    The image url is added to the database
    If not session user is directed back to login page
    """
    if session:
        if request.method == 'POST':
            # get file from form
            for item in request.files.getlist("image_file"):
                # creates a string for the file name to upload to cloudinary
                filename = secure_filename(item.filename)
                filename, file_extension = os.path.splitext(filename)
                public_id = (username + '/q_auto:low/' + filename)
                if check_extention(file_extension):
                    return redirect(url_for('profile',
                                            username=session['user']))

                # uploads to cloudinary
                cloudinary.uploader.unsigned_upload(
                    item,
                    "puppy_image",
                    cloud_name='puppyplaymate',
                    folder='/user_images/',
                    public_id=public_id)
                # sets a url for image to be saved to the database
                image_url = (
                    cloudinary_url
                    + public_id
                    + file_extension)
                # adds the url to the database
                mongo.db.users.update_one(
                    {"username": session["user"]},
                    {"$addToSet": {"all_images": image_url}})
                # if the profile box is checked it will be set as the profile
                if request.form.get('profile_check'):
                    mongo.db.users.update_one(
                        {"username": session["user"]},
                        {"$set": {"image_url": image_url}})
            return redirect(url_for('profile',
                                    username=username))
        return render_template("edit_images.html",
                               username=username)
    flash("You need to be logged in to view this page")
    return render_template('login.html')


# edit images
@app.route("/edit_images/profile_photo/<username>", methods=["GET", "POST"])
def profile_photo(username):
    """ Allows user to set the profile picture from the selected photo
    If not session redirects to login
    """
    if session:
        # finds instance in datebase to set the profile picture
        user_profile = mongo.db.users.find_one({"username": username})
        if request.method == 'POST':
            mongo.db.users.update_one(
                {"username": session["user"]},
                {"$set": {"image_url": request.form.get('photo')}})
            return redirect(url_for('profile',
                                    username=username))
        return render_template("profile.html",
                               username=session["user"],
                               user_profile=user_profile)
    flash("You need to be logged in to view this page")
    return render_template("login.html")


# deletes images
@app.route("/delete_images/<username>", methods=["GET", "POST"])
def delete_images(username):
    """ Allows user to set the delete  picture from the selected photo
    If not session redirects to login
    """
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


# lets the user add a walk to their profile
@app.route("/profile/<username>/add_walk", methods=["GET", "POST"])
def add_walk(username):

    if session:
        user_profile = mongo.db.users.find_one({"username": username})

        if request.method == "POST":
            if check_input(request.form.get(
                'walk_description')) or check_input(
                    request.form.get('place')):
                return redirect(url_for("profile", username=username))
            # updates the users walk details in the database

            mongo.db.users.update_one(
                {"username": username},
                {"$set": {
                 "next_walk": {
                     'date': datetime.strptime(
                         request.form.get(
                             "walk_date"), "%Y-%m-%d"),
                     'time': request.form.get('time'),
                     'place': request.form.get('place'),
                     'walk_description': request.form.get(
                         'walk_description')
                 }}})
            return redirect(url_for('profile', username=username))
        return render_template("add_walk.html", username=session[
            "user"], user_profile=user_profile)
    flash("You need to logged in to view this page")
    return redirect(url_for('login'))


# Comments
# Adds a comment to the users profile
@app.route("/profile/<username>/comment", methods=["GET", "POST"])
def add_comment(username):

    if session:
        user_session = mongo.db.users.find_one({"username": session['user']})

        # Adds a comment to the users profile
        if request.method == "POST":
            if check_input(request.form.get('add_comment')):
                return redirect(url_for("profile", username=username))

            mongo.db.users.update_one(
                {"username": username},
                {"$addToSet": {"comments": {
                    '_id': ObjectId(),
                    'date': datetime.now().strftime("%d/%m/%Y, %H:%M"),
                    'author': user_session['username'],
                    'author_dog': user_session['dog_name'],
                    'text': request.form.get('add_comment'),
                    "img_url": user_session['image_url'],
                    'private': request.form.get('private')
                }}})
            return redirect(url_for('profile', username=username))

    flash("You need to logged in to view this page")
    return redirect(url_for('login'))


# edits comment
@app.route("/profile/<username>/edit_comment/<comment_id>",
           methods=["GET", "POST"])
def edit_comment(username, comment_id):

    if session:
        user_session = mongo.db.users.find_one({"username": session['user']})

        # lets the user edit the comment
        if request.method == "POST":
            if check_input(request.form.get('edit_comment')):
                return redirect(url_for("profile", username=username))

            mongo.db.users.update_one(
                {"username": username},
                {"$pull": {"comments": {"_id": ObjectId(comment_id)}}})

            mongo.db.users.update_one(
                {"username": username},
                {"$addToSet": {"comments":
                               {"_id": ObjectId(comment_id),
                                'date':
                                datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                'author': user_session['username'],
                                'author_dog': user_session['dog_name'],
                                'text': request.form.get('edit_comment'),
                                "img_url": user_session['image_url'],
                                'private': request.form.get('private')
                                }}})
        return redirect(url_for('profile', username=username))
    flash("You need to logged in to view this page")
    return redirect(url_for('login'))


# deletes comment
@app.route("/profile/<username>/delete_comment/<comment_id>",
           methods=["GET", "POST"])
def delete_comment(username, comment_id):

    if session:
        # removes the comment from the database
        if request.method == "POST":
            mongo.db.users.update_one(
                {"username": username},
                {"$pull": {"comments": {"_id": ObjectId(comment_id)}}})

        return redirect(url_for('profile', username=username))
    flash("You need to logged in to view this page")
    return redirect(url_for('login'))


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
    flash("You need logged in to view this page")
    return redirect(url_for('homepage'))


# mail
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():

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
            reset_password_mail(temp_password, user_email)

            return render_template("reset_sent.html")
        else:
            flash(
                'Incorrect Username and/or Password,'
                'if you have forgotten your password you can reset it')
    return render_template("reset_password.html")


# change password section
@app.route("/change_password", methods=["GET", "POST"])
def change_password():

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
                existing_user["password"], request.form.get(
                    "current-password")) or check_password_hash(
                existing_user["temp_password"],
                    request.form.get("current-password")):
                # inserts password to database and assigns a new temp password
                mongo.db.users.update_one(
                    {"username": request.form.get('username')},
                    {"$set": {
                        "password": generate_password_hash(
                            request.form.get('new-password')),
                        "temp_password": generate_password_hash(
                            get_random_string(14))}})
                session["user"] = request.form.get("username")
                return redirect(url_for(
                    "profile", username=session["user"]))

            # ensures the hash matches if the user is using the temp password
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("change_password"))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("change_password"))
    return render_template("change_password.html")


# reprt user
@app.route("/report_user", methods=["GET", "POST"])
def report_user():

    if request.method == 'POST':
        # gets the users deatils and report
        user_session = mongo.db.users.find_one({"username": session['user']})
        user_email = user_session['email']

        if check_input(request.form.get('report-user')) or check_input(
            request.form.get('report-text')):
            return redirect(url_for("report_user"))

        # sends email to company owners and ccs in reporter
        report_user_mail(user_email)

        flash("Message Sent")
        return render_template("report_user.html")
    return render_template("report_user.html")


# contact form
@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():

    if request.method == 'POST':
        if session:
            user_email = mongo.db.users.find_one(
                {"username": session['user']})['email']
        else:
            user_email = request.form.get('email')

        if not_valid_email(user_email) or check_input(
                request.form.get('message-text')):
            return redirect(url_for("contact_us"))

        contact_us_mail(user_email)

        return render_template("contact_us.html")
    return render_template("contact_us.html")


# error handlers
@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
