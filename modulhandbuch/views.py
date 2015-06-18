from django.shortcuts import render
from django.core.exceptions import FieldDoesNotExist

from django.views.generic import View, ListView, DetailView

import models

# Create your views here.


class SimpleListView(ListView):
    """A simple version of ListView. It tries to construct
    all relevant data for the template from the class itself
    and the meta data inside the class.
    Additionally, it also looks at editing permissions for a class,
    based on the logged in user and the model's objects' can_edit function.
    """

    modelname = None
    title = None
    template_name = "modulhandbuch/generic_list.html"

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(SimpleListView, self).get_context_data(**kwargs)

        try:
            editpermissions = [x.can_edit(self.request.user)
                               for x in context['object_list']]
        except:
            # just to make sure we behave reasonably if the model
            # does not implement can_edit
            editpermissions = [False] * len(context['object_list'])

        context['object_list'] = zip(context['object_list'],
                                     editpermissions)

        # Add in a QuerySet of all the books
        context['modelname'] = (self.modelname
                                if self.modelname
                                else self.model.__name__)

        context['title'] = (self.title
                            if self.title
                            else self.model._meta.verbose_name_plural)

        print context
        return context


class FachgebieteView(SimpleListView):
    model = models.Fachgebiet


class LehreinheitenView(SimpleListView):
    model = models.Lehreinheit


class LehrendeView(SimpleListView):
    model = models.Lehrender


class LehrveranstaltungenView(SimpleListView):
    model = models.Lehrveranstaltung


class ModuleView(SimpleListView):
    model = models.Modul


class OrganisationsformView(SimpleListView):
    model = models.Organisationsform


class PruefungsformView(SimpleListView):
    model = models.Pruefungsform


class StudiengangView(SimpleListView):
    model = models.Studiengang


class FocusAreaView(SimpleListView):
    model = models.FocusArea


#########################################
# Views for the detailed disaply of an entry

class SimpleDetailView(DetailView):
    """A simple view to construct a per-object detail view.
    Similar to SimpleListView, it tries to grab meta data from the class.
    It wants to be told which fields to display.
    """

    template_name = "modulhandbuch/generic_detail.html"
    display_fields = []
    title = ""
    modelname = ""

    def get_context_data(self, **kwargs):
        context = super(SimpleDetailView, self).get_context_data(**kwargs)

        context['title'] = (self.title
                            if self.title
                            else self.model._meta.verbose_name)
        try:
            context['title2'] = (self.model._meta.get_field("nameDe")
                                 .value_to_string(self.object))
        except:
            context['title2'] = ""

        context['modelname'] = (self.modelname
                                if self.modelname
                                else self.model.__name__)
            
        # figure out which fields, precedence:
        # - given by the view subclass
        # - by the models meta class
        # - all fields
        
        if not self.display_fields:
            try: 
                self.display_fields = self.model.display_fields
            except:
                # this is basically a fail, since nothing will be displayed :-(
                # but grabbing all fields makes little sense, since
                # plenty of internal fields would be displayed as well
                self.display_fields = []

        context['fields'] = []
        for  f in self.display_fields:
            try: 
                vn = self.model._meta.get_field(f).verbose_name
            except FieldDoesNotExist:
                continue
            
            helptext = self.model._meta.get_field(f).help_text

            # getting the value is a bit more complex:
            at = getattr(self.object, f)
            
            try:
                val = at.__unicode__()
            except:
                val = at

            if ( (val is None) or
                 (val == "")):
                val = "--"

            context['fields'].append( (vn, val, helptext ))

        return context


class FachgebieteDetailView(SimpleDetailView):
    model = models.Fachgebiet


class LehreinheitenDetailView(SimpleDetailView):
    model = models.Lehreinheit


class LehrendeDetailView(SimpleDetailView):
    model = models.Lehrender


class LehrveranstaltungenDetailView(SimpleDetailView):
    model = models.Lehrveranstaltung


class OrganisationsformDetailView(SimpleDetailView):
    model = models.Organisationsform


class PruefungsformDetailView(SimpleDetailView):
    model = models.Pruefungsform


class ModuleDetailView(SimpleDetailView):
    model = models.Modul
    
    def get_context_data(self, **kwargs):
        context = super(ModuleDetailView, self).get_context_data(**kwargs)

        # get all the lehrveranstaltungen via the intermediary
        # work around; _set seems to have issues with inheritance :-(
        veranstaltungslps = models.VeranstaltungsLps.objects.filter(
            modul=self.object)
        
        for lvlps in veranstaltungslps:
            context['fields'].append(
                ( "VL " + lvlps.veranstaltung.__unicode__(),
                  lvlps.lp,
                  "Anzahl LPs in diesem Modul",
              )
            )

        return context


class FocusAreaDetailView(SimpleDetailView):
    model = models.FocusArea

    def get_context_data(self, **kwargs):
        context = super(FocusAreaDetailView, self).get_context_data(**kwargs)

        for m in self.object.module.all():
            context['fields'].append(
                ('Modul',
                 m.__unicode__(),
                 ''
                )
            )
        
        return context


class StudiengangDetailView(SimpleDetailView):
    model = models.Studiengang
    # TODO: list foriegn keys 

    def get_context_data(self, **kwargs):
        context = super(StudiengangDetailView, self).get_context_data(**kwargs)

        for m in self.object.module.all():
            context['fields'].append(
                ('Modul',
                 m.__unicode__(),
                 ''
                )
            )
        
        for m in self.object.focusareas.all():
            context['fields'].append(
                ('Studienrichtung',
                 m.__unicode__(),
                 ''
                )
            )
            
        return context
    
