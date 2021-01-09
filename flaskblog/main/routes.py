from flask import Blueprint, render_template
from flaskblog.models import Event
from flask_login import login_required
main = Blueprint('main', __name__)

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

@main.route("/home")
@login_required
def home():
    posts = Event.query.all()
    return render_template('home.html', posts=posts)


@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact sports club', places=places)
