from .models import Tag,Project
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginateProjects(request, projects,results):
    page = request.GET.get("page")
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    leftidx = int(page)-4
    if leftidx<1:
        leftidx=1
    rightidx = int(page) + 4
    if rightidx>paginator.num_pages:
        rightidx=paginator.num_pages
    custom_range = range(leftidx,rightidx+1)
    return projects,custom_range

def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains = search_query)
    projects = Project.objects.distinct().filter(
            Q(title__icontains = search_query) |
            Q(description__icontains = search_query) |
            Q(owner__name__icontains = search_query) |
            Q(tags__in=tags)
        )
    return projects, search_query