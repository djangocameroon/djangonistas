"""Views powering the community hub pages."""

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

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


def people_list(request):
    """Directory of contributors and mentors."""
    page_obj = _paginate(request, Person.objects.all())
    return render(request, "hub/people.html", {"page_obj": page_obj, "people": page_obj})


def people_detail(request, slug):
    """Detail page for a single contributor."""
    person = get_object_or_404(Person, slug=slug)
    return render(request, "hub/person_detail.html", {"person": person})


def community_list(request):
    """Directory of communities that collaborate with Django Cameroon."""
    page_obj = _paginate(request, Community.objects.all())
    return render(request, "hub/communities.html", {"page_obj": page_obj, "communities": page_obj})


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
    page_obj = _paginate(request, School.objects.all())
    return render(request, "hub/schools.html", {"page_obj": page_obj, "schools": page_obj})


def school_detail(request, slug):
    """Detail page for a school or innovation hub."""
    school = get_object_or_404(School, slug=slug)
    return render(request, "hub/school_detail.html", {"school": school})
