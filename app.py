from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import pymysql

from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://rawlings:1234@localhost:8889/char_user'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.fatcow.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEBUG'] = False
app.config['MAIL_SUPPRESS_SEND'] = True
app.config['TESTING'] = False


db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Char(db.Model):
    __tablename__ = 'char'
    id = db.Column(db.Integer, primary_key=True)
    charname = db.Column(db.String(60), nullable=False)
    level = db.Column(db.Integer, default=1)
    pclass = db.Column(db.String(36), nullable=False)
    strength = db.Column(db.Integer, default=10)
    constition = db.Column(db.Integer, default=10)
    dexterity = db.Column(db.Integer, default=10)
    wisdom = db.Column(db.Integer, default=10)
    intelligence = db.Column(db.Integer, default=10)
    charisma = db.Column(db.Integer, default=10)

    def __repr__(self):
        return '<Char {}>'.format(self.charname)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(60), unique=True, nullable=False)
    last = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Profile {}>'.format(self.username)


class NewChar(FlaskForm):
    #new character form.
    charname = StringField('Character Name', validators=[DataRequired()])
    charclass = SelectField('Select Class',
                            choices=[('barb', 'Barbarian'), ('bard', 'Bard'), ('cleric', 'Cleric',), ('druid', 'Druid'),
                                     ('fighter', 'Fighter'), ('monk', 'Monk'), ('paladin', 'Paladin'),
                                     ('ranger', 'Ranger'), ('rogue', 'Rogue'), ('sorcerer', 'Sorcerer'),
                                     ('warlock', 'Warlock'), ('wizard', 'Wizaed')], validators=[DataRequired()])
    charalign = SelectField('Alignment',
                            choices=[('alignlg', 'Lawful Good'), ('alignng', 'Neutral Good'),
                                     ('aligncg', 'Chaotic Good',), ('alignng', 'Lawful Neutral'),
                                     ('alignTN', 'True Neutral'), ('aligncn', 'Chaotic Neutral',),
                                     ('alignle', 'Lawful Evil'), ('alignne', 'Neutral Evil'),
                                     ('alignce', 'Chaotic Evil',)])
    charrace = SelectField('Select Class',
                           choices=[('dborn', 'Dragonborn'), ('hdwarf', 'Dwarf, Hill'), ('mdwarf', 'Dwarf, Mountain'),
                                    ('helf', 'Elf, High'), ('welf', 'Elf, Wood'), ('fgnome', 'Gnome, Forest'),
                                    ('rgnome', 'Gnome, Rock'), ('lhalf', 'Halfling, lightfoot'),
                                    ('shalf', 'Halfling, Stout'), ('helf', 'Half Elf'), ('horc', 'Half Orc'),
                                    ('human', 'Human'), ('tief', 'Tiefling')], validators=[DataRequired()])
    charbkgrd = SelectField('Select Class',
                            choices=[('acolyte', 'Acolyte',), ('charlatan', 'Charlatan'), ('criminal', 'Criminal'),
                                     ('entertainer', 'Entertainer'), ('fhero', 'Folk Hero'),
                                     ('gartisan', 'Guild Artisan'), ('hermit', 'Hermit'), ('nobel', 'Nobel'),
                                     ('outlander', 'Outlander'), ('sage', 'Sage'), ('sailor', 'Sailor'),
                                     ('soldier', 'Soldier'), ('urchin', 'Urchin')], validators=[DataRequired()])
    charlevel = StringField('Character Level', default='01', validators=[DataRequired()])
    submit = SubmitField('Submit')


# New user form
class NewUser(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    useremail = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')


# New user form
class ManualStats(FlaskForm):
    strength = IntegerField('Strength', validators=[DataRequired()])
    constition = IntegerField('Constition', validators=[DataRequired()])
    dexterity = IntegerField('Dexterity', validators=[DataRequired()])
    intelligence = IntegerField('Intelligence', validators=[DataRequired()])
    wisdom = IntegerField('Wisdom', validators=[DataRequired()])
    charisma = IntegerField('Charisma', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    msg = Message("Hello", sender='dev@rawlings.site', recipients=['c.d.rawlings@gmail.com'])
    msg.body = 'this is the test message'
    mail.send(msg)
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/new_user')
def newuser():
    form = NewUser()
    return render_template('user.html', title='New user', form=form)


@app.route('/new_character')
def newchar():
    form = NewChar()
    return render_template('new_char.html', title='New charatcter', form=form)


@app.route('/manual_enter')
def manual():
    form = ManualStats()
    return render_template('manual.html', title='Manually enter stats', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
