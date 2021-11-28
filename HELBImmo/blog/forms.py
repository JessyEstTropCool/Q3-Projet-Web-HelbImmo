from django import forms
from django.db.models import fields
from .models import Post, GalleryImage, PostConsult

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'price', 'livable_surface', 'room_amount', 'thumbnail']

    """def save(self, *args, **kwargs):
        self.instance.save()
        return self.instance"""

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']