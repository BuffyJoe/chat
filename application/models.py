from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import AutoField

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateField(auto_now=True)
    members = models.ManyToManyField(User, related_name='members', default=None, blank=True)
    category = models.ManyToManyField(Category, related_name='tags')

    def __str__(self):
        return f'{self.title}'

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'{self.body}'

JOIN_CHOICES = (
    ('MEMBER', 'MEMBER'),
    ('VISITOR', 'VISITOR'),
)
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    value = models.CharField(choices=JOIN_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.user)

class pm(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField()
    unread = models.BooleanField(default=False)

    def __str__(self):
        return f'sender:{self.sender} - receiver:{self.receiver} - {self.body}'
