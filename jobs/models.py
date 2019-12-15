from django.db import models


class Job(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=256)
    description = models.TextField(default='')
    hover_text = models.CharField(max_length=256)
    link_to_website = models.URLField(default='', max_length=2000, blank=True)
    link_to_github = models.URLField(default='', max_length=2000, blank=True)

    def __str__(self):
        return self.title
