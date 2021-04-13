from app import mail
from flask_mail import Message
from flask import (
    flash, request, session)
from main.variables.variables import change_password_link


def contact_us_mail(email):
    user_text = request.form.get('message-text')
    msg = Message('Contacting us at PuppyPlaymates',
                  html=('< p > Thank you for contacting us '
                        'with the following message:</p>'
                        '<p> %s </p>'
                        '<p>We will endevour to get back to you '
                        'within 48hr</p>'
                        '<p>The Team at PuppyPlaymates</p>' % user_text),
                  sender="thepuppyplaymates@gmail.com",
                  cc=[email],
                  recipients=["thepuppyplaymates@gmail.com"])
    mail.send(msg)
    flash("Message sent successfully")


def welcome_email():
    user_email = request.form.get('email')
    msg = Message('Welcome to Puppyplaymate',
                  html='<p>Hello  %s </p>'
                  '<p>Thank you for registering with us at PuppyPlaymates</p>'
                  '<p> We are excited to have you join us and hope you have'
                  ' success finding a playmate for your Pup!</p>'
                  ' <p>The Team at PuppyPlaymates</p>' % session[
                      'user'],
                  sender="thepuppyplaymates@gmail.com",
                  recipients=[user_email])
    mail.send(msg)


def reset_password_mail(temp_password, user_email):
    reset_message = ('<p>You look like you need to reset your password</p>'
                     '<p>This is your <b>Temporary password:</b>'
                     + temp_password
                     + ' </p>'
                     '<a href='
                     + change_password_link
                     + '>Reset Password Link</a>'
                     '<p>If you didn\'t request this email to be sent '
                     'it might be worth logging into your account and '
                     'changing your password</p>'
                     '<p>The Team at PuppyPlaymates</p>')
    msg = Message("Reset Password",
                  html=reset_message,
                  sender="thepuppyplaymates@gmail.com",
                  recipients=[user_email])
    mail.send(msg)


def report_user_mail(user_email):
    user_report = request.form.get('report-user')
    user_text = request.form.get('report-text')

    # creates a report string
    report = ('<p>You have reported'
              '<b>'
              + user_report
              + '</b></p>'
              "<p> For the following reasons: </p> "
              '<p>'
              + user_text
              + '</p>'
              'We will take a look into the users activity and'
              'take the appropriate action.</p>'
              '<p>The Team at PuppyPlaymates</p>')

    msg = Message("Report user",
                  html=report,
                  sender="thepuppyplaymates@gmail.com",
                  cc=[user_email],
                  recipients=["thepuppyplaymates@gmail.com"])
    mail.send(msg)