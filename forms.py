from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Enter email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "Enter first name"})
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Enter last name"})
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Enter email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    submit = SubmitField("Register")
