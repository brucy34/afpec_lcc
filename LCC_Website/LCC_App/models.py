from django.contrib.auth.hashers import make_password,check_password
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _



class ConcurrentManager(BaseUserManager):
    def create_user(self, concurrent_code, password=None,firstname=None,lastname=None, **extra_fields):
        if not concurrent_code:
            raise ValueError('The Concurrent Code field must be set')
        concurrent = self.model(concurrent_code=concurrent_code, **extra_fields)
        concurrent.set_password(password)
        concurrent.firstname=firstname
        concurrent.lastname=lastname
        concurrent.save(using=self._db)
        return concurrent

    def create_superuser(self, concurrent_code, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(concurrent_code, password, **extra_fields)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img=models.FileField(upload_to='cat_img/')

    def __str__(self):
        return self.name

class Book(models.Model):
    code = models.CharField(max_length=100,primary_key=True,editable=False)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True)
    authors_in = models.CharField(max_length=100, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField()
    edition = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    nbPage = models.PositiveIntegerField(blank=True,)
    pdf = models.FileField(upload_to='pdfs/')
    category = models.ForeignKey(Category,on_delete=models.PROTECT)

    def generate_code(self):
        code = f"{self.author[:1]}-{self.title[:5]}-{self.year}"
        return code.upper()

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    vid = models.FileField(upload_to='videos/')
    img =models.FileField(upload_to='videos/img/', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Concurrent(AbstractBaseUser, PermissionsMixin):
    concurrent_code = models.CharField(max_length=25, unique=True)
    lastname = models.CharField(max_length=100, help_text='john',null=True)
    firstname = models.CharField(max_length=100, help_text='doe', null=True)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    in_university = models.BooleanField(verbose_name="Are you in University right now?",default=False)
    university = models.CharField(max_length=100,blank=True)
    discipline = models.CharField(max_length=100,blank=True)
    level = models.CharField(max_length=100,blank=True)
    profession = models.CharField(max_length=100,blank=True)
    last_login = models.DateTimeField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add the password field back
    password = models.CharField(max_length=128)
    personal_library = models.ManyToManyField(Book, related_name='added_books', blank=True)

    objects = ConcurrentManager()

    USERNAME_FIELD = 'concurrent_code'
    REQUIRED_FIELDS = []  # Add any additional required fields here

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='concurrents_groups',  # Specify a unique related_name
        related_query_name='concurrent',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='concurrents_permissions',  # Specify a unique related_name
        related_query_name='concurrent',
    )

    def save(self, *args, **kwargs):
        if not self.concurrent_code:
            self.concurrent_code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        code_prefix = f"{self.lastname[:3]}-{self.firstname[:3]}-24-AFPEC-LCC"
        return code_prefix.upper()

    def __str__(self):
        return self.concurrent_code
