from django.db import models


class Job(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=256)
    description = models.TextField(default='')
    hover_text = models.CharField(max_length=256)

    def __str__(self):
        return self.title
