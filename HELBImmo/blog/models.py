from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

#Post model, type_bien is used to differenciate between types of real estate
class Post(models.Model):
    type_bien = models.CharField(max_length=20, default='Maison')
    title = models.CharField( max_length=100 )
    content = models.TextField()
    date_posted = models.DateTimeField( default=timezone.now )
    author = models.ForeignKey( User, on_delete=models.CASCADE )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    livable_surface = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    room_amount = models.IntegerField(default=0)
    nb_etage = models.IntegerField(default=1)
    situe_etage = models.IntegerField(default=0)
    thumbnail = models.ImageField(default='no_photo.jpg', upload_to='gallery_images')
    to_sell = models.BooleanField(default=True)
    #addresse
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    latitude = models.DecimalField(max_digits=12, decimal_places=10)
    road_num = models.CharField( max_length=100)
    region_city = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)

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

#single consultation of a given post, created after loading it's detailed page
class PostConsult(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField( default=timezone.now)

    def __str__(self):
        return self.post.title + " consult"

#favorite of a post, used for the watchlist
class PostFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return self.user.__str__() + " favorite on " + self.post.title

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return self.user.__str__() + ' on ' + self.post.__str__() + ' : ' + self.content

#answer is a different model due to it linking to the question rather than the post itself
class Reponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return 'answer to ' + self.question.__str__()