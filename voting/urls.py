from django.urls import path
from .views import home, list_elections, vote, results, login_view, register_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('elections/', list_elections, name='list_elections'),
    path('vote/<int:election_id>/', vote, name='vote'),
    path('results/<int:election_id>/', results, name='results'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
