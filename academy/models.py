from django.db import models
from django.contrib.auth.models import User  # Add this import



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/')
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)  # Add this field
    def __str__(self):
        return self.title

class Certification(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()