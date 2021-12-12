from django.contrib import admin
from .models import Post, GalleryImage, PostConsult, PostFavorite

admin.site.register(Post)
admin.site.register(GalleryImage)
admin.site.register(PostConsult)
admin.site.register(PostFavorite)