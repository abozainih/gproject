from django.urls import include, path
from . import views

urlpatterns = [
    path('list/', views.OrdersPendingListView.as_view(), name="orderlistpendingapi"),
]