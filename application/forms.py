from django.db.models import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple, SelectMultiple
from .models import Category, Group, GroupMessage, pm
from django import forms

class GroupForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Group
        fields = ['title', 'description']

class MessageForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']

class PmForm(ModelForm):
    class Meta:
        model = pm
        fields = ['receiver', 'body']

class dmform(ModelForm):
    class Meta:
        model = pm
        fields = ['body']


class registerform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        