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
    url(r'/mhbhome.html$',
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

    url(r'/generieren$',
        active_and_login_required(
            active_and_login_required(views.GenerierenAuswahl.as_view())),
            name="modulhandbuchgenerieren"),
    
    url(r'/generieren/(?P<sg>[0-9]+)/(?P<td>[0-9]+)$',
        active_and_login_required(views.Generieren.as_view()),
        name="modulhandbuchgenerierenPDF"),

    ##### 
    # URLs for the various objects:
    # naming convention: the names of the URL patterns MUST
    # be the lower-case model names, with List or Detail appended.
    # else, autmatically going back to the right URLs in change_form
    # does not work
    
    url(r'/fachgebiet$',
        active_and_login_required(views.FachgebieteView.as_view()),
        name="fachgebietList"), 
    url(r'/fachgebiet/(?P<pk>[0-9]+)$',
        active_and_login_required(views.FachgebieteDetailView.as_view()),
        name="fachgebietDetail"),
    
    url(r'/lehreinheit$',
        active_and_login_required(views.LehreinheitenView.as_view()),
        name="lehreinheitList"),
    url(r'/lehreinheit/(?P<pk>[0-9]+)$',
        active_and_login_required(views.LehreinheitenDetailView.as_view()),
        name="lehreinheitDetail"),
    
    url(r'/lehrender$',
        active_and_login_required(views.LehrendeView.as_view()),
        name="lehrenderList"),
    url(r'/lehrender$',
        active_and_login_required(views.LehrendeView.as_view()),
        name="lehrender"),
    url(r'/lehrender/(?P<pk>[0-9]+)$',
        active_and_login_required(views.LehrendeDetailView.as_view()),
        name="lehrenderDetail"),

    
    url(r'/lehrveranstaltung$',
        active_and_login_required(views.LehrveranstaltungenView.as_view()),
        name="lehrveranstaltungList"),
    url(r'/lehrveranstaltung/(?P<pk>[0-9]+)$',
        active_and_login_required(views.LehrveranstaltungenDetailView.as_view()),
        name="lehrveranstaltungDetail"),

    
    url(r'/modul$',
        active_and_login_required(views.ModuleView.as_view()),
        name="modulList"), 
    url(r'/modul/(?P<pk>[0-9]+)$',
        active_and_login_required(views.ModuleDetailView.as_view()),
        name="modulDetail"),
    
    url(r'/organisationsform$',
        active_and_login_required(views.OrganisationsformView.as_view()),
        name="organisationsformList"),
    url(r'/organisationsform/(?P<pk>[0-9]+)$',
        active_and_login_required(views.OrganisationsformDetailView.as_view()),
        name="organisationsformDetail"),
    
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

    url(r'/texdatei$',
        active_and_login_required(views.TexDateienView.as_view()),
        name="texdateienList"), 
    url(r'/texdateien/(?P<pk>[0-9]+)$',
        active_and_login_required(views.TexDateienDetailView.as_view()),
        name="texdateienDetail"),

]

