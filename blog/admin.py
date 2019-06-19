from django.contrib import admin
from .models import Post, Category, Comment
from markdownx.admin import MarkdownxModelAdmin

# class PostAdmin(admin.ModelAdmin):
#     pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
