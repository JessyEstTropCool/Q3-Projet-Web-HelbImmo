from django.contrib import admin
from .models import Post, PostConsult, PostFavorite, Question, Reponse

admin.site.register(Post)
admin.site.register(PostConsult)
admin.site.register(PostFavorite)
admin.site.register(Question)
admin.site.register(Reponse)