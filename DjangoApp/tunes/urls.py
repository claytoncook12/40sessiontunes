from django.urls import path, include
from tunes import views

app_name = 'tunes'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:id>/', views.detail, name='detail'),
    path('abc_combine/', views.abc_combine, name="abc_combine")
    #path('<int:id>/abc', views.abc, name='abc'),
]