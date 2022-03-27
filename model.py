from flask_login._compat import text_type
from sqlalchemy import Integer, Sequence
from sqlalchemy.orm import relationship

from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, Sequence('user_id', start=1, increment=1), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return text_type(self.id)

    def get(self, id):
        return unicode(self.id)

    def __repr__(self):
        return '<Email %r>' % self.email


class UserData(db.Model):
    __tablename__ = 'userdata'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120), db.ForeignKey(User.email), unique=True, nullable=False)
    guide = db.Column(db.Boolean, default=0)
    professional = db.Column(db.Boolean, default=0)
    premium = db.Column(db.Boolean, default=0)
    province = db.Column(db.String)
    experiences = db.relationship('ExperienceDB', backref='user')
    feedback = db.relationship('FeedbackDB', backref='userdata')


class LanguagesSpoken(db.Model):
    __tablename__ = 'languagesspoken'
    id = db.Column(db.Integer, db.ForeignKey(UserData.id), primary_key=True)
    lang = db.Column(db.String(3), primary_key=True)


class FeedbackDB(db.Model):
    __tablename__ = 'feedbackDB'
    id = db.Column(db.Integer(), Sequence('feedback_id', start=1, increment=1), primary_key=True)
    sender = db.Column(db.String(), db.ForeignKey(UserData.id), nullable=False)
    receiver = db.Column(db.String(), nullable=False)
    star = db.Column(db.Integer)
    date = db.Column(db.Date)
    review = db.Column(db.String())


class ExperienceDB(db.Model):
    __tablename__ = 'experienceDB'
    id = db.Column(db.Integer(), Sequence('experience_id', start=1, increment=1), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey(UserData.id), nullable=False)
    title = db.Column(db.String(), nullable=False)
    nation = db.Column(db.String(), default="Italy")
    provinceExp = db.Column(db.String(), nullable=False)
    place = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_of_addition = db.Column(db.Date, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Integer, nullable=False)

