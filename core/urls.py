from django.urls import path
from . import views
from .views import UserLoginView, SignUpView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tours/<int:tour_id>/edit/', views.edit_tour, name='edit_tour'),
    path('add-tour/', views.add_tour, name='add_tour'),
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]