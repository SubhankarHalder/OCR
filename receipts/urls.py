from django.urls import path
from . import views
from receipts.views import PhotoRest

urlpatterns = [
        # Directs to the index function in the views file
        path('', views.index, name='index'),
        # A new view would be called when URL matches 'photos/'
        path('photos/', views.PhotoListView.as_view(), name = 'photos'),
        # API path
        path('api', PhotoRest.as_view() ),
        ]
