from flask import (
    flash,
    redirect, request, url_for)
import re
from main.app_utils import profanity_check
from main.variables.variables import extentions, sizes, genders
from main.variables.flash_messages import *


password_pattern = (
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*-_#?&])([A-Za-z\d@$!%-_*#?&]){8,30}$")
username_pattern = (r"^(?=.*[A-Za-z])[a-zA-Z0-9]{4,20}$")
email_pattern = (r'[^@]+@[^@]+\.[^@]+')


def check_extention(file):
    """ Input is a string of the file extention
    Checks if extention is an allowed image extention
    Returns boolean true if not in extention
    """
    if file not in extentions:
        flash(flash_extention)
        return True


def not_valid_password(password):
    """ Input is a string
    Checks to see if password matches pattern
    Delivers flash message if none match
    Output is a boolean of True is doesn't match
    """
    if not (re.search(password_pattern, password)):
        flash(flash_password)
        return True


def not_valid_username(username):
    """ Input is a string
    Checks to see if username matches pattern
    Output is a boolean of True is doesn't match
    """
    if not (re.search(username_pattern, username)):
        flash(flash_username)
        return True


def not_valid_email(email):
    """ Input is a string
    Checks to see if email matches pattern
    if doesnt match delivers flash message
    Output is a boolean of True is doesn't match
    """
    if not (re.search(email_pattern, email)):
        flash(flash_email)
        return True


def not_valid_text(text):
    """ Input is a string
    To see if the user is only using spaces
    If doesn't match delivers flash message
    Output is a boolean of True is doesn't match
    """
    if text.isspace():
        flash(flash_spaces)
        return True


def check_length(input, length):
    """ Takes input as string and length as interger
    Converts the length into a string and concencrates is with the pattern
    Checks to see if the input matches the pattern
    Returns a boolean of True is is doesn't match
    """
    max = str(length)
    length_pattern = (
        r"^.{1," +
        max +
        "}$")
    if not (re.search(length_pattern, input)):
        flash(flash_length)
        return True


def check_input(input, length):
    """ Take the input and checks for profanity, input and length
    Input is a string and length is an interger
    Output is a boolean, if True wont allow data insert
    """
    if profanity_check(input):
        flash(flash_text)
        return True

    if not_valid_text(input):
        return True

    if check_length(input, length):
        return True


def check_size(input):
    """ Takes input as a string
        Checks to see if the string is in sizes
        Output is a boolean of True is doesn't match
    """
    if input not in sizes:
        return True


def check_gender(input):
    """ Takes input as a string
        Checks to see if the string is in gender
        Output is a boolean of True is doesn't match
    """
    if input not in genders:
        return True


def check_text_input(input, length):
    """ Takes input string and length as interger
    passes these to the appropriate functions
    """
    if not_valid_text(input):
        return True

    if check_length(input, length):
        return True


def check_not_valid_registration():
    """ Checks fields for a valid registrations
    Passes the form details through the appropriate validators
    Checks to make sure password matches
    """
    if not_valid_username(request.form.get("username")):
        return True
    if profanity_check(request.form.get('username')):
        flash(flash_text)
        return True
    if not_valid_email(request.form.get("email")):
        return True
    if not_valid_password(request.form.get('password')):
        return True
    # checks to see if both passwords match
    if request.form['password'] != request.form['repeat-password']:
        flash(flash_repeat)
        return redirect(url_for("register"))


def check_not_valid_build():
    """ Checks fields for a valid registrations
    Passes the form details through the appropriate validators
    Checks for profanity and delievers appropriate flash messsage
    Checks to make sure password matches
    """
    dog_description = request.form.get('dog_description')
    human_description = request.form.get('human_description')
    dog_name = request.form.get('dog_name')
    human_name = request.form.get('human_name')
    dog_location = request.form.get('dog_location')
    dog_size = request.form.get('dog_size')
    dog_gender = request.form.get('dog_gender')
    dog_breed = request.form.get('dog_breed')

    if check_text_input(dog_description, 1500):
        return True
    if profanity_check(dog_description):
        flash(flash_description)
        return True

    if check_text_input(human_description, 1500):
        return True
    if profanity_check(human_description):
        flash(flash_description)
        return True

    if check_text_input(dog_name, 35):
        return True
    if profanity_check(dog_name):
        flash(flash_dogname)
        return True

    if check_text_input(human_name, 35):
        return True
    if profanity_check(human_name):
        flash(flash_human)
        return True

    if check_text_input(dog_location, 50):
        return True
    if profanity_check(dog_location):
        flash(flash_location)
        return True

    if check_text_input(dog_breed, 30):
        return True
    if profanity_check(dog_breed):
        flash(flash_profanity)
        return True

    if check_size(dog_size):
        return True

    if check_gender(dog_gender):
        return True


def check_not_valid_edit():
    """ Checks fields for a valid registrations
    Passes the form details through the appropriate validators
    Checks for profanity and delievers appropriate flash messsage
    Checks to make sure password matches
    """

    dog_description = request.form.get('dog_description')
    dog_name = request.form.get('dog_name')
    dog_location = request.form.get('dog_location')
    dog_size = request.form.get('dog_size')

    if check_text_input(dog_description, 1500):
        return True
    if profanity_check(dog_description):
        flash(flash_description)
        return True

    if check_text_input(dog_name, 30):
        return True
    if profanity_check(dog_name):
        flash(flash_dogname)
        return True

    if check_text_input(dog_location, 30):
        return True
    if profanity_check(dog_location):
        flash(flash_location)
        return True

    if check_size(dog_size):
        return True


def check_not_valid_edit_human():
    """ Checks fields for a valid registrations
    Passes the form details through the appropriate validators
    Checks for profanity and delievers appropriate flash messsage
    """
    human_description = request.form.get('human_description')
    human_name = request.form.get('human_name')

    if check_text_input(human_description, 1500):
        return True
    if profanity_check(human_description):
        flash(flash_description)
        return True

    if check_text_input(human_name, 30):
        return True
    if profanity_check(human_name):
        flash(flash_name)
        return True
