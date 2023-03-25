from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


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
   """Simple Note models """

   user = models.ForeignKey(
       User,
       related_name="users",
       on_delete=models.CASCADE,
       verbose_name="user",
       )

   name = models.CharField(
       max_length=50, 
       verbose_name='Note name',
   )
   
   text=CKEditor5Field('Text', config_name='extends')
   
   file_note = models.FileField(
       verbose_name='Upload file',
       upload_to='uploads/%Y/%m/%d/',
       max_length=254,
       null=True,
       blank=True,
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

   cat = models.ForeignKey(
       'Category', 
       on_delete=models.PROTECT, 
       )

   def get_absolute_url(self):
       return reverse('simple_note', kwargs={'simple_note_slug': self.slug})
          
        
   def __str__(self):
       return f'{self.name}, {self.text}'
   

   class Meta:
       verbose_name = 'Simple Note'
       ordering = ['time_create', 'name']



class Category(models.Model):   

    name = models.CharField(
        max_length=100, 
        db_index=True, 
        verbose_name="Category"
        )
    
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        db_index=True, 
        verbose_name="URL",
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'
        ordering = ['id']
