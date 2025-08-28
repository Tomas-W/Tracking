import re

from flask_wtf import FlaskForm
from wtforms.fields import Field
from wtforms.validators import ValidationError



class EmailCheck:
    def __init__(self) -> None:
        self.invalid_message: str = "Invalid email"
        self.regex: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __call__(self, form: FlaskForm, field: Field) -> None:
        if not field.data:
            raise ValidationError(self.invalid_message)
        if not re.match(self.regex, field.data):
            raise ValidationError(self.invalid_message)
