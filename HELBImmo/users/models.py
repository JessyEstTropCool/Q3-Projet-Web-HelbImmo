from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from blog.models import PostFavorite

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    #favorites = models.ManyToManyField(PostFavorite)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save(**kwargs)

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Criteria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    minimum_surface = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    locality = models.CharField(max_length=100, default='')
    room_amount = models.IntegerField(default=0)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Criteria'