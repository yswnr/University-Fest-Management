from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('events/', views.events_page, name='events'),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login/', views.login_page, name='login'),
    path('signup/<str:signup_option>/', views.signup_redirect, name='signup_redirect'),
    path('studentsignup/', views.signup_student, name='signup_student'),
    path('participantsignup/', views.signup_participant, name='signup_participant'),
    path('organizersignup/', views.signup_organizer, name='signup_organizer'),
    path('adminsignup/', views.signup_Admin, name='signup_admin'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('participant/dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('organizer/dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admindashboard/',views.admin_dashboard,name = 'admin_dashboard'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete_participant/<int:participant_id>/', views.delete_participant, name='delete_participant'),
    path('delete_organizer/<int:organizer_id>/', views.delete_organizer, name='delete_organizer'),
    path('register_hostel/', views.register_hostel, name='register_hostel'),
    # Add other URLs for your app if needed
]

