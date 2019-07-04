from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Creaate your models here.
class About(models.Model):
    about = MarkdownxField()

    @property
    def formatted_markdown(self):
        return markdownify(self.about)

    def __str__(self):
        return "About me section"
