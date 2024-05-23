from django.urls import path, include
from . import views

app_name="master"

urlpatterns = [
    path('', views.redirect_to_dashboard, name='homepage'),
    path('dashboard', views.homepage, name='homepage'),
    path('<slug:slug>', views.crud_list, name='crud_list'),
    path('<slug:slug>/list', views.crud_list, name='crud_list'),
    path('<slug:slug>/list/filter', views.filter_crud_list, name='filter_crud_list'),
    path('<slug:slug>/create', views.crud_create_or_update, name='crud_create'),
    path('<slug:slug>/<int:id>/edit', views.crud_create_or_update, name='crud_update'),
    path('<slug:slug>/<int:id>/delete', views.crud_delete, name='crud_delete'),
    path('<slug:slug>/upload', views.upload, name='upload_file'),
]
    

