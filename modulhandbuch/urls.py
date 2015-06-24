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
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic import TemplateView

from modulhandbuch import views

def active_and_login_required(function=None,
                              redirect_field_name=REDIRECT_FIELD_NAME,
                              login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_active,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



urlpatterns = [
    # TODO: figure out how to limit admin to certain applications
    # TODO: Namen auf modulnamen vereinhetlichen; das hilft bei den breadcrumbs!
    url(r'/mhbhome.html',
        active_and_login_required(
            TemplateView.as_view(template_name="mhome.html")),
        name="mhbhome"),
    url(r'/$',
        active_and_login_required(
            TemplateView.as_view(template_name="mhome.html")),
        name="modulhandbuch"),

    url(r'/ansehen$',
        active_and_login_required(
            TemplateView.as_view(template_name="ansehen.html")),
        name="modulhandbuchansehen"),

    ##### 
    # URLs for the various objects: 
    url(r'/fachgebiet$',
        active_and_login_required(views.FachgebieteView.as_view()),
        name="fachgebieteList"), 
    url(r'/fachgebiet/(?P<pk>[0-9]+)',
        active_and_login_required(views.FachgebieteDetailView.as_view()),
        name="fachgebieteDetail"),
    
    url(r'/lehreinheit$',
        active_and_login_required(views.LehreinheitenView.as_view()),
        name="lehreinheitenList"),
    url(r'/lehreinheit/(?P<pk>[0-9]+)$',
        active_and_login_required(views.LehreinheitenDetailView.as_view()),
        name="lehreinheitenDetail"),
    
    url(r'/lehrender$',
        active_and_login_required(views.LehrendeView.as_view()),
        name="lehrendeList"),
    url(r'/lehrender$',
        active_and_login_required(views.LehrendeView.as_view()),
        name="lehrender"),
    url(r'/lehrender/(?P<pk>[0-9]+)$',
        active_and_login_required(views.LehrendeDetailView.as_view()),
        name="lehrendeDetail"),

    
    url(r'/lehrveranstaltung$',
        active_and_login_required(views.LehrveranstaltungenView.as_view()),
        name="lehrveranstaltungenList"),
    url(r'/lehrveranstaltung/(?P<pk>[0-9]+)$',
        active_and_login_required(views.LehrveranstaltungenDetailView.as_view()),
        name="lehrveranstaltungenDetail"),

    
    url(r'/modul$',
        active_and_login_required(views.ModuleView.as_view()),
        name="moduleList"), 
    url(r'/modul/(?P<pk>[0-9]+)$',
        active_and_login_required(views.ModuleDetailView.as_view()),
        name="moduleDetail"),
    
    url(r'/organisationsform$',
        active_and_login_required(views.OrganisationsformView.as_view()),
        name="organisationsList"),
    url(r'/organisationsform/(?P<pk>[0-9]+)$',
        active_and_login_required(views.OrganisationsformDetailView.as_view()),
        name="organisationsDetail"),
    
    url(r'/pruefungsform$',
        active_and_login_required(views.PruefungsformView.as_view()),
        name="pruefungsformList"),
    url(r'/pruefungsform/(?P<pk>[0-9]+)$',
        active_and_login_required(views.PruefungsformDetailView.as_view()),
        name="pruefungsformDetail"),
    
    url(r'/studiengang$',
        active_and_login_required(views.StudiengangView.as_view()),
        name="studiengangList"),
    url(r'/studiengang/(?P<pk>[0-9]+)$',
        active_and_login_required(views.StudiengangDetailView.as_view()),
        name="studiengangDetail"),
    
    url(r'/focusarea$',
        active_and_login_required(views.FocusAreaView.as_view()),
        name="focusareaList"), 
    url(r'/focusarea/(?P<pk>[0-9]+)$',
        active_and_login_required(views.FocusAreaDetailView.as_view()),
        name="focusareaDetail"), 
]
