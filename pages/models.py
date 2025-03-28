from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


from utils.generators import unique_slugify


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class ArticlePost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    views = models.PositiveIntegerField(default=0)
    is_index = models.BooleanField(default=False)
    image_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        new_slug = f"{self.title}"
        unique_slugify(self, new_slug)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blogpost-detail', kwargs={'slug': self.slug})
    

class Comment(models.Model):
    post = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    # email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email_address = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_address
    

class GlobalCounter(models.Model):
    key = models.CharField(max_length=50, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.key}: {self.count}"
