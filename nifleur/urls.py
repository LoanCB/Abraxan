from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),

    path('parameters', views.parameters, name='parameters'),
    path('parameters/<str:model>/<int:object_id>/edit', views.edit_simple_form, name='edit_simple_form'),
    path('parameters/<str:model>/<int:object_id>/delete', views.delete_model_object, name='delete_model_object'),

    path('contract_requests', views.contract_requests_list, name='contract_requests_list'),
    path('contract_requests/new', views.create_contract_request, name='create_contract_request'),
    path('contract_requests/download', views.export_contract_requests, name='export_contract_requests'),
    path('contract_requests/<int:contract_id>/details', views.contract_request_detail, name='contract_request_detail'),
    path(
        'contract_requests/<int:contract_id>/details/<str:action>/',
        views.change_contract_status,
        name='change_contract_status'
    ),

    path('speakers', views.speakers_list, name='speakers_list'),
    path('speakers/<int:speaker_id>/details', views.speaker_details, name='speaker_details'),
    path('speakers/new', views.speaker_form, name='speaker_form'),

    path('disciplines', views.discipline_list, name='discipline_list'),

    path('schools', views.school_list, name='school_list'),
    path('schools/<int:school_id>/details', views.school_details, name='school_details'),

    path('companies', views.company_list, name='company_list'),
    path('companies/<int:company_id>/details', views.company_details, name='company_details')
]
