from django import forms
from django.db.models import fields
from .models import Post, GalleryImage, PostConsult

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['typeBien', 'to_sell', 'title', 'content', 'price', 'livable_surface', 'room_amount', 'thumbnail']

    TRUE_FALSE_CHOICES = (
        (True, 'A vendre'),
        (False, 'A louer')
    )

    CHOICES = (
        (True, 'Maison'),
        (False, 'Appart'),
        (None, 'Garage')
    )

    to_sell = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="A louer/A vendre", 
                                initial='', widget=forms.Select(), required=True)

    typeBien = forms.ChoiceField(choices = CHOICES, label="Type de bien", 
                                initial='', widget=forms.Select(), required=True)

    """def save(self, *args, **kwargs):
        self.instance.save()
        return self.instance"""

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']