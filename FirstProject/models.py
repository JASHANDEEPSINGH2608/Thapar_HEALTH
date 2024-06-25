from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    title=models.TextField()
    description=models.TextField()
    price=models.TextField()
    summary=models.TextField(default='this is so cool!')

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.user.username


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    time_slot=models.TimeField()
    desc=models.TextField()
    issue=models.TextField(null=True)
    created_at = models.DateTimeField(default=None, null=True, blank=True)
    is_canceled = models.BooleanField(default=False)
    

    def __str__(self):
        if self.user:
            return f"Appointment for {self.user.username} at {self.created_at}"
        else:
            return f"Appointment with no associated user at {self.created_at}"
from django.contrib.auth.models import User
from django.db import models

class signup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    roll_no = models.CharField(max_length=20, blank=True, null=True)


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/profile_images/filename
    return f'user_{instance.user.id}/profile_images/{filename}'
class data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    profile_image=models.ImageField(null=True,upload_to=user_directory_path)
    Mobile_number=models.TextField(max_length=10,null=True)
    Birthday=models.DateField(default='2020-11-26')
    Medical_Allergies=models.TextField(max_length=255)


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='prescriptions/')

    









