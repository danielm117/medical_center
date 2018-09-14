from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        route='geo/',
        view=TemplateView.as_view(template_name="geo.html"),
        name='index',
    ),
    path(
        route='calculate_index/',
        view=views.calculate_index,
        name='calculate_index',
    ),
    path(
        route='result_list/',
        view=views.ResultListView.as_view(),
        name='result_list',
    ),
]
