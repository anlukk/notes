from django.db import models
from django.conf import settings
from django.urls import reverse


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

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile', 
        )
    
    narrate = models.TextField(
        max_length=9999, 
        default='Enter Narration',
        )
    
    review_narration = models.CharField(
        max_length=50, 
        choices=NARRATESTATUS, 
        default='Reviewing Narration',
        )
    
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        )
    
    photo = models.ImageField(
        upload_to='', 
        blank=True,
        )

    def __str__(self):
        return 'profile for user {}'.format(self.user.username)
    
class SimpleNote(models.Model):
   """Create new Simple note"""

   name = models.CharField(
       max_length=50, 
       verbose_name='Name note',
       )
   
   text = models.CharField(
       max_length=10000000, 
       verbose_name='Note',
       )
   
   images = models.FileField(
       verbose_name='Upload file'
       )

   time_create = models.DateTimeField(
       auto_now_add=True, 
       verbose_name='Time add in time_create',
       )
   
   time_update = models.DateTimeField(
       auto_now=True, 
       verbose_name='Time update in time_create',
       )
   
   slug = models.SlugField(
       max_length=255,
       unique=True,
       db_index=True,
       verbose_name="URL",
   )

   is_printing = models.BooleanField(default=True)


   def get_absolute_url(self):
       return reverse('simple_note', kwargs={'simple_note_slug': self.slug})
       

   def __str__(self):
       return self.name
   
   class Meta:
       verbose_name = 'Simple Note'
       ordering = ['time_create', 'name']
