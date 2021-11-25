from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

class Post(models.Model):
    title = models.CharField( max_length=100 )
    content = models.TextField()
    date_posted = models.DateTimeField( default=timezone.now )
    author = models.ForeignKey( User, on_delete=models.CASCADE )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    livable_surface = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    #locality = models.ForeignKey( City)
    room_amount = models.IntegerField(default=0)
    thumbnail = models.ImageField(default='no_photo.jpg', upload_to='gallery_images')
    to_sell = models.BooleanField(default=True)
    #consultations

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class GalleryImage(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE, default=Post.objects.first() )
    image = models.ImageField(default='no_photo.jpg', upload_to='gallery_images')
