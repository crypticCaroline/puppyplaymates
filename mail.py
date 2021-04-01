import os
from app import app, mail
from flask_mail import Mail, Message
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)


def contact_us_mail(email):
    user_text = request.form.get('message-text')

    message = ("Thank you for sending us the following message:" + user_text)

    # sends email to user
    msg = Message("Thank you for contacting us",
                  html="<p> %s </p><p>We will endevour to get back to you within 48hr</p> <p>The Team at PuppyPlaymates</p>" % message,
                  sender="thepuppyplaymates@gmail.com",
                  cc=[email],
                  recipients=["thepuppyplaymates@gmail.com"])
    
    mail.send(msg)
    flash("Message sent successfully")


def welcome_email():
    user_email = request.form.get('email')
    print(user_email)
    print(session['user'])
    msg = Message("Welcome to Puppyplaymates",
                  html="<p>Hello  %s </p><p>Thank you for registering with us at PuppyPlaymates.</p><p>We are excited to have you join us and hope you have success finding a playmate for your Pup!</p> <p>The Team at PuppyPlaymates</p>" % session[
                      'user'],
                  sender="thepuppyplaymates@gmail.com",
                  recipients=[user_email])
    mail.send(msg)


def reset_password_mail(temp_password, user_email):
    msg = Message("Reset Password",
                  html="<p>You look like you need to reset your password</p><p>This is your <b>Temporary password:</b> %s </p><a href='https://8080-bronze-catfish-6qabji6o.ws-eu03.gitpod.io/change_password'>Reset Password Link</a><p>If you didn't request this email to be sent it might be work logging into your account and changing your password</p><p>The Team at PuppyPlaymates</p>" % temp_password,
                  sender="thepuppyplaymates@gmail.com",
                  recipients=[user_email])
    mail.send(msg)


def report_user_mail(user_email):
    user_report = request.form.get('report-user')
    user_text = request.form.get('report-text')

    # creates a report string
    report = (user_report + " with the following message: " + user_text)

    msg = Message("Report user",
                  html="<p>You have reported %s We will take a look into the users activity and take the appropriate action. <p>The Team at PuppyPlaymates</p>" % report,
                  sender="thepuppyplaymates@gmail.com",
                  cc=[user_email],
                  recipients=["thepuppyplaymates@gmail.com"])
    mail.send(msg)
