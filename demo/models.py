from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser



class Post (models.Model):

    description = models.CharField(max_length=128, blank=False)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    postedDate = models.DateTimeField(auto_now_add=True)

class ImageUpload (models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ="static/", max_length=254)
    

class LikeHistory (models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    like = models.BooleanField(
        default = False, editable = False, serialize = False)
    
    dislike = models.BooleanField(
        default = False, editable = False, serialize = False)

