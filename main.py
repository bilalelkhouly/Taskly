import os
from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import relationship
from forms import LoginForm, RegisterForm
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///tasks.db")
db = SQLAlchemy()
db.init_app(app)


# Configure tables
class User(UserMixin, db.Model):
    __tablename__ = "user_data"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(100))
    lists = relationship("Lists", back_populates="user")


class Lists(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey("user_data.id"), nullable=False)
    user = relationship("User", back_populates="lists")
    tasks = relationship('Tasks', back_populates="list")
    __table_args__ = (db.UniqueConstraint('list_title', 'user_id', name='_user_list_title_uc'),)


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    list = relationship('Lists', back_populates='tasks')


with app.app_context():
    db.create_all()

today = datetime.now().date()
tomorrow = today + timedelta(days=1)


@app.route('/')
def dashboard():
    if current_user.is_authenticated:
        total_tasks = 0
        overdue_tasks = 0
        completed_tasks = 0
        upcoming_tasks = []
        for user_list in current_user.lists:
            for task in user_list.tasks:
                total_tasks += 1
                if task.completed:
                    completed_tasks += 1
                if task.due_date.date() < today:
                    overdue_tasks += 1
                if task.due_date.date() in [today, tomorrow]:
                    upcoming_tasks.append(task)
        return render_template('dashboard.html', user=current_user, lists=current_user.lists,
                               upcoming_tasks=upcoming_tasks[:5], total_tasks=total_tasks, overdue_tasks=overdue_tasks,
                               completed_tasks=completed_tasks, due_tasks=total_tasks-overdue_tasks, today=today)
    else:
        return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user:
            # User doesn't exist
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            # Password incorrect
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, please log in instead.")
            return redirect(url_for('login'))
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User(
            email=email,
            password=generate_password_hash(password=password, method="pbkdf2:sha256", salt_length=8),
            first_name=first_name,
            last_name=last_name
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)