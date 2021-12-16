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
    #addresse
    longitude = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    latitude = models.DecimalField(max_digits=12, decimal_places=10, default=0)
    road_num = models.CharField( max_length=100, default='Grand Place 14')
    region_city = models.CharField(max_length=100, default='1000 City of Brussels, Brussels-Capital')
    country_code = models.CharField(max_length=2, default='BE')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, **kwargs):
        super().save(**kwargs)

        img = Image.open(self.thumbnail.path)
        
        if img.height > 1080 or img.width > 1920:
            output_size = (1920, 1080)
            img.thumbnail(output_size)

        img.save(self.thumbnail.path)

class GalleryImage(models.Model):
    #post = models.ForeignKey(Post, on_delete=models.CASCADE, default=Post.objects.first() )
    image = models.ImageField(default='no_photo.jpg', upload_to='gallery_images')

class PostConsult(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField( default=timezone.now)

    def __str__(self):
        return self.post.title + " consult"

class PostFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return self.user.username + " favorite on " + self.post.title