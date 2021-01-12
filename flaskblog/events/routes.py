from flask import Blueprint, render_template, url_for, flash, redirect, abort
from sqlalchemy import and_
from wtforms import meta

from flaskblog import db
from flaskblog.events.forms import CreateForm
from flaskblog.models import Club, Sport, Event, Participant
from flask_login import current_user, login_required

events = Blueprint('events', __name__)

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

sports = [
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


@events.route("/myevents")
@login_required
def myevents():
    posts = Event.query.filter_by(user_id=current_user.id).all()
    parts = Event.query.join(Event.participant2).filter_by(u_id=current_user.id).all()
    # pa = Participant.query.filter_by(joined=current_user).all()
    # parts = Event.query.filter_by(id=pa)

    return render_template('myevents.html', title='My Events', posts=posts, parts=parts)


@events.route("/create", methods=['GET', 'POST'])
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
    form.place.choices = available_place
    form.sport.choices = available_sports

    if form.validate_on_submit():
        c = Club.query.filter_by(name=form.place.data).first()
        s = Sport.query.filter_by(name=form.sport.data).first()

        event = Event(date=form.date.data, time=form.time.data, cost=form.cost.data, np=form.np.data,
                      level=form.level.data,
                      creator=current_user, place=c, sportevent=s)

        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('events.myevents'))

    return render_template('create.html', title='Create', form=form)




@events.route("/myevents/<int:event_id>/remove", methods=['POST'])
@login_required
def remove(event_id):
    event = Event.query.get_or_404(event_id)
    if event.creator != current_user:
        abort(403)

    pa = Participant.query.filter_by(e_id=event_id).all()
    db.session.delete(event)
    db.session.commit()
    for x in pa:
        db.session.delete(x)
        db.session.commit()


    # pr = Participant.query.get_or_404(id)
    # if Participant.e_id == None:
    # db.session.delete(pr)
    flash('Your event has been removed!', 'success')
    return redirect(url_for('events.myevents'))


@events.route("/myevents/<int:event_id>/cancel", methods=['POST'])
@login_required
def cancel(event_id):
    #parti = Participant.query.get_or_404(event_id).all()
    #parti = Participant.query.filter_by(e_id=event_id).all()
    parti= Participant.query.filter_by(u_id=current_user.id).filter_by(e_id=event_id).first()
    #if parti.joined == current_user:
    db.session.delete(parti)
    db.session.commit()

    flash('You have cancelled your participation', 'success')
    return redirect(url_for('events.myevents'))


@events.route("/home/<int:event_id>/join", methods=['POST'])
@login_required
def join(event_id):
    if Participant.query.filter_by(u_id=current_user.id).filter_by(e_id=event_id).first():
        abort(500)

    event = Event.query.get_or_404(event_id)
    participant = Participant(joined=current_user, part=event)

    if event.creator == current_user:
        abort(403)

    db.session.add(participant)
    db.session.commit()
    flash('You have joined the event, check MyEvents!', 'success')
    return redirect(url_for('main.home'))


@events.route("/getplace", methods=['GET', 'POST'])
def getplace():
    for p in places:
        c = Club(name=p['name'], address=p['address'], phone=p['telephone'])
        if Club.query.filter_by(phone=p['telephone']).first():
            break
        else:
            db.session.add(c)
            db.session.commit()

    available_place = []
    for c in Club.query.all():
        p = (str(c.name), str(c.name).capitalize())
        available_place.append(p)

    return redirect(url_for('events.create'))


@events.route("/getsport", methods=['GET', 'POST'])
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

    return redirect(url_for('events.create'))
