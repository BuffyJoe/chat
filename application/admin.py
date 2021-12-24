from django.contrib import admin
from .models import Category, Group, GroupMessage, Member, pm

# Register your models here.

admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(pm)
admin.site.register(Member)
admin.site.register(Category)