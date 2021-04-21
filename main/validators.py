from flask import (
    flash,
    redirect, request, url_for)
import re
from main.app_utils import profanity_check
from main.variables.variables import extentions, sizes, genders
from main.variables.flash_messages import *


password_pattern = (
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*-_#?&])([A-Za-z\d@$!%-_*#?&]{8,30})$")
username_pattern = (r"^(?=.*[A-Za-z])([a-zA-Z0-9/^\s*]){4,20}$")
email_pattern = (r'[^@]+@[^@]+\.[^@]+')
length_pattern = (
    r"^[a-zA-Z0-9~`!@#\$%\^&\*\(\)_\-\+={\[\}\]\|\\:;'<,>\.\?\/\" ]{1,1000}$")


def check_extention(file):
    """
    Checks if extention is an allowed image extention
    """
    if file not in extentions:
        flash(flash_extention)
        return True


def not_valid_password(password):
    """ Checks to see if password matches pattern
    Delivers flash message if none match
    """
    if not (re.search(password_pattern, password)):
        flash(flash_password)
        return True


def not_valid_username(username):
    """ Checks to see if username matches pattern
    """
    if not (re.search(username_pattern, username)):
        flash(flash_username)
        return True


def not_valid_email(email):
    """ Checks to see if email matches pattern
    delivers flash message
    """
    if not (re.search(email_pattern, email)):
        flash(flash_email)
        return True


def not_valid_text(text):
    """ To see if the user is only using spaces
    Delivers flash message if so
    """
    if text.isspace():
        flash(flash_spaces)
        return True


def check_length(input):
    if not (re.search(length_pattern, input)):
        flash(flash_length)
        return True


def check_input(input):
    """ take the input and checks for profanity, spaces and length
    Output is a boolean, if True wont allow data insert
    """
    if profanity_check(input):
        flash(flash_text)
        return True

    if not_valid_text(input):
        return True

    if check_length(input):
        return True


def check_size(input):
    if input not in sizes:
        return True


def check_gender(input):
    if input not in genders:
        return True


def check_text_input(input):
    if not_valid_text(input):
        return True

    if check_length(input):
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

    if check_text_input(dog_description):
        return True
    if profanity_check(dog_description):
        flash(flash_description)
        return True

    if check_text_input(human_description):
        return True
    if profanity_check(human_description):
        flash(flash_description)
        return True

    if check_text_input(dog_name):
        return True
    if profanity_check(dog_name):
        flash(flash_dogname)
        return True

    if check_text_input(human_name):
        return True
    if profanity_check(human_name):
        flash(flash_human)
        return True
    if check_length(human_name):
        return True

    if check_text_input(dog_location):
        return True
    if profanity_check(dog_location):
        flash(flash_location)
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

    if check_text_input(dog_description):
        return True
    if profanity_check(dog_description):
        flash(flash_description)
        return True

    if check_text_input(dog_name):
        return True
    if profanity_check(dog_name):
        flash(flash_dogname)
        return True

    if check_text_input(dog_location):
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

    if check_text_input(human_description):
        return True
    if profanity_check(human_description):
        flash(flash_description)
        return True

    if check_text_input(human_name):
        return True
    if profanity_check(human_name):
        flash(flash_name)
        return True

