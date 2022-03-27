import os

from flask import Flask, render_template, redirect, session, url_for, request, flash, abort
from flask_bcrypt import bcrypt, generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import delete, update, distinct, select
#from sqlalchemy.orm import load_only
#from werkzeug.urls import url_parse
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime
from flask_mail import Mail, Message
from sqlalchemy import desc, asc

from variable import password_check, msg_suggestion, msg_signup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afsdlmafmamowe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + "/static"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'fantasthike@gmail.com'
app.config['MAIL_PASSWORD'] = 'ISGROUP32'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
my_API_key = "AIzaSyDZWx-eBhOJVDF6rkoXHyff0Nkh81zkOZY"

from model import User, UserData, FeedbackDB, LanguagesSpoken, ExperienceDB
from form import Search, RegistrationForm, LoginForm, Feedback, EditData, Suggest, Experience, Delete, searchUser


@app.before_first_request
def setup_db():
    # db.drop_all()
    # session.clear()
    # logout_user()
    db.create_all()
    session['profile'] = None


@login_manager.user_loader
def load_user(id):
    try:
        return User.query.filter(User.id == id).first()
    except:
        return None


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@app.route('/', methods=['GET', 'POST'])
def index():
    personalData = None
    if current_user.is_authenticated:
        personalData = UserData.query.filter_by(id=current_user.id).first()
    form = Search()
    formUsername = searchUser()
    exp_suggestion = ExperienceDB.query.order_by(desc(ExperienceDB.date_of_addition)).limit(3)
    exp_number = exp_suggestion.count()
    if formUsername.validate_on_submit():
        username = formUsername.username.data.lower()
        userSearched = UserData.query.filter_by(username=username).first()
        if userSearched:
            return redirect(url_for('profile', username=username))
        else:
            flash('username not valid, check if you typed it right', category='usernameError')
            return redirect(url_for('index') + '#usersearch')
    if form.validate_on_submit():
        province = form.province.data
        return redirect(url_for('search', province=province.capitalize()))
    return render_template('index.html', form=form, personalData=personalData, exp_number=exp_number,
                           exp_suggestion=exp_suggestion, formuser=formUsername)


