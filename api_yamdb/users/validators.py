from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(username):
    if username == 'me':
        raise ValidationError('username "me" запрещён')
    regular_expression_validate = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message=f"username: '{username}' содержит запрещенные символы",
        code='invalid_username',
    )
    regular_expression_validate(username)
    return username
