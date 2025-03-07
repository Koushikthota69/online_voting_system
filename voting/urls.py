from django.urls import path
from .views import home, list_elections, vote, results, login_view, register_view, logout_view
from .views import delete_election
from django.contrib.auth import views as auth_views
from . import views
from .views import update_profile


urlpatterns = [
    path('', home, name='home'),
    path('elections/', list_elections, name='list_elections'),
    path('vote/<int:election_id>/', vote, name='vote'),
    path('results/<int:election_id>/', results, name='results'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('delete_election/<int:election_id>/', delete_election, name='delete_election'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="voting/password_reset.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="voting/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="voting/password_reset.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="voting/password_reset_done.html"), name="password_reset_complete"),
    path('update_profile/', update_profile, name='update_profile')

]