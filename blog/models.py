from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = MarkdownxField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    image = models.ImageField(upload_to='images/', null=True)

    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return 'Author: {}, Post: {}, Date: {}'.format(self.author, self.post, self.created_on)
