from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, EmailValidator


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractUser):
    username = None
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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
