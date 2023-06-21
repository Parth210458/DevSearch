from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import Profile, Skill
from django.db.models import Q




def paginateProfiles(request, profiles,results):
    page = request.GET.get("page")
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    leftidx = int(page)-4
    if leftidx<1:
        leftidx=1
    rightidx = int(page) + 4
    if rightidx>paginator.num_pages:
        rightidx=paginator.num_pages
    custom_range = range(leftidx,rightidx+1)
    return profiles,custom_range

def searchProfile(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
          )
    return profiles, search_query