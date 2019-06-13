from django.db import models

'''
every time you update a model, or create a new one, then you should 
run 'python manage.py makemigrations' on the command line.
'''

class Job(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=256)
    description = models.TextField(default='')

    def __str__(self):
        return self.summary
