from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'scheduling_app'
urlpatterns = [
    path('', views.accounts_redirect_view, name='home'),
    path('about', views.home_view, name='about'),
    path('accounts/login', views.account_views.accounts_redirect_view, name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/select-account', views.account_views.select_account_view, name='accountSelect'),
    path('account/redirect-account', views.account_views.accounts_redirect_view, name='accountRedirects'),

    path('courses', views.course_table_view, name='courseTable'),
    path('schedules/student', views.student_schedules_view, name='studentSchedules'),
    path('schedules/advisor', views.advisor_schedules_view, name='advisorSchedules'),

    path('course/<int:course_pk>', views.course_view, name='courseDetail'),

    path('admin/testing-page', views.testing_page, name='testingPage')
]