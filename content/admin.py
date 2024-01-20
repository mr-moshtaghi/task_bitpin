from django.contrib import admin

from .models import Content, Rating


@admin.register(Content)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "text")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("rating",)