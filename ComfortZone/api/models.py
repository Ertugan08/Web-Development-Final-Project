import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db.models import CharField, FloatField, TextField, IntegerField, DateField, ManyToManyField, BooleanField
from django.db.models.fields.related import ForeignKey
class UserManager(BaseUserManager):

    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # Свойство `USERNAME_FIELD` сообщает нам, какое поле мы будем использовать для входа.
    USERNAME_FIELD = 'username'

    # Сообщает Django, что класс UserManager, определенный выше,
    # должен управлять объектами этого типа.
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = timezone.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class Category(models.Model):
    name = CharField(max_length=255)
    photo = CharField(max_length=700)

    def __str__(self):
        return self.name


class Events(models.Model):
    title = CharField(max_length=255)
    desc = TextField()
    info = TextField()
    photo = CharField(max_length=800)
    like = models.ForeignKey()
    date = DateField(auto_now=True)
    category = ForeignKey(Category, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE, related_name='events', default=1)

    def __str__(self):
        return self.title

class LikeUser(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    event = ForeignKey(Events, on_delete=models.CASCADE, related_name='liked_events')
    user_liked = BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.event}"


