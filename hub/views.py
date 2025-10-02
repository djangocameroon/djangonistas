"""Views powering the community hub pages."""

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Community, Person, School

PAGE_SIZE = 9


def home(request):
    """Landing page introducing the initiative and highlighting navigation."""
    context = {
        "people_count": Person.objects.count(),
        "community_count": Community.objects.count(),
        "school_count": School.objects.count(),
    }
    return render(request, "hub/home.html", context)


def _paginate(request, queryset):
    paginator = Paginator(queryset, PAGE_SIZE)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    page.elided_page_range = paginator.get_elided_page_range(
        page.number, on_each_side=1, on_ends=1
    )
    return page


def _filter_people(queryset, request):
    """Apply search and filter logic to people queryset."""
    search_query = request.GET.get('search', '').strip()
    role_filter = request.GET.get('role', '').strip()
    location_filter = request.GET.get('location', '').strip()
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(bio__icontains=search_query) |
            Q(interests__icontains=search_query) |
            Q(availability__icontains=search_query)
        )
    
    if role_filter:
        queryset = queryset.filter(role__icontains=role_filter)
    
    return queryset


def _filter_communities(queryset, request):
    """Apply search and filter logic to communities queryset."""
    search_query = request.GET.get('search', '').strip()
    location_filter = request.GET.get('location', '').strip()
    focus_filter = request.GET.get('focus', '').strip()
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(focus__icontains=search_query)
        )
    
    if location_filter:
        queryset = queryset.filter(location__icontains=location_filter)
    
    if focus_filter:
        queryset = queryset.filter(focus__icontains=focus_filter)
    
    return queryset


def _filter_schools(queryset, request):
    """Apply search and filter logic to schools queryset."""
    search_query = request.GET.get('search', '').strip()
    city_filter = request.GET.get('city', '').strip()
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(programs__icontains=search_query)
        )
    
    if city_filter:
        queryset = queryset.filter(city__icontains=city_filter)
    
    return queryset


def people_list(request):
    """Directory of contributors and mentors."""
    queryset = Person.objects.all()
    queryset = _filter_people(queryset, request)
    
    # Get filter options for dropdowns
    roles = Person.objects.values_list('role', flat=True).distinct().exclude(role='')
    
    page_obj = _paginate(request, queryset)
    context = {
        "page_obj": page_obj, 
        "people": page_obj,
        "roles": sorted(roles),
        "current_search": request.GET.get('search', ''),
        "current_role": request.GET.get('role', ''),
    }
    return render(request, "hub/people.html", context)


def people_detail(request, slug):
    """Detail page for a single contributor."""
    person = get_object_or_404(Person, slug=slug)
    return render(request, "hub/person_detail.html", {"person": person})


def community_list(request):
    """Directory of communities that collaborate with Django Cameroon."""
    queryset = Community.objects.all()
    queryset = _filter_communities(queryset, request)
    
    # Get filter options for dropdowns
    locations = Community.objects.values_list('location', flat=True).distinct().exclude(location='')
    
    page_obj = _paginate(request, queryset)
    context = {
        "page_obj": page_obj, 
        "communities": page_obj,
        "locations": sorted(locations),
        "current_search": request.GET.get('search', ''),
        "current_location": request.GET.get('location', ''),
    }
    return render(request, "hub/communities.html", context)


def community_detail(request, slug):
    """Detail page for a partner community."""
    community = get_object_or_404(Community, slug=slug)
    links = community.links or {}
    link_items = [
        ("Website", links.get("website")),
        ("Twitter", links.get("twitter")),
    ]
    link_items = [item for item in link_items if item[1]]
    return render(
        request,
        "hub/community_detail.html",
        {"community": community, "link_items": link_items},
    )


def school_list(request):
    """Directory of schools and innovation hubs."""
    queryset = School.objects.all()
    queryset = _filter_schools(queryset, request)
    
    # Get filter options for dropdowns
    cities = School.objects.values_list('city', flat=True).distinct().exclude(city='')
    
    page_obj = _paginate(request, queryset)
    context = {
        "page_obj": page_obj, 
        "schools": page_obj,
        "cities": sorted(cities),
        "current_search": request.GET.get('search', ''),
        "current_city": request.GET.get('city', ''),
    }
    return render(request, "hub/schools.html", context)


def school_detail(request, slug):
    """Detail page for a school or innovation hub."""
    school = get_object_or_404(School, slug=slug)
    return render(request, "hub/school_detail.html", {"school": school})
