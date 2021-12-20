from django import forms
from django.db.models import fields
from django.core.exceptions import ValidationError
from .models import Post, GalleryImage, PostConsult
from .widgets import MapWidget

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['type_bien', 
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
        'nb_etage',
        'situe_etage',
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
        ('Maison', 'Maison'),
        ('Appartement', 'Appartement'),
        ('Garage', 'Garage')
    )

    address = forms.CharField(widget=MapWidget(), initial='')

    to_sell = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="A Louer/A Vendre", 
                                initial='', widget=forms.Select(), required=True)

    type_bien = forms.ChoiceField(choices = CHOICES, label="Type de bien", 
                                initial=CHOICES[0], widget=forms.Select(), required=False)

    def __init__(self, *args, **kwargs):
        form = kwargs.get('instance')

        if form is not None:
            kwargs.update(initial={
                'address': form.road_num + '|' + form.region_city + '|' + form.country_code + '|' + str(form.longitude) + '|' + str(form.latitude)
            })

        super().__init__(*args, **kwargs)

    def clean(self):
        addr = self.cleaned_data['address']

        if addr is not None:
            self.cleaned_data['road_num'] = addr[0]
            self.cleaned_data['region_city'] = addr[1]
            self.cleaned_data['country_code'] = addr[2]
            self.cleaned_data['longitude'] = format(float(addr[3]), ".10f")
            self.cleaned_data['latitude'] = format(float(addr[4]), ".10f")

        return self.cleaned_data

    def clean_address(self):
        addr = self.cleaned_data['address'].split('|')
        
        if len(addr) > 0 and addr[0] != 'None':
            return addr
        else:
            return None

    """def save(self, *args, **kwargs):
        self.instance.save()
        return self.instance"""

class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']