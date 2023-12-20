from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.


# uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="Tag")
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)


    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse 

