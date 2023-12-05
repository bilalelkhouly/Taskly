from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField, SelectField
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


class TaskForm(FlaskForm):
    task_text = StringField("Task", validators=[DataRequired()], render_kw={"placeholder": "Enter task"})
    due_date = DateField("Due Date", validators=[DataRequired()], render_kw={"placeholder": "Enter due date"})
    task_list = SelectField("List", validators=[DataRequired()], coerce=str)
    submit = SubmitField("Add")

class TaskListForm(FlaskForm):
    task_text = StringField("Task", validators=[DataRequired()], render_kw={"placeholder": "Enter task"})
    due_date = DateField("Due Date", validators=[DataRequired()], render_kw={"placeholder": "Enter due date"})
    submit = SubmitField("Add")

class ListForm(FlaskForm):
    list_name = StringField("List name", validators=[DataRequired()], render_kw={"placeholder": "Enter list name"})
    submit = SubmitField("Add")