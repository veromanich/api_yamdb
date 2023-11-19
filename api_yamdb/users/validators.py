from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Запрещено использовать "me" в качестве username'),
            params={"value": value},
        )


class UsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = 'В username присутствуют запрещенные символы'
    code = 'invalid_username'
