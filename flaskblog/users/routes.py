from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_user.forms import ResetPasswordForm

from flaskblog import bcrypt, db
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, AddSport, RequestResetForm
from flaskblog.models import User, Sport, SportPlayed
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_mail, send_reset_email

users = Blueprint('users', __name__)

available_place = []
available_sports = []

places = [
    {
        'name': 'Centro Sportivo Robilant',
        'address': 'Piazza Robilant 16, Torino (TO), 10141',
        'telephone': '011 385 0763'

    },
    {
        'name': 'Monviso Sporting Club',
        'address': 'Corso Giuseppe Allamano, 25, Grugliasco (TO), 10095',
        'telephone': '011 788 034'
    },
    {
        'name': 'Royal Club',
        'address': 'Piazza Muzio Scevola,2, Torino (TO), 10133',
        'telephone': '011 661 8432'
    },
    {
        'name': 'Master Club 2.0',
        'address': 'Corso Moncalieri 494, Torino (TO), 10133',
        'telephone': '011 661 0963'
    },
    {
        'name': 'Esperia Torino',
        'address': 'Corso Moncalieri,2, Torino(TO), 10131',
        'telephone': '011 819 3013'
    }
]

sports=[
    {
        'name': 'Basketball'
    },
    {
        'name': 'Beachvolley'
    },
    {
        'name': 'Football'
    },
    {
        'name': 'Padel'
    },
    {
        'name': 'Tennis'
    }
]


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,surname=form.surname.data, birthdate= form.birthdate.data, email=form.email.data, password=hashed_password)
        send_mail(form.email.data,
                  'You have registered succesfully',
                  'mail',
                  name=form.name.data,
                  username=form.email.data,
                  password=form.password.data
                  )

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)





@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/", methods=['GET', 'POST'])
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        current_user.birthdate = form.birthdate.data


        #s1 = Sport.query.filter_by(name=form.sport1.data).first()
        #sport_play1 = SportPlayed(level=form.level1.data, played=current_user, sport=s1)
        #db.session.add(sport_play1)
        #db.session.add(sport_play2)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.birthdate.data = current_user.birthdate
        #form.level1.data = SportPlayed.query.filter_by(level=form.level1.data).first()

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    form2 = AddSport()

    available_sports = []
    for x in Sport.query.all():
        s = (str(x.name), str(x.name).capitalize())
        available_sports.append(s)
    form2.sport1.choices = available_sports

    if form2.validate_on_submit():

        s1 = Sport.query.filter_by(name=form2.sport1.data).first()
        sport_play1 = SportPlayed(level=form2.level1.data, played=current_user, sport=s1)

        sp= SportPlayed.query.filter_by(u_id=current_user.id).filter_by(s_id=s1.id).first()
        if sp:
            db.session.update()
            db.session.commit()

        db.session.add(sport_play1)
        db.session.commit()

        flash('Sport has been added!', 'success')
        return redirect(url_for('users.profile'))

    sportp = SportPlayed.query.filter_by(u_id = current_user.id).all()
    return render_template('profile.html', title='Profile',
                           image_file=image_file, form=form, sportp=sportp, form2=form2)
