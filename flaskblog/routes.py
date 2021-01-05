import os
#import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, session, request, abort
from flaskblog import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateProfileForm, CreateForm, UpdatePlaceForm
from flaskblog.models import User, Club, Sport, SportPlayed, Event, Participant
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message

available_place=[]
available_sports=[]



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

posts = [
    {
        'author': 'Marta Campra',
        'title': 'Event 1',
        'content': 'First post content',
        'date_posted': 'December 7, 2020'
    },
    {
        'author': 'Francesca Romana Calvi',
        'title': 'Event 2',
        'content': 'Second post content',
        'date_posted': 'December 8, 2020'
    }
]

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

#@app.route("/")
@app.route("/home")
@login_required
def home():
    posts = Event.query.all()
    return render_template('home.html', posts=posts)




@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    available_sports = []
    for x in Sport.query.all():
        s = (str(x.name), str(x.name).capitalize())
        available_sports.append(s)
    form.sport1.choices = available_sports
    form.sport2.choices = available_sports
    form.sport3.choices = available_sports

    if form.validate_on_submit():
        #us = SportPlayed.query.filter_by(played=current_user).all()
        #db.session.delete(us)
        #db.session.commit()

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        current_user.birthdate = form.birthdate.data

        s1 = Sport.query.filter_by(name=form.sport1.data).first()
        sport_play1 = SportPlayed(level=form.level1.data, played=current_user, sport=s1)

        s2 = Sport.query.filter_by(name=form.sport2.data).first()
        sport_play2 = SportPlayed(level=form.level2.data, played=current_user, sport=s2)

        db.session.add(sport_play1)
        db.session.add(sport_play2)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.birthdate.data = current_user.birthdate
        form.level1.data = SportPlayed.query.filter_by(level=form.level1.data).first()

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('profile.html', title='Profile',
                           image_file=image_file, form=form)

@app.route("/myevents")
@login_required
def myevents():
    posts = Event.query.filter_by(user_id = current_user.id).all()
    #pa = Participant.query.filter_by(joined=current_user).all()
    #parts = Event.query.filter_by(id=pa)

    return render_template('myevents.html', title='My Events', posts=posts)

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact sports club', places=places)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,surname=form.surname.data, birthdate= form.birthdate.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():

    available_place = []
    for c in Club.query.all():
        p = (str(c.name), str(c.name).capitalize())
        available_place.append(p)

    available_sports = []
    for x in Sport.query.all():
        s = (str(x.name), str(x.name).capitalize())
        available_sports.append(s)

    form = CreateForm()
    print('look here:')
    print(form.place.choices)
    form.place.choices=available_place
    form.sport.choices=available_sports

    if form.validate_on_submit():
        c = Club.query.filter_by(name=form.place.data).first()
        s = Sport.query.filter_by(name=form.sport.data).first()

        event = Event(date=form.date.data, time=form.time.data, cost=form.cost.data, np=form.np.data,
                      creator=current_user, place=c, sportevent=s)

        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('myevents'))

    return render_template('create.html', title='Create', form=form)



#@app.route("/update", methods=['GET', 'POST'])
#def update_place2():
 #   form=UpdatePlaceForm()
  #  p=(form.place.data, form.place.data.capitalized)
   # available_place.append(p)


@app.route("/myevents/<int:event_id>/remove", methods=['POST'])
@login_required
def remove(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been removed!', 'success')
    return redirect(url_for('myevents'))


@app.route("/home/<int:event_id>/join", methods=['POST'])
@login_required
def join(event_id):
    event = Event.query.get_or_404(event_id)
    participant = Participant(joined=current_user, part=event)
    if event.creator == current_user:
        abort(403)
        #flash('You cannot join your event.', 'success')
    db.session.add(participant)
    db.session.commit()
    flash('You have joined the event, check MyEvents!', 'success')
    return redirect(url_for('home'))


@app.route("/getplace", methods=['GET', 'POST'])
def getplace():

    for p in places:
        c= Club(name=p['name'], address=p['address'], phone=p['telephone'])
        if Club.query.filter_by(phone=p['telephone']).first():
            break
        else:
            db.session.add(c)
            db.session.commit()


    available_place=[]
    for c in Club.query.all():
        p = (str(c.name), str(c.name).capitalize())
        available_place.append(p)

    return redirect(url_for('create'))


@app.route("/getsport", methods=['GET', 'POST'])
def getsport():
    available_sports = []

    for s in sports:
        x = Sport(name=s['name'])
        if Sport.query.filter_by(name=s['name']).first():
            break
        else:
            db.session.add(x)
            db.session.commit()

    for x in Sport.query.all():
        s = (str(x.name), str(x.name).capitalize())
        available_sports.append(s)

    return redirect(url_for('create'))

