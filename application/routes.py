import os
from datetime import datetime
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, CommentForm
from application.models import User, Book, Login, Comment, Point
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password,
                    name=form.name.data.lower(), mobile_phone=form.mobile_phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.emailOrUsername.data.lower()).first()
        if user is None:
            user = User.query.filter_by(username=form.emailOrUsername.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            user_login = Login(user_id=user.id)
            login_user(user, remember=form.remember.data)
            db.session.add(user_login)
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    '''random_hex = secrets.token_hex(16)'''
    random_hex = datetime.now().strftime("%m%d%Y%H%M%S%f")
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def del_picture(filename):
    os.remove(os.path.join(app.root_path, 'static/profile_pics', filename))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            old_picture_file = current_user.image_user
            current_user.image_user = picture_file
            if picture_file != "default.jpg":
                del_picture(old_picture_file)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.mobile_phone = form.mobile_phone.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.mobile_phone.data = current_user.mobile_phone
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_user)
    return render_template('account.html', image_file=image_file, form=form)


@app.route("/books", methods=['GET', 'POST'])
@login_required
def books():
    books = Book.query.all()
    points_list=[]
    points_count =[]
    point_total=0
    for book in books:
        for p in book.points:
            point_total += p.point
        if len(book.points) != 0:
            point_avg = (point_total / len(book.points))
        else:
            point_avg = 0
        points_list.append(point_avg)
        points_count.append(len(book.points))
    return render_template('books.html', books=books, points_list=points_list, points_count=points_count)


@app.route("/book/<book_id>", methods=['GET', 'POST'])
@login_required
def book(book_id):
    a = request.args.get("point")
    point_check = Point.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if point_check:
        data_rat = point_check.point
    else:
        data_rat = 0
    if a is not None:
        if point_check:
            point_check.point = a
            db.session.add(point_check)
            db.session.commit()
        else:
            point = Point(user_id=current_user.id, book_id=book_id, point=a)
            db.session.add(point)
            db.session.commit()
        return redirect(url_for('book', book_id=book_id))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id, book_id=book_id, content=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('book', book_id=book_id))
    book = Book.query.filter_by(id=book_id).first()
    comments = Comment.query.filter_by(book_id=book.id).order_by(desc(Comment.creation_time))
    return render_template('book.html', book=book, comments=comments, form=form, func=parse_date, str=str, data_rat=data_rat)


def parse_date(date):
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    return day+'.'+month+'.'+year

