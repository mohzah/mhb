# -*- coding: utf-8 -*-


from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from modulhandbuch.models import *

import re

# Option with easy_select2:
from easy_select2 import select2_modelform

############

def user_unicode(self):
    return  u'%s (%s, %s)' % (self.username, self.last_name, self.first_name)

User.__unicode__ = user_unicode

admin.site.unregister(User)
admin.site.register(User)

##############

def restrict_form(uneditable, admin_class, self, request, obj=None, **kwargs):
    '''
    helper function to remove the fields that are not editable by Non-owner users from the form
    :param uneditable: a list of fields uneditable by the editors and only editable by owner or superuser
    :param admin_class:
    :param self: ModelAdmin object, an object of the admin_class
    :param request: HTTP request obj
    :param obj:
    :param kwargs:
    :return:
    '''
    try:
        editors = obj.editors.all()
        adding_new_obj = False
    except AttributeError as e:
        adding_new_obj = True
        print 'exception'

    # print 'adding new obj', adding_new_obj
    if adding_new_obj:
        # has access to all fields
        pass
    elif request.user.is_superuser or request.user == obj.owner:
        # has access to all fields
        pass
    elif request.user in editors:
        self.fields = [field for field in self.fields if field not in uneditable]

    return super(admin_class, self).get_form(request, obj, **kwargs)

#########################################################

## a basic admin to add ownership

class OwnedAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        res = super(OwnedAdmin, self).__init__(*args, **kwargs)

        # self.realInlines = self.inlines

        # construct the field names to show:
        tmp = [f.name for f in self.model._meta.fields]
        # print "admin: ", self.__class__, tmp
        # print "admin_fields: ", self.model.admin_fields
        try:
            tmp.remove('id')
            # tmp.remove('owner')
            tmp.remove('namedentity_ptr')
            tmp.remove('slug')
        except:
            # not all fields might be in all modules,
            # but that is not a problem
            pass
        self.fields = tmp + self.model.admin_fields + ['editors', ]

        # print "init owned admin: ", self, self.fields

        return res

    def get_queryset(self, request):
        """Get objects that the logged-in user is allowed to edit. 
        Could be as owner, superuser, or by being part of editors
        """
        
        qs = super(OwnedAdmin, self).get_queryset(request)

        # print "admin get_qs: ", qs
        
        if request.user.is_superuser:
            return qs

        qs = qs.filter(Q(owner=request.user) |
                         Q(editors__in = [request.user])
                         ).distinct()

        # print "admin get_qs 2: ", qs
        
        return qs
    
    def save_model(self, request, obj, form, change):
        # print "--------------"
        # print "in save_model: ", obj, obj.owner, change, request.user

        if (change is False) or (obj.owner is None):
            obj.owner = request.user
        obj.save()

    # TODO:
    # die folgenden Funktionen werden eigentlich nicht gebraucht,
    # wenn über get_queryset auf owner eingeschröänkt wird.
    # Es kann trotzdem nicht schaden, falls jemand direkt die URL manipuliert
    # es fehlt hier noch die has_change_permission!

    def has_delete_permission(self, request, obj=None):
        # print "has delete: ", obj, request.user, request.user.is_superuser
        if obj:
            if ((request.user.is_superuser) or
                (obj.owner == request.user)):
                return True

        return False

    def get_readonly_fields(self, request, obj=None):
        # print "grof: ", request, request.user, obj, obj.owner if obj else "N/A"

        tmp = self.readonly_fields
        # print "readonly: ", tmp

        if (obj
            and not (obj.owner == request.user)
            and not (request.user in obj.editors.all())
            and not request.user.is_superuser):
            # print "setting fields readonly"
            # then add further read-only fields, actually, all of them
            # tmp = tmp + self.not_owner_readonly_fields
            tmp = list(tmp) + [f.name for f in self.model._meta.fields]

            # show a message here?
            self.message_user(request,
                              u"Sie dürfen diesen Eintrag nicht editieren!",
                              )

        # print "readonly_fields: ", tmp
        return tmp

    # attempt to get the inlines as read-only as well:

    # def get_formsets_with_inlines(self, request, obj=None):
    #     for inline in self.get_inline_instances(request, obj):
    #         yield inline.get_formset(request, obj), inline

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     obj = self.model.objects.get(pk=object_id)
    #     print "in change_veiw ", obj

    #     # if obj and not (obj.owner == request.user):
    #     #     print "disable editing of inlines"
    #     #     self.inlines = []

    #     return super(OwnedAdmin, self).change_view(request,
    #                                                object_id,
    #                                                form_url, extra_context)

    # override the HttpResponse hooks:
    def my_response_url(self, request, obj):
        # redirect back to the survey page for this model
        try:
            urlname = obj.__class__.__name__.lower() + "List"
            url = reverse(urlname)
        except:
            # this exception should only happen if the url names
            # dont match the expected patterns
            url = reverse("modulhandbuchansehen")

        return url

    def response_change(self, request, obj):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(self.my_response_url(request, obj))
        else:
            return super(OwnedAdmin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):

        if '_continue' not in request.POST:
            # since no object exists, it is harder to find out the class
            # let's detour via the URL 
            r = re.match('.*/modulhandbuch/([^/]*)/.*', request.path)
            urlname = r.group(1) + 'List'
            return HttpResponseRedirect(reverse(urlname))
        else:
            return super(OwnedAdmin, self).response_delete(request,
                                                       obj_display, obj_id) 

    def response_add(self, request, obj, post_url_continue=None):
        if '_continue' not in request.POST:
            return HttpResponseRedirect(self.my_response_url(request, obj))
        else:
            return super(OwnedAdmin, self).response_add(request,
                                                        obj, post_url_continue)

