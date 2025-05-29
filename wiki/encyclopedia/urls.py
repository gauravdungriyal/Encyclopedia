from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki",views.index,name="wiki"),
    path("wiki/<str:title>/",views.wiki,name="wiki_title"),
    path("search",views.search,name="search"),
    path("createpage",views.createpage,name="create_page"),
    path("editpage/<str:title>/",views.editpage,name="edit_page"),
]
