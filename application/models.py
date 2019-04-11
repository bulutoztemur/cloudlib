from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


users_books_association = db.Table(
    'users_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

users_authors_association = db.Table(
    'users_authors',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_phone = db.Column(db.Text, unique=True)
    image_user = db.Column(db.String(20), nullable=False, default='default.jpg')
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    logins = db.relationship('Login', backref='user', lazy=True)
    fav_books = db.relationship("Book", secondary=users_books_association, backref='users_fav')
    fav_authors = db.relationship("Author", secondary=users_authors_association, backref='users_fav')
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_user}', '{self.creation_time}')"


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Login('{self.login_time}')"


books_authors_association = db.Table(
    'books_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

books_categories_association = db.Table(
    'books_categories',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    date_of_issue = db.Column(db.Integer)
    image_book = db.Column(db.String(20), nullable=False, default='default.jpg')
    authors = db.relationship("Author", secondary=books_authors_association, backref='books')
    categories = db.relationship("Category", secondary=books_categories_association, backref='books')
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Book('{self.bookname}', '{self.date_of_issue}', '{self.image_book}')"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Category('{self.category_name}')"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(60), nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Author('{self.author_name}')"


class Comment(db.Model):
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique_user_book'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    content = db.Column(db.String(60), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship(User, backref=db.backref("comments", cascade="all, delete-orphan"))
    book = db.relationship(Book, backref=db.backref("comments", cascade="all, delete-orphan"))
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.creation_time}')"


class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    user = db.relationship(User, backref=db.backref("points", cascade="all, delete-orphan"))
    book = db.relationship(Book, backref=db.backref("points", cascade="all, delete-orphan"))
    db.UniqueConstraint('user_id', 'book_id', name='unique_user_book')

    def __repr__(self):
        return f"Point('{self.point}')"