ModulForm = select2_modelform(Modul, attrs={'width': '250px'})


#########################################################

# inlines that understand whether they should be editable

class OwnedInline(admin.TabularInline):

    pass


class ModulLVInline(OwnedInline):
    model = VeranstaltungsLps
    # TODO: select2_modelform zeigt alle möglichen keys an,
    # in einem ersten select field, das gart nicht angezeigt
    # werden sollte. Das ist ein killer bug :-(

    # form = select2_modelform(FocusArea, attrs={'width': '250px'})
    fk_name = "modul"
    # fields = ['veranstaltung', 'lp', 'prufungsleistung', 'studienleistung', 'status']
    fields = ['veranstaltung', 'lp', 'prufungsleistung', 'sl_qt', 'status', 'form', 'dauer_umfang']
    readonly_fields = ['modul']
    verbose_name = "Lehrveranstaltung (und LP) in diesem Modul"
    verbose_name_plural = "Lehrveranstaltungen (und LPs) in diesem Modul"

    # def has_delete_permission(self, request, obj=None):
    #     if obj:
    #         print "Modul inlinline: ", request.user, obj, type(obj)
    #         if ((request.user == obj.owner) or
    #             (request.user.is_superuser)):
    #             return True
    #         else:
    #             return False
    #     else:
    #         return True
    #     pass



###############################
# patch the classes together


# class FocusAreaModulInline(admin.TabularInline):
#
#     model = FocusArea.module.through


# class FocusAreaAdmin(OwnedAdmin):
#     # inlines = [FocusAreaModulInline]
#
#     form = select2_modelform(FocusArea, attrs={'width': '250px'})
#
#     # fields = [ 'url', 'nameDe', 'nameEn',
#     #            'module',
#     #            'beschreibungDe', 'beschreibungEn',
#     #            'verantwortlicher',
#     #            'editors']
#     pass

# class StudiengangFocusAreaInline(admin.TabularInline):
#     model = Studiengang.focusareas.through
#     verbose_name = "Focus Area dieses Studiengangs"
#     verbose_name_plural = "Focus Areas dieses Studiengangs"

class StudiengangModuleInline(admin.TabularInline):
    model = Studiengang.module.through
    verbose_name = "Studiengangs dieses Modul"
    verbose_name_plural = "Studiengangs dieses Modul"


class PrufungsleistungAdmin(OwnedAdmin):
    model = Prufungsleistung
    verbose_name = u"Prüfungsleistung"
    form = select2_modelform(Prufungsleistung, attrs={'width': '250px'})


# class StudienleistungAdmin(OwnedAdmin):
#     model = Studienleistung
#     verbose_name = 'Studienleistung / qualifiziere Teilnahme'
#     form = select2_modelform(Studienleistung, attrs={'width': '250px'})


