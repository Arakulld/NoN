import os
from django.conf import settings
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def save(self, *args, **kwargs):
        try:
            old_photo = Profile.objects.get(pk=self.pk).photo
        except Profile.DoesNotExist:
            old_photo = None

        if old_photo and old_photo != self.photo:
            try:
                os.remove(old_photo.path)
            except FileNotFoundError:
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        photo_path = self.photo.path
        super(Profile, self).delete(*args, **kwargs)
        if photo_path:
            os.remove(photo_path)
