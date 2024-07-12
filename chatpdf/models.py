
from django.db import models
from django.contrib.auth.models import User
import shortuuid
 

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    chat_file= models.CharField(max_length=255, default='')

    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = shortuuid.uuid()
        super().save(*args, **kwargs)    
        

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.body or "File Message"}'



class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    vector_file = models.CharField(max_length=255, null=True, blank=True)
    file_name= models.CharField(max_length=255, blank=True, default='')
    extention= models.CharField(max_length=255, blank=True, default='')    

    def __str__(self):
        return f'{self.file.name}'

      