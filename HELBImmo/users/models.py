from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from blog.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    favorites = models.ManyToManyField(Post)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Criteria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    minimum_surface = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    #locality = models.ForeignKey( City)
    room_amount = models.IntegerField(default=0)