from flask import (
    flash,
    redirect, request, url_for)
import re
from main.app_utils import profanity_check
from main.variables.variables import extentions
from main.variables.flash_messages import *


password_pattern = (
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*-_#?&])([A-Za-z\d@$!%-_*#?&]{8,30})$")
username_pattern = (r"^(?=.*[A-Za-z])([a-zA-Z0-9/^\s*]){4,20}$")
email_pattern = (r'[^@]+@[^@]+\.[^@]+')


def check_extention(file):
    if file not in extentions:
        flash(flash_extention)
        return True


def not_valid_password(password):
    if not (re.search(password_pattern,
                      password)):
        return True


def not_valid_username(username):
    if not (re.search(username_pattern, username)):
        return True


def not_valid_email(email):
    if not (re.search(email_pattern, email)):
        flash(flash_email)
        return True


def not_valid_text(text):
    if text.isspace():
        flash(flash_spaces)
        return True


def check_input(input):
    if profanity_check(input):
        flash(
            flash_text)
        return True
    if not_valid_text(input):
        return True


def check_not_valid_registration():
    # checked to make sure valid before passing into the database
    if not_valid_username(request.form.get("username")):
        flash(flash_username)
        return True
    if profanity_check(request.form.get('username')):
        flash(
            flash_text)
        return True
    if not_valid_email(request.form.get("email")):
        return True
    if not_valid_password(request.form.get('password')):
        flash(flash_password)
        return True

    # checks to see if both passwords match
    if request.form['password'] != request.form['repeat-password']:
        flash(flash_repeat)
        return redirect(url_for("register"))


def check_not_valid_build():
    # Checks for valid input and profanity
    if not_valid_text(request.form.get('dog_description')):
        return True
    if profanity_check(request.form.get('dog_description')):
        flash(flash_description)
        return True

    if not_valid_text(request.form.get('human_description')):
        return True
    if profanity_check(request.form.get('human_description')):
        flash(flash_description)
        return True

    if not_valid_text(request.form.get('dog_name')):
        return True
    if profanity_check(request.form.get('dog_name')):
        flash(flash_dogname)
        return True

    if not_valid_text(request.form.get('human_name')):
        return True
    if profanity_check(request.form.get('human_name')):
        flash(flash_human)
        return True

    if not_valid_text(request.form.get('dog_location')):
        return True
    if profanity_check(request.form.get('dog_location')):
        flash(flash_location)
        return True


def check_not_valid_edit():
    # Checks for valid input and profanity
    if not_valid_text(request.form.get('dog_description')):
        return True
    if profanity_check(request.form.get('dog_description')):
        flash(flash_description)
        return True

    if not_valid_text(request.form.get('dog_name')):
        return True
    if profanity_check(request.form.get('dog_name')):
        flash(flash_dogname)
        return True

    if not_valid_text(request.form.get('dog_location')):
        return True
    if profanity_check(request.form.get('dog_location')):
        flash(flash_location)
        return True


def check_not_valid_edit_human():
    # Checks for valid input and profanity

    if not_valid_text(request.form.get('human_description')):
        return True
    if profanity_check(request.form.get('human_description')):
        flash(flash_description)
        return True

    if not_valid_text(request.form.get('human_name')):
        return True
    if profanity_check(request.form.get('human_name')):
        flash(flash_name)
        return True
