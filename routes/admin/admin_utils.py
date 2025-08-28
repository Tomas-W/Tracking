from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class WeightForm(FlaskForm):
    date = StringField(
        label="Date",
        render_kw={"placeholder": "Date"},
        validators=[
            DataRequired(message="Date is required"),
        ]
    )
    weight = FloatField(
        label="Weight",
        render_kw={"placeholder": "Weight"},
        validators=[
            DataRequired(message="Weight is required"),
            NumberRange(min=0, message="Must be positive"),
        ],
    )
    form_type = HiddenField(default="weight")
    submit = SubmitField(label="Submit")
