from flask import session
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    HiddenField,
    SubmitField,
)
from wtforms.validators import DataRequired


def login_user(username: str) -> None:
    """Adds username to session."""
    session["username"] = username


class LoginForm(FlaskForm):
    username = StringField(
        label="Username",
        render_kw={"placeholder": "Username"},
        validators=[
            DataRequired(message="Username is required"),
        ]
    )
    password = PasswordField(
        label="Password",
        render_kw={"placeholder": "Password"},
        validators=[
            DataRequired(message="Password is required"),
        ]
    )
    remember = BooleanField("Remember me")
    form_type = HiddenField(default="login")
    submit = SubmitField(label="Login")
