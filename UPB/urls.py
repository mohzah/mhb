"""UPB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic import TemplateView

import UPB.views

admin.site.site_header = 'UPB Webanwendungen'

def active_and_login_required(function=None,
                              redirect_field_name=REDIRECT_FIELD_NAME,
                              login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_active,
        # lambda u: True,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# admin.autodiscover()

urlpatterns = [
    # TODO: figure out how to limit admin to certain applications 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django_auth_krb.views.krb_login'),
    url(r'^accounts/logout/$', 'django_auth_krb.views.krb_logout'),
    # url(r'^accounts/login/$', auth_views.login),
    # url(r'^accounts/logout/$', auth_views.logout),
    url(r'^$',
        active_and_login_required(
            TemplateView.as_view (template_name='home.html')),
        name="home"),
    url(r'^modulhandbuch', include('modulhandbuch.urls')),

    url(r'^media/(?P<filename>.*)/$',
        UPB.views.serveGeneratedFiles.as_view(),
        name="media")
]
