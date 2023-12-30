from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField







# Create your models here.


#this for my user model ---------------------------------------------------------
from django.contrib.auth.models import BaseUserManager
from bson import Decimal128

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Ensure that the email is normalized
        email = self.normalize_email(email)

        return self.create_user(email, username, password=password, **extra_fields)



class userdata(AbstractBaseUser):
    # is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager() 

    def has_perm(self, perm, obj=None):
        # For simplicity, assuming all users have all permissions.
        return True

    def has_module_perms(self, app_label):
        # For simplicity, assuming all users have permissions to all modules.
        return True

    def __str__(self):
        return self.username

####################################
# Using the Custom User Model:

#you can use the custom user model like any other Django user model. 
# For example, 
# when creating a new user,use 
#  userdata.objects.create_user()      or      userdata.objects.create_superuser().
    # new_user = userdata.objects.create_user(email='user@example.com', username='example_user', password='password123')
    # new_superuser = userdata.objects.create_superuser(email='admin@example.com', username='admin_user', password='adminpassword')



User = get_user_model()


  #this for my listing model ---------------------------------------------------------  

class Review(models.Model):
    comment = models.TextField()
    rating = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Review"


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    reviews = models.ManyToManyField(Review)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete_associated_reviews(self):
        self.reviews.all().delete()

    def save(self, *args, **kwargs):
        # Convert Decimal128 to Decimal for the price field
        if isinstance(self.price, Decimal128):
            self.price = self.price.to_decimal()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title








