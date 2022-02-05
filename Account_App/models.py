from django.db import models

#To create a custom user model and admin pannel
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy


#To automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyUserManager(BaseUserManager):
     '''A custom manager to deal with emails as unique identifier'''
     def _create_user(self,email,password, **extra_fields):
          """Create and save a user with a given email and password """

          if not email:
               raise ValueError("The Email must be set")
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_fields )
          user.set_password(password)
          user.save(using=self._db)
          return user

     def create_superuser(self, email, password, **extra_fileds):
          extra_fileds.setdefault('is_staff', True)
          extra_fileds.setdefault('is_superuser', True)
          extra_fileds.setdefault('is_active', True)

          if extra_fileds.get('is_staff') is not True:
               raise ValueError('Superuser must have is staff True')
          if extra_fileds.get('is_superuser') is not True:
               raise ValueError('Super user must have is superuser true.')
          return self._create_user(email, password, **extra_fileds)


class User(AbstractBaseUser,PermissionsMixin):
     email = models.EmailField(unique=True, null=False)
     is_staff = models.BooleanField(
          gettext_lazy('staff status'),
          default= False,
          help_text= gettext_lazy('Designates whether the user can log in this site')
     )

     is_active = models.BooleanField(
          gettext_lazy('active'),
          default = True,
          help_text = gettext_lazy('Designates whether this user should be treated as active. Unselect this insstead of deleting accounts')

     )
     USERNAME_FIELD = 'email'
     objects = MyUserManager()

     def __str__(self):
          return self.email

     def get__full_name(self):
          return self.email

     def get_short_name(self):
          return self.email


class Profile(models.Model):
     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
     username = models.CharField(max_length=264,blank=True)
     full_name =  models.CharField(max_length=264,blank=True)
     address_1 = models.CharField(max_length=300,blank=True)
     city = models.CharField(max_length=40,blank=True)
     zipcode = models.CharField(max_length=10,blank=True)
     country = models.CharField(max_length=50,blank=True)
     phone = models.CharField(max_length=20,blank=True)
     date_joined = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
          return self.username + str("'s profile")

     def is_fully_filled(self):
          fields_names = [f.name for f in self._meta.get_fields()]

          for field_name in fields_names:
               value = getattr(self,field_name)
               if value is None or value=='':
                    return False
          return True
           
@receiver(post_save, sender=User)
def created_profile(sender,instance, created, **kwargs):
     if created:
          Profile.objects.create(user= instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
     instance.profile.save()