@app.route('/profileid/<id>', methods=['GET', 'POST'])
def profile_by_id(id):
    personal = User.query.filter_by(id=id).first()
    if not personal:
        abort(404)
    personalData = UserData.query.filter_by(id=id).first()
    return redirect(url_for('profile', username=personalData.username))


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if not current_user.is_authenticated:
        flash("You can access personal profiles only if you are subscribed, please log in before retrying.",
              category="accessprofile")
        session['profile'] = username
        return redirect(url_for('login'))
    me = False
    form = Feedback()
    formexp = Experience()
    formdelete = Delete()
    today = datetime.date.today()
    userdata = UserData.query.filter_by(username=username).first()
    if not userdata:
        flash('Profile not founded')
        abort(404)
    user = User.query.filter_by(id=userdata.id).first()
    lang = LanguagesSpoken.query.filter_by(id=userdata.id).all()
    if current_user.is_authenticated:
        sender = UserData.query.filter_by(email=current_user.email).first()
        if sender.username == username:
            me = True
    if form.validate_on_submit():
        if current_user.is_authenticated:
            snd = FeedbackDB.query.filter_by(sender=sender.id, receiver=userdata.id,
                                             date=datetime.date.today()).first()
            if snd:
                flash("You've already sent a feedback today to this person", category="feedback")
                return redirect("#feedbackform")
            else:
                fb = FeedbackDB(sender=sender.id, receiver=userdata.id, star=form.star.data,
                                review=form.review.data, date=datetime.date.today())
                db.session.add(fb)
                db.session.commit()
                flash("Feedback Sent", category="feedback")
        else:
            flash("You need to log in before entering a feedback", category="feedback")
            return redirect("#feedbackform")
    if formexp.validate_on_submit():
        old_exp = ExperienceDB.query.filter_by(user_id=sender.id,
                                               title=formexp.title.data.capitalize()).first()
        if old_exp:
            flash("You already have an experience with this title, please change it!", category="experience")
        if (formexp.end_date.data - today).days > 366:
            flash("End date must be less than one year from today", category="experience")
        elif formexp.end_date.data < formexp.start_date.data:
            flash("End date must be greater than start date", category="experience")
        elif formexp.end_date.data < formexp.start_date.data:
            flash("End date must be after start date", category="experience")
        elif formexp.start_date.data < today:
            flash("Start date must be after today", category="experience")
        else:
            exp = ExperienceDB(
                user_id=sender.id,
                title=formexp.title.data.title(),
                provinceExp=formexp.province.data.title(),
                description=formexp.description.data,
                date_of_addition=datetime.date.today(),
                start_date=formexp.start_date.data,
                end_date=formexp.end_date.data,
                price=formexp.price.data,
                place=formexp.place.data.title()
            )
            db.session.add(exp)
            db.session.commit()
            flash("Experience added, thank you!", category="experience")
            exp = ExperienceDB.query.filter_by(user_id=sender.id, title=formexp.title.data.title()).first()
            return redirect(url_for('profile', username=sender.username) + '#' + str(exp.id))
        return redirect(url_for('profile', username=sender.username) + '#experience')
    if me:
        if formdelete.validate_on_submit():
            exp = ExperienceDB.query.filter_by(id=formdelete.expid.data).first()
            if exp is not None:
                db.session.delete(exp)
                db.session.commit()
                flash("Experience correctly deleted!", category="experiencedeleted")
            return redirect(url_for('profile', username=sender.username) + '#experiencebody')
    experience = ExperienceDB.query.filter_by(user_id=userdata.id)
    fr = FeedbackDB.query.filter_by(receiver=userdata.id).join(UserData, FeedbackDB.receiver == UserData.id).all()
    num_fr = FeedbackDB.query.filter_by(receiver=userdata.id).count()
    return render_template('profile.html', username=username, form=form, user=user, lang=lang, me=me,
                           formdelete=formdelete,
                           feedback_received=fr, userdata=userdata, formexp=formexp, num_fr=num_fr,
                           experience=experience, today=today)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('profile_by_id', id=current_user.id))
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        usr = UserData.query.filter_by(username=form.username.data).first()
        password_strength = password_check(form.password.data)
        if usr:
            flash("Username already used", category="error")
        elif user:
            flash("Email already used", category="error")
        elif form.password.data != form.confirm.data:
            flash("Make sure you typed the password correctly", category="passworderror")
        elif password_strength['password_ok'] == 0:
            flash("Password must have min 8 character: 1 lowercase, 1 uppercase, 1 symbol and 1 number.",
                  category="passworderror")
        else:
            pass_hashed = generate_password_hash(form.password.data)
            username = form.username.data
            new_user2 = User(
                email=email.lower(),
                password=pass_hashed)
            new_user = UserData(
                id=new_user2.id,
                username=username.lower(),
                name=form.name.data.title(),
                surname=form.surname.data.title(),
                bio=form.bio.data,
                phone=form.phone.data,
                email=email.lower(),
                province=form.province.data.title()
            )
            db.session.add(new_user2)
            db.session.commit()
            db.session.add(new_user)
            db.session.commit()
            for l in form.language.data:
                lang_user = LanguagesSpoken(id=new_user2.id, lang=l)
                db.session.add(lang_user)
                db.session.commit()
            flash("Account created!", category="successcreated")
            folder_name = str(new_user2.id)
            if not os.path.exists('static/assets/profilephoto/' + folder_name):
                os.makedirs('static/assets/profilephoto/' + folder_name)
            file_url = 'assets/profilephoto/' + folder_name
            profilepicture = form.profilepicture.data
            photos.save(profilepicture, name=folder_name + '.jpg', folder=file_url)
            login_user(new_user2)
            msg = Message('hey there! All good, start hiking!', recipients=[email],
                          sender=app.config['MAIL_USERNAME'])
            msg.body = msg_signup
            mail.send(msg)
            return redirect(url_for('profile', username=form.username.data.lower()))

    return render_template('signup.html', form=form)


@app.route('/signup4guides', methods=['GET', 'POST'])
def signup4guides():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('profile_by_id', id=current_user.id))
    if form.validate_on_submit():
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        usr = UserData.query.filter_by(username=form.username.data).first()
        password_strength = password_check(form.password.data)
        if usr:
            flash("Username already used", category="error")
        elif user:
            flash("Email already used", category="error")
        elif password_strength['password_ok'] == 0:
            flash("Password must have min 8 character: 1 lowercase, 1 uppercase, 1 symbol and 1 number.",
                  category="passworderror")
        elif form.password.data != form.confirm.data:
            flash("Make sure you typed the password correctly", category="passworderror")
        else:
            pass_hashed = generate_password_hash(form.password.data)
            username = form.username.data
            new_user2 = User(
                email=email.lower(),
                password=pass_hashed)
            new_user = UserData(
                id=new_user2.id,
                username=username.lower(),
                name=form.name.data.title(),
                surname=form.surname.data.title(),
                bio=form.bio.data,
                phone=form.phone.data,
                email=form.email.data.lower(),
                guide=1,
                professional=form.professional.data,
                province=form.province.data.title()
            )
            db.session.add(new_user2)
            db.session.commit()
            db.session.add(new_user)
            db.session.commit()
            for l in form.language.data:
                lang_user = LanguagesSpoken(id=new_user2.id, lang=l)
                db.session.add(lang_user)
                db.session.commit()
            flash("Account created!", category="successcreated")
            folder_name = str(new_user2.id)
            if not os.path.exists('static/assets/profilephoto/' + folder_name):
                os.makedirs('static/assets/profilephoto/' + folder_name)
            file_url = 'assets/profilephoto/' + folder_name
            profilepicture = form.profilepicture.data
            photos.save(profilepicture, name=folder_name + '.jpg', folder=file_url)
            login_user(new_user2)
            msg = Message('hey there, your subscription is accepted! Start inserting new exciting experiences!',
                          recipients=[email], sender=app.config['MAIL_USERNAME'])
            msg.body = msg_signup
            mail.send(msg)
            return redirect(url_for('profile', username=form.username.data.lower()))

    return render_template('signup4guides.html', form=form)


