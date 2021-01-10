import os
from PIL import Image
from flask import render_template

from flaskblog import app
from flask_mail import Mail, Message


def save_picture(form_picture):
    fname, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = fname + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    output_size = (325, 325)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # mail
app.config['MAIL_PORT'] = 465  # 587
app.config['MAIL_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']

mailobject = Mail(app)
#EMAIL_USERNAME=gruppo21.2020@gmail.com;EMAIL_PASSWORD=Gruppo212020

# s= URLSafeTimedSerializer('Thisisasecret!')

def send_mail(to, subject, template, **kwargs):
    msg = Message(subject,
                  recipients=[to],
                  sender=app.config['MAIL_USERNAME'])
    # print (msg)
    msg.html = render_template(template + '.html', **kwargs)
    mailobject.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.html = render_template('reset_mail.html', token=token, _external=True)
    mailobject.send(msg)


