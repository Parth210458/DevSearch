from django.shortcuts import render,redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.contrib import messages
from django.db.models import Q

from .models import Profile, Skill, Message
from .forms import customUserCreationForm,ProfileForm, SkillsForm, MessageForm
from .utils import searchProfile,paginateProfiles
# Create your views here.


def loginUser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username doesnot exist')
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'User loggedin')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'Username or password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'User loggedout')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = customUserCreationForm()

    if request.method == "POST":
        form = customUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request,user)
            messages.success(request,"Account created successfully")
            return redirect("edit-account")
        else:
            messages.error(request,'someting went wrong')




    context = {'page':page,'form':form}
    return render(request,'users/login_register.html',context)

def profiles(request):
    
    profiles, search_query = searchProfile(request)
    
    profiles,custom_range = paginateProfiles(request,profiles,6)
    context = {'profiles': profiles, 'search_query':search_query,"custom_range":custom_range}
    return render(request, "users/profiles.html", context)




def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description='')
    context = {'profile':profile, 'top_skills':top_skills, 'other_skills':other_skills}
    return render(request, 'users/user-profile.html',context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()

    projects = profile.project_set.all()
    context = {'profile':profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method =='POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile )
        if form.is_valid():
            form.save()

            return redirect('account')
    context={'form':form}

    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillsForm()
    context={'form':form}
    if request.method=='POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added successfully")
            return redirect('account')
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillsForm(instance = skill)
    context={'form':form}
    if request.method=='POST':
        form = SkillsForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully")
            return redirect('account')
    return render(request,'users/skill_form.html',context)


def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    context = {'object':skill}

    if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill deleted successfully!')
        return redirect('account')
    return render(request, 'delete_template.html')

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    #here using related name that was in models.py
    messagesRequest = profile.messages.all()

    unreadCount = messagesRequest.filter(is_read=False).count()
    print(unreadCount)
    context= {'messagesRequest':messagesRequest,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    print('sender:::::  ',message.sender.id)
    if message.is_read==False:
        message.is_read=True
        message.save()
    context={'message':message,'profile':profile}


    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form =MessageForm()

    try:
        sender = request.user.profile
    except:
        sender=None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name= sender.name
                message.email= sender.email
            message.save()

            messages.success(request,"Message sent successfully")
            return redirect(request,'user-profile',pk=recipient.id)


    context ={'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context)