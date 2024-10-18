from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superadmin", True)
        extra_fields.setdefault("is_superuser", True)  # Ensures this is set
        extra_fields.setdefault("is_staff", True)      # Ensures staff access

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser , PermissionsMixin):
    name= models.CharField(max_length=255)
    email= models.EmailField(max_length=100, unique=True)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    username= None

    objects  = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['name']

    def __str__(self):
        return self.email

    def get_by_natural_key(self,email):
        return self.objects.get(email=email)

