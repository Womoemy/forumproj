"""classforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
# from django.urls import re_path
from forum import views
from accounts import views as accounts_views


urlpatterns = [
    path('', views.home, name='home'),
    path('forums/<int:pk>/', views.forum_topics, name='forum_topics'),
    path('forums/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('forums/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('forums/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name="reply_topic"),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # re_path(r'^$', views.home, name='home'),
    # re_path(r'^forums/(?P<pk>\d+)/$', views.forum_topics, name='forum_topics'),
    # re_path(r'^forums/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    # re_path(r'^signup/$', accounts_views.signup, name='signup'),
    path('admin/', admin.site.urls),
    
    
    path('reset/',
        auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
    
]
