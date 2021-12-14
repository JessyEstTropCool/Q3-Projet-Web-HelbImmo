from django import forms
from django.db.models import fields
from .models import Post, GalleryImage, PostConsult
from .widgets import MapWidget

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['typeBien', 
        'to_sell', 
        'title', 
        'content', 
        'price',
        'address',
        'road_num', 
        'region_city', 
        'country_code', 
        'longitude',
        'latitude',
        'livable_surface',
        'room_amount', 
        'thumbnail'
        ]
        widgets = {
            'road_num': forms.HiddenInput(), 
            'region_city': forms.HiddenInput(), 
            'country_code': forms.HiddenInput(), 
            'longitude': forms.HiddenInput(),
            'latitude': forms.HiddenInput()
        }

    TRUE_FALSE_CHOICES = (
        (True, 'A vendre'),
        (False, 'A louer')
    )

    CHOICES = (
        (True, 'Maison'),
        (False, 'Appart'),
        (None, 'Garage')
    )

    address = forms.CharField(widget=MapWidget())

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