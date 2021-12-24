from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from .models import GroupMessage, Group, Member, pm, Category
from django.http import HttpResponseRedirect
from .forms import GroupForm, MessageForm, PmForm, dmform, registerform
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def landing(request):
     return render(request, 'landing.html')
     
def index(request):
     if request.user.is_authenticated == False:
          return redirect('landing')
     groups = Group.objects.all().order_by('-created')[:15]
     colour = random.choice(['danger', 'secondary', 'warning'])
     colour2 = random.choice(['success', 'primary', 'info'])
     if request.method == 'POST':
          search = request.POST.get('search')
          groups = Group.objects.filter(Q(title__icontains=search) | Q(owner__username__icontains=search))

     context = {
          'groups' : groups,
          'colour' : colour,
          'colour2' : colour2,
          }

     try:
          user = request.user
          group = Group.objects.filter(members=user)
          private = pm.objects.filter(receiver=request.user, unread=True)
          
          context = {
          'groups' : groups,
          'group' : group,
          'private' : private,
          'colour' : colour,
          'colour2' : colour2,
          }
     except:
          pass
     return render(request, 'home.html', context)
@login_required(login_url='log-in')
def edit(request, pk):
     group = Group.objects.get(id=pk)
     form = GroupForm(instance=group)
     if request.method == 'POST':
          form = GroupForm(request.POST, instance=group)
          if form.is_valid:
               forms = form.save(commit=False)
               forms.owner = request.user
               forms.save()
               return redirect('home')
     
     context = {
          'form' : form
     }
     return render(request, 'edit.html', context)

@login_required(login_url='log-in')
def create(request):
     form = GroupForm()
     if request.method == 'POST':
          form = GroupForm(request.POST)
          if form.is_valid():
               forms = form.save(commit=False)
               forms.owner = request.user
               forms.save()
               forms.save_m2m()
               return redirect('home')
     
     context = {
          'form' : form
     }
     return render(request, 'create.html', context)
@login_required(login_url='log-in')
def groupview(request, pk):
     colors = ['danger', 'success', 'info', 'primary', 'secondary']
     group = Group.objects.get(id=pk)
     groups = False
     try:
          groups = Group.objects.filter(category__in=group.category.all()).distinct().order_by('-created')
     except:
          pass
     message = GroupMessage.objects.filter(group=group).order_by('update')[:10]
     form = MessageForm()
     members = group.members.all()
     context = {
          'group' : group,
          'messages' : message,
          'form' : form,
          'members' : members,
          'groups' : groups,
          'colors' : colors,
     }
     if request.method == 'POST':
          form = MessageForm(request.POST)
          if form.is_valid():
               forms = form.save(commit=False)
               forms.group = Group.objects.get(id=pk)
               forms.owner = request.user
               forms.save()
               return render(request, 'group.html', context)
     return render(request, 'group.html', context)
@login_required(login_url='log-in')
def joingroup(request):
     usering = request.user
     if request.method == 'POST':
          group_id = request.POST.get('group_id')
          group_obj = Group.objects.get(id=group_id)
          if usering in group_obj.members.all():
               group_obj.members.remove(usering)
          else:
               group_obj.members.add(usering)
     return HttpResponseRedirect(group_id)
@login_required(login_url='log-in')
def deleteGroup(request, pk):
    obj = Group.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
#     context = {
#             'obj' : obj
#     }
    return redirect('home')


def Loginpage(request): 
    if request.user.is_authenticated:
        return redirect('home')
    context = {'login' : True}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            pass

        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'incorrect Username or password')
            
    return render(request, 'login.html', context)
     
def logoutpage(request):
     if request.method == 'POST':
          logout(request)
          return redirect('home')
     return render(request, 'login.html', {'logout' : True})


def register(request):
    if request.user.is_authenticated:
          return redirect('home')
    form = registerform()
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)              
            return redirect('home')
        else:
            message = messages.error(request, 'error occured while submitting form')
            return render(request, 'register.html', {'form' : form, 'message' : message})
    return render(request, 'register.html', {'form' : form})



