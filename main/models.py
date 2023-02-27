from django.db import models
from django.conf import settings


class Task(models.Model):
    title = models.CharField('Название', max_length=10000)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'personal'

class Profiles(models.Model):
    
    NARRATESTATUS = (
        ('PAS', 'Passed'),
        ('REV', 'For_Review'),
        ('ACC', 'Narration_Accepted'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    narrate = models.TextField(max_length=9999, default='Enter Narration')
    review_narration = models.CharField(max_length=50, choices=NARRATESTATUS, default='Reviewing Narration')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='', blank=True)

    def __str__(self):
        return 'profile for user {}'.format(self.user.username)
    
#class Notes(models.Model):
  #  block = models.TextField(max_length=10000000)
   # ...
