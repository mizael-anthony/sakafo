from django.db import models
from django.urls import reverse

# Create your models here.
class Blog(models.Model):
   title = models.CharField(max_length=100, unique=True)
   slug = models.SlugField(max_length=100, unique=True)
   body = models.TextField()
   img = models.ImageField(upload_to='images/', blank=True, null=True)
   posted = models.DateField(db_index=True, auto_now_add=True)
   category = models.ForeignKey('actu.Category', on_delete=models.CASCADE)

   def __str__(self):
        return self.title

   def __unicode__(self):
       return '%s' % self.title

   def get_absolute_url(self):
       return reverse('view_blog_post',args=(self.slug))

class Category(models.Model):
   title = models.CharField(max_length=100, db_index=True)
   slug = models.SlugField(max_length=100, db_index=True)

   def __unicode__(self):
       return '%s' % self.title

   def get_absolute_url(self):
       return reverse('view_blog_category', args=(self.slug))