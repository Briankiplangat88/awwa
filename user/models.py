from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('profile_pics/', blank=True, default = 'image')

    def __str__(self):
        return self.user.username
    
    def save_profile(self):
        self.save()                   

    def delete_profile(self):
        self.delete()
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles' 
        
# creating user profile 

def create_user_profile(sender, instance, created, **kwargs):
        if created:Profile.objects.create(user=instance)
# saving user profile

def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        
# project attributes
class Projects(models.Model):
    project_title = models.CharField(max_length=255)
    project_image = CloudinaryField('images')
    project_description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField()
    country =CountryField(blank_label='(select country', default='Kenya')
    
    
    def save_project(self):
        self.save()
    
    def delete_project(self):
        self.delete()
        
    @classmethod
    def get_projects(cls):
        projects = cls.objects.all()
        return projects
    
    @classmethod
    def search_projects(cls, search_term):
        projects = cls.objects.filter(project_title__icontains=search_term)
        return projects
    
    
    @classmethod
    def get_by_author(cls, author):
        projects = cls.objects.filter(author=author)
        return projects
    
    
    @classmethod
    def get_project(request, id):
        try:
            project = Projects.objects.get(pk = id)
            
        except ObjectDoesNotExist:
            raise Http404()
        
        return project
    
    def __str__(self):
        return self.project_title
