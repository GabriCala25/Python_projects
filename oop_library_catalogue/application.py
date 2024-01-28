from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # Add a one-to-many relationship between User and Book
    books = db.relationship('Book', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Book {self.name} by {self.author}>"

with app.app_context():
    db.create_all()

class BookCatalog:
    def add_book(self, name, author):
        # Associate the book with the current logged-in user
        new_book = Book(name=name, author=author, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()

    def get_catalog(self):
        # Only retrieve books associated with the current logged-in user
        return Book.query.filter_by(user_id=current_user.id).all()

catalog = BookCatalog()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()
        flash('Registrazione completata con successo!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET'])
def landing():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            with app.app_context():
                login_user(user)
            flash('Accesso riuscito!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Accesso fallito. Verifica username e password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    books = catalog.get_catalog()
    return render_template('home.html', books = books)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        catalog.add_book(name, author)
        return redirect(url_for('home'))
    return render_template('add_book.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)