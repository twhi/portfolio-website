from django.contrib import admin
from .models import About
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(About, MarkdownxModelAdmin)
