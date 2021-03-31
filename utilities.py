from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
import random
import string
import re
from datetime import date

curse_words = {"fuck", "shit", "cunt", "wanker", "fucker", "fucktard", "shitstick", "dickhead", "asshole", "dickwipe",
                   "twat", "tit", "tits", "fucktits", "wankstain", "dick"}

def profanity_check(input):
    for word in input.split():
        if word in curse_words:
            print(word)
            return True


def check_age(dob):
    today = date.today()
    age = today.year - dob.year - \
        ((today.month, today.day) < (dob.month, dob.day))
    return age


def check_birthday(dob):
    today = date.today()
    if ((today.month, today.day) == (dob.month, dob.day)):
        return True


def get_random_string(length):
    items = string.ascii_letters
    result_str = ''.join(random.choice(items) for i in range(length))
    return result_str


def valid_password(password):
    if not (re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*-_#?&])([A-Za-z\d@$!%-_*#?&]{8,30})$", password)):
        return True


def valid_username(username):
    if not (re.search(r"^(?=.*[A-Za-z])([a-zA-Z0-9!?/][^\s*]){4,20}$", username)):
        return True
 

def valid_email(email):
    if not (re.search(r'[^@]+@[^@]+\.[^@]+', email)):
        return True


def valid_text(text):
    if text.isspace():
        flash("Text fields must include characters")
        return True


def valid_date(date):
    return True


def check_input(input):
    if profanity_check(input):
        flash("This text violates our safe spaces policy, please refrain from using profanity")
        return True
    if valid_text(input):
        return True


def check_valid_registration():
    # checked to make sure valid before passing into the database
    if valid_username(request.form.get("username")):
        flash("This is not a valid username")
        return True
    if profanity_check(request.form.get('username')):
        flash(
            "This username violates our safespaces policy, please refrain from using profanity")
        return True
    if valid_email(request.form.get("email")):
        flash("This is not a valid email")
        return True
    if valid_password(request.form.get('password')):
        flash("This is not a valid password")
        return True

    # checks to see if both passwords match
    if request.form.get('password') != request.form('repeat-password'):
        flash("Passwords did not match, please try again")
        return True


def check_valid_build():
    # Checks for valid input and profanity
    if valid_text(request.form.get('dog_description')):
        return True
    if profanity_check(request.form.get('dog_description')):
        flash(
            "This description violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('human_description')):
        return True
    if profanity_check(request.form.get('human_description')):
        flash(
            "This description violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('dog_name')):
        return True
    if profanity_check(request.form.get('dog_name')):
        flash(
            "Did you really call your dog that? That name violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('human_name')):
        return True
    if profanity_check(request.form.get('human_name')):
        flash(
            "Are you really called that? That name violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('dog_location')):
        return True
    if profanity_check(request.form.get('dog_location')):
        flash(
            "Please refrain from using profanity and use a real location")
        return True
        

def check_valid_edit():
    # Checks for valid input and profanity
    if valid_text(request.form.get('dog_description')):
        return True
    if profanity_check(request.form.get('dog_description')):
        flash(
            "This description violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('dog_name')):
        return True
    if profanity_check(request.form.get('dog_name')):
        flash(
            "Did you really call your dog that? That name violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('dog_location')):
        return True
    if profanity_check(request.form.get('dog_location')):
        flash(
            "Please refrain from using profanity and use a real location")
        return True


def check_valid_edit_human():
    # Checks for valid input and profanity

    if valid_text(request.form.get('human_description')):
        return True
    if profanity_check(request.form.get('human_description')):
        flash(
            "This description violates our safespaces policy, please refrain from using profanity")
        return True

    if valid_text(request.form.get('human_name')):
        return True
    if profanity_check(request.form.get('human_name')):
        flash(
            "Are you really called that? That name violates our safespaces policy, please refrain from using profanity")
        return True