@app.route('/search/<province>', methods=['GET', 'POST'])
def search(province):
    today = datetime.date.today()
    number_of_experiences = ExperienceDB.query.filter_by(provinceExp=province.title()).where(
        ExperienceDB.end_date >= today).count()
    form = Suggest()
    if form.validate_on_submit():
        usr = User.query.filter_by(email=form.email.data.lower()).first()
        if usr:
            flash("This person is already subscribed. We hope to see new experiences soon!", category="success")
        else:
            msg = Message('hey there, a friend of you is already hiking, what do you wait?',
                          recipients=[form.email.data],
                          sender=app.config['MAIL_USERNAME'])
            msg.body = msg_suggestion
            mail.send(msg)
            flash("Mail sent, thank you!", category="success")
    exp = ExperienceDB.query.filter_by(provinceExp=province.title()).join(UserData,
                                                                          ExperienceDB.user_id == UserData.id).order_by(
        desc(ExperienceDB.date_of_addition)).all()
    provinces = ExperienceDB.query.where(ExperienceDB.end_date >= today).distinct(ExperienceDB.provinceExp).all()
    province_served = []
    for p in provinces:
        if p.provinceExp not in province_served:
            province_served.append(p.provinceExp)
    return render_template('search.html', province=province, exp=exp, number_of_experiences=number_of_experiences,
                           form=form, today=today, province_served=province_served)


@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('profile_by_id', id=current_user.id))
    if form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                usr = UserData.query.filter_by(email=email).first()
                login_user(user, remember=form.remember.data, duration=datetime.timedelta(days=10))
                if session['profile'] is not None:
                    username = session['profile']
                    session['profile'] = None
                    return redirect(url_for('profile', username=username))
                return redirect(url_for('profile', username=usr.username))
            flash("wrong password", category="error")
            return redirect(url_for('login'))
        flash("invalid email", category="error")
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/editdata', methods=['GET', 'POST'])
@login_required
def editdata():
    personal = User.query.filter_by(id=current_user.id).first()
    user = UserData.query.filter_by(id=current_user.id).first()
    form = EditData()
    if form.validate_on_submit():
        if form.name.data != '':
            user.name = form.name.data.title()
        if form.surname.data != '':
            user.surname = form.surname.data.title()
        if form.bio.data != '':
            user.bio = form.bio.data
        if form.phone.data != '':
            user.phone = form.phone.data
        if form.province.data != '':
            user.province = form.province.data.title()
        if form.professional.data != 0:
            user.professional = 1
        if not form.premium.data:
            user.premium = 0
        if form.premium.data:
            user.premium = 1
        db.session.commit()
        l = form.language.data
        if form.language.data != []:
            oldlang = LanguagesSpoken.query.filter_by(id=current_user.id).all()
            for l in oldlang:
                db.session.delete(l)
                db.session.commit()
            for l in form.language.data:
                lang_user = LanguagesSpoken(id=current_user.id, lang=l)
                db.session.add(lang_user)
                db.session.commit()
        if form.profilepicture.data is not None:
            folder_name = str(personal.id)
            if os.path.exists('static/assets/profilephoto/' + folder_name):
                print('static/assets/profilephoto/' + folder_name + "/" + folder_name + ".jpg")
                os.remove("static/assets/profilephoto/" + folder_name + "/" + folder_name + ".jpg")
            file_url = 'assets/profilephoto/' + folder_name
            profilepicture = form.profilepicture.data
            photos.save(profilepicture, name=folder_name + '.jpg', folder=file_url)
        if form.password.data != '':
            if form.password.data == form.confirm.data:
                password_strength = password_check(form.password.data)
                if password_strength['password_ok'] == 0:
                    flash("Password must have min 8 character: 1 lowercase, 1 uppercase, 1 symbol and 1 number.",
                          category="passworderror")
                    return redirect(url_for('editdata'))
                else:
                    usr = User.query.filter_by(id=user.id).first()
                    usr.password = generate_password_hash(form.password.data)
                    db.session.commit()
            else:
                flash("Password do not match, please try again", category="error")
                return redirect(url_for('editdata'))
        return redirect(url_for('profile', username=user.username))
    return render_template('editdata.html', form=form, user=user)


if __name__ == '__main__':
    app.run(debug=True)
