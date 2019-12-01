from django.urls import path
from . import views

urlpatterns = [
        # Directs to the index function in the views file
        path('', views.index, name='index'),
        # A new view would be called when URL matches 'photos/'
        path('photos/', views.PhotoListView.as_view(), name = 'photos'),
        ]
