from django.urls import path

from . import views

app_name = "hub"

urlpatterns = [
    path("", views.home, name="home"),
    path("people/", views.people_list, name="people"),
    path("people/<slug:slug>/", views.people_detail, name="person-detail"),
    path("communities/", views.community_list, name="communities"),
    path("communities/<slug:slug>/", views.community_detail, name="community-detail"),
    path("schools/", views.school_list, name="schools"),
    path("schools/<slug:slug>/", views.school_detail, name="school-detail"),
    path("api/search/", views.search_api, name="search-api"),
]