class StudiengangAdmin(OwnedAdmin):
    model = Studiengang
    form = select2_modelform(Studiengang, attrs={'width': '250px'})
    
    fields = ['nameDe', 'nameEn',
              'url',
              'beschreibungDe', 'beschreibungEn',
              'verantwortlicher',
              'startdateien',
             ]
    # inlines = [#StudiengangFocusAreaInline,
    #            StudiengangModuleInline]
    pass


class ModulAdmin(OwnedAdmin):
    form = ModulForm
    inlines = [ModulLVInline, StudiengangModuleInline]
    form = select2_modelform(Modul, attrs={'width': '250px'})

    def get_form(self, request, obj=None, **kwargs):
        uneditable = ['nameEn', 'nameDe', 'nummer', 'workload', 'credits', 'haufigkeit', 'dauer', 'gruppengrosse', 'verwendung', 'voraussetzungen']
        return restrict_form(uneditable, ModulAdmin, self, request, obj, **kwargs)


class LehrenderAdmin(OwnedAdmin):
    model = Lehrender
    form = select2_modelform(Lehrender, attrs={'width': '250px'})



class LehrstuhlAdmin(OwnedAdmin):
    model = Lehrstuhl
    form = select2_modelform(Lehrstuhl, attrs={'width': '250px'})


# class LehreinheitAdmin(OwnedAdmin):
#     model = Lehreinheit
#     form = select2_modelform(Lehreinheit, attrs={'width': '250px'})


class PruefungsformAdmin(OwnedAdmin):
    model = Pruefungsform
    form = select2_modelform(Pruefungsform, attrs={'width': '250px'})


class OrganisationsformAdmin(OwnedAdmin):
    model = Organisationsform
    form = select2_modelform(Organisationsform, attrs={'width': '250px'})


class NichtfachlicheKompetenzAdmin(OwnedAdmin):
    model = NichtfachlicheKompetenz
    form = select2_modelform(NichtfachlicheKompetenz, attrs={'width': '250px'})


class LehrveranstaltungAdmin(OwnedAdmin):
    model = Lehrveranstaltung
    form = select2_modelform(Lehrveranstaltung, attrs={'width': '250px'})
    # exclude = ('interneBemerkung',)   # doesn't work for interneBemerkung
    # exclude = ('beschreibungDe', 'beschreibungEn')

    def get_form(self, request, obj=None, **kwargs):
        uneditable = ['nameEn', 'nameDe', 'kontaktzeit', 'termin', 'sprache', 'lv_nr', 'ects', 'swsPraktikum',
                      'zielsemester', 'verantwortlicher', 'englishsprachige']
        return restrict_form(uneditable, LehrveranstaltungAdmin, self, request, obj, **kwargs)
        # uneditable = ['weiterfuehrende']
        # superuser_fields = self.fields
        # normaluser_fields = [field for field in self.fields if field not in uneditable]
        # if request.user.is_superuser or obj.owner == request.user:
        #     self.fields = superuser_fields
        # elif request.user in obj.editors.all():
        #     self.fields = normaluser_fields
        #
        # return super(LehrveranstaltungAdmin, self).get_form(request, obj, **kwargs)

####################

# admin.site.register(Lehreinheit, LehreinheitAdmin)
admin.site.register(Lehrstuhl, LehrstuhlAdmin)
admin.site.register(Lehrender, LehrenderAdmin)
admin.site.register(Pruefungsform, PruefungsformAdmin)
admin.site.register(Organisationsform, OrganisationsformAdmin)
admin.site.register(NichtfachlicheKompetenz, NichtfachlicheKompetenzAdmin)
admin.site.register(Lehrveranstaltung, LehrveranstaltungAdmin)
admin.site.register(Prufungsleistung, PrufungsleistungAdmin)
# admin.site.register(Studienleistung, StudienleistungAdmin)
# admin.site.register(Prufungsleistung)
admin.site.register(Modul, ModulAdmin)
# admin.site.register(FocusArea, FocusAreaAdmin)
admin.site.register(Studiengang, StudiengangAdmin)
admin.site.register(TexDateien)
admin.site.register(VeranstaltungsLps)
admin.site.register(Moduletype)
