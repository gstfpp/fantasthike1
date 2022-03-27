from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, TextAreaField, PasswordField, SubmitField, IntegerField, \
    SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, InputRequired, EqualTo, NumberRange, Email, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateField
from variable import provinces


class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    remember = BooleanField('remember me')
    submit = SubmitField('login')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email(message="Email not valid")])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    phone = StringField('phone')
    language = SelectMultipleField('languages',
                                   choices=[('DE', 'German'), ('EN', 'English'), ('FR', 'French'), ('IT', 'Italian'),
                                            ('CH', 'Chinese')])
    password = PasswordField('password',
                             validators=[DataRequired()])
    professional = BooleanField('professional')
    confirm = PasswordField('confirm')
    province = StringField('province')
    profilepicture = FileField('ProfilePicture', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'],
                                                                                         message='file must be jpg, png or jpeg')])
    terms_and_condition = BooleanField('terms_and_condition')
    submit = SubmitField('Create account')


class EditData(FlaskForm):
    name = StringField('name', default=None)
    surname = StringField('surname', default=None)
    bio = TextAreaField('Bio', default=None)
    phone = StringField('phone', default=None)
    password = PasswordField('NewPassword', validators=[EqualTo('confirm', message='Passwords must match')],
                             default=None)
    confirm = PasswordField('RepeatPassword', default=None)
    language = SelectMultipleField('languages',
                                   choices=[('DE', 'German'), ('EN', 'English'), ('FR', 'French'), ('IT', 'Italian'),
                                            ('ES', 'Spanish'), ('CH', 'Chinese')], default=None)
    province = StringField('province', default=None)
    professional = BooleanField('professional', default=None)
    premium = BooleanField('premium', default=None)
    profilepicture = FileField('ProfilePicture')
    submit = SubmitField('Edit')


class Search(FlaskForm):
    province = SelectField('province', choices=provinces, default="Turin")
    submit = SubmitField('Search your new adventure!')


class Suggest(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message="This is not an email, please check again")])
    submit = SubmitField('Send')


class Feedback(FlaskForm):
    star = IntegerField(default=3,
                        validators=[DataRequired(), NumberRange(1, 5, message="Insert a number between 1 and 5")])
    review = TextAreaField('review', validators=[DataRequired()])
    submit = SubmitField('submit')


class Experience(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    province = SelectField('province', choices=provinces, validators=[DataRequired()])
    place = StringField('place', validators=[DataRequired()])
    start_date = DateField('start_date', validators=[DataRequired()])
    end_date = DateField('end_date', validators=[DataRequired()])
    price = IntegerField('price', default=0)
    submit = SubmitField('submit')


class Delete(FlaskForm):
    expid = HiddenField('expid')
    submit = SubmitField('Delete')


class searchUser(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Search')
