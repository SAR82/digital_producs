
import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password=None, is_staff=False, is_superuser=False, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given username, email, and password.
        """
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            elif phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
                while User.objects.filter(username=username).exists():
                    username += str(random.randint(10, 99))
            else:
                raise ValueError('Either username, email, or phone_number must be provided.')

        return self._create_user(username, phone_number, email, password, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, username, phone_number, email, password=None, **extra_fields):
        return self._create_user(username, phone_number, email, password, is_staff=True, is_superuser=True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text=_('Required. 30 characters or fewer starting with a letter. Letters, digits, and underscore characters are allowed.'),
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z][a-zA-Z0-9_\.]+$',
                _('Enter a valid username starting with a letter. This value may contain only letters, numbers, and underscore characters.'),
                'invalid'
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=False,
        null=True,
        blank=True,
    )
    phone_number = models.BigIntegerField(
        _('mobile number'),
        unique=True,
        null=True,
        blank=True,
        validators=[
            validators.RegexValidator(
            r'^989[0-3,9]\d{8}$',
            _('Enter a valid mobile number starting with 989 followed by 9 digits.'),
            'invalid'
            ),
        ],
        error_messages={
            'unique': _("A user with this mobile number already exists."),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        """
        String representation of the user.
        """
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nick_name = models.CharField(_('nick name'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.BooleanField(
        _('gender'),
        null=True,
        blank=True,
        help_text=_('Female is False, Male is True, Null is unspecified.')
    )
    province = models.ForeignKey(
        'Province',
        verbose_name=_('province'),
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f"{self.user.username}'s profile"
    

class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3

    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )

    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), null=True, blank=True)
    notify_token = models.CharField(
        _('Notification Token'),
        max_length=200,
        blank=True,
        validators=[
            validators.RegexValidator(
                r'^[a-zA-Z0-9]+$',
                _('Notify token is not valid'),
                'invalid'
            ),
        ]
    )
    last_login = models.DateTimeField(_('last login date'), null=True, blank=True)
    device_type = models.PositiveSmallIntegerField(
        _('Device Type'),
        choices=DEVICE_TYPE_CHOICES,
        default=ANDROID
    )
    device_os = models.CharField(_('Device OS'), max_length=20, blank=True)
    device_model = models.CharField(_('Device Model'), max_length=50, blank=True)
    app_version = models.CharField(_('App Version'), max_length=20, blank=True)
    created_time = models.DateTimeField(_('Created Time'), auto_now_add=True)

    class Meta:
        db_table = 'devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_uuid')

    def __str__(self):
        return f"{self.user.username}'s device ({self.get_device_type_display()})"
    
class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name