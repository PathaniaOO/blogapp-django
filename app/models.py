from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    slug=models.SlugField(max_length=255, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug :
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name 
    
    
class Subscribe(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    date = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)



class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=255, unique=True)
    image=models.ImageField(null=True,blank=True, upload_to='images/')
    tags=models.ManyToManyField(Tag, blank=True, related_name='post')
    view_count= models.IntegerField(null=True, blank=True, default=0)
    is_featured = models.BooleanField(default=False)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    bookmarks=models.ManyToManyField(User, related_name='bookmarks', default=None, blank=True)
    likes=models.ManyToManyField(User, related_name='post_like', default=None, blank=True)

    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_comments(self):
        return self.comments.count()
    
    def number_of_top_level_comments(self):
        return self.comments.filter(parent=None).count()

class Comments(models.Model):
    content=models.TextField()
    date =models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    website=models.CharField(max_length=200)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author=models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    parent=models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

class WebsiteMeta(models.Model):
    title= models.CharField(max_length=255,)
    description = models.CharField(max_length=200)
    about= models.TextField(max_length=500)