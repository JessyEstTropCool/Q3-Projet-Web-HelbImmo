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

    def clean(self):
        addr = self.cleaned_data['address']

        self.cleaned_data['road_num'] = addr[0]
        self.cleaned_data['region_city'] = addr[1]
        self.cleaned_data['country_code'] = addr[2]
        self.cleaned_data['longitude'] = format(float(addr[3]), ".10f")
        self.cleaned_data['latitude'] = format(float(addr[4]), ".10f")

        return self.cleaned_data

    def clean_address(self):
        addr = self.cleaned_data['address'].split('|')
        
        return addr

    """def save(self, *args, **kwargs):
        self.instance.save()
        return self.instance"""

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']