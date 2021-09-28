from django.urls import path, include
from tunes import views

app_name = 'tunes'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('abc_combine/', views.abc_combine, name="abc_combine"),
    path('ref/<int:pk>', views.detail_audio_ref, name="detail_audio_ref"),
    #path('<int:id>/abc', views.abc, name='abc'),
]