from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('contract_requests', views.contract_requests_list, name='contract_requests_list'),
    path('speakers', views.speakers_list, name='speakers_list'),
    path('speakers/<int:speaker_id>/details', views.speaker_details, name='speaker_details'),
    path('disciplines', views.discipline_list, name='discipline_list'),
    path('schools/<int:school_id>/details', views.school_details, name='school_details')
]
