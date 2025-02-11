from django.urls import path
from .views import home, list_elections, vote, results, login_view, register_view, logout_view
from .views import delete_election
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('elections/', list_elections, name='list_elections'),
    path('vote/<int:election_id>/', vote, name='vote'),
    path('results/<int:election_id>/', results, name='results'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('delete_election/<int:election_id>/', delete_election, name='delete_election'),
     path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='voting/password_reset.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='voting/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='voting/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='voting/password_reset_complete.html'), 
         name='password_reset_complete')
]
