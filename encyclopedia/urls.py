from re import search
from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/"+'<str:title>', views.editpage, name="editpage"),
    path("random", views.rand_page, name="rand_page"),
    path("404", views.notfound, name="notfound"),
    path("wiki/"+'<str:title>', views.viewpage, name="viewpage"),

]