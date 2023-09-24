from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
 def get_queryset(self):
    return super().get_queryset()\
    .filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    tag=TaggableManager()
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    title=models.CharField(max_length=256)
    slug=models.SlugField(max_length=256,unique_for_date='publish')
    body=models.TextField()
    publish=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status=models.CharField(choices=Status.choices,max_length=2,default=Status.DRAFT)
    user=models.ForeignKey(User,related_name="created_by",on_delete=models.CASCADE)
    class Meta:
        ordering = ['-publish']
        indexes=[
            models.Index(fields=['-publish'])
        ]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail',
        args=[self.slug,self.publish.day,
 self.publish.month,
self.publish.year,
])
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)
class Comment(models.Model):
    post = models.ForeignKey(Post,
    on_delete=models.CASCADE,
    related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
