from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, EmailValidator


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
    )
    # TODO fix for polish letters
    name_validator = RegexValidator(r'^[a-zA-Z]+$', 'Enter a valid name. This value may contain only letters.')
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        help_text=_('Required. 30 characters or fewer. Letters only.'),
        validators=[name_validator],
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters only.'),
        validators=[name_validator],
    )
    email_validator = EmailValidator()
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Standard email format.'),
        validators=[email_validator],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
