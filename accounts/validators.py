import re
from datetime import date

from django.core.exceptions import ValidationError


def validate_username(username: str) -> None:
    if re.search(r'^[A-Za-z_]*$', username) is None:
        raise ValidationError(f'{username} contains non-english letters or characters other than underscore')
    if username.startswith('_') or username.endswith('_'):
        raise ValidationError(f'{username} cannot start or end with an underscore')


def validate_name(name: str) -> None:
    if re.search(r'^[A-Za-z]*$', name) is None:
        raise ValidationError(f'{name} contains non-english letters')


def validate_birth_date(birth_date: date) -> None:
    if birth_date.year < 1900:
        raise ValidationError('Invalid birth date - year must be greater than 1900.')
    age = (date.today() - birth_date).days // 365
    if age < 18:
        raise ValidationError('You must be at least 18 years old to register.')
