import random
import string
from datetime import date
from main.variables.variables import curse_words


def profanity_check(input):
    for word in input.split():
        if word in curse_words:
            print(word)
            return True


def check_age(dob):
    if not dob == "":
        today = date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
    else:
        age = ""
    return age


def check_birthday(dob):
    if not dob == "":
        today = date.today()
        if ((today.month, today.day) == (dob.month, dob.day)):
            return True


def get_random_string(length):
    items = string.ascii_letters
    result_str = ''.join(random.choice(items) for i in range(length))
    return result_str


def dog_liker(user_profile, user_session):
    for dogs_like in user_profile["dog_liker"]:  # check if has liked page
        if 'user' in dogs_like:
            liker_id = dogs_like['user']
            if user_session["_id"] == liker_id:
                return True  # changes like button to unlike

