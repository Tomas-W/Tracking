from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class AddUserForm(FlaskForm):
    username = StringField(
        label="Username",
        render_kw={"placeholder": "Username"},
        validators=[
            DataRequired(message="Username is required"),
        ]
    )
    password = StringField(
        label="Password",
        render_kw={"placeholder": "Password"},
        validators=[
            DataRequired(message="Password is required"),
        ],
    )
    password2 = StringField(
        label="Repeat Password",
        render_kw={"placeholder": "Repeat Password"},
        validators=[
            DataRequired(message="Password is required"),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    form_type = HiddenField(default="add_user")
    submit = SubmitField(label="Add")
