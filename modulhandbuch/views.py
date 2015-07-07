# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist

from django.views.generic import View, TemplateView, ListView, DetailView

import models

import tempfile

import jinja2

import codecs, os, subprocess, shutil, re

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


class TexDateienView(SimpleListView):
    model = models.TexDateien

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


class TexDateienDetailView(SimpleDetailView):
    model = models.TexDateien


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



class GenerierenAuswahl(TemplateView):
    template_name = "generieren.html"

    def get_context_data(self, **kwargs):
        print "in contetx data von GenerierenAuswahl"
        context = super(GenerierenAuswahl, self).get_context_data(**kwargs)

        context['files'] = [
            (sg, [tex
                  for tex in sg.startdateien.all()
                  # if tex.is_start_file()
              ], )
            for sg in models.Studiengang.objects.all()]
        print context['files']

        return context


class Generieren(TemplateView):
    template_name = "generatedPDFs.html"

    def runLatex(self, fn, tempDir):
        """
        Run pdflatex twice on filename; return suitable error codes
        """

        retval = {}
        try:
            # run PDF twice:
            retval['output'] = subprocess.check_output (['pdflatex',
                                                         '-interaction=nonstopmode',
                                                         fn],
                                                        stderr=subprocess.STDOUT,
                                                        cwd = tempDir
                                                        )

            retval['output'] = subprocess.check_output (['pdflatex',
                                                         '-interaction=nonstopmode',
                                                         fn],
                                                        stderr=subprocess.STDOUT,
                                                        cwd = tempDir
                                                        )
            retval['returncode'] = 0
            retval['pdf'] = re.sub ('.tex$', '', fn) + '.pdf'
        except subprocess.CalledProcessError as e:
            retval['output'] = e.output
            retval['cmd'] = e.cmd
            retval['returncode'] = e.returncode

        return retval

    def renderTexdateiObj(self, tmpdir, texdateien,
                          studiengang, startdatei,
                          ):
        """Take a list of texdatei objects and turn them
        into a tex file in the file system. 
        Only hit the database once
        """

        error = []

        latex_renderer = jinja2.Environment(
            comment_start_string="{###",
            comment_end_string="###}",
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        ######################
        # Databae retrieval: 
        # pass in all the generic data, not related to
        # the concrete studiengang
        _lehreinheiten = models.Lehreinheit.objects.all()
        _fachgebiete = models.Fachgebiet.objects.all()
        _pruefungsformen = models.Pruefungsform.objects.all()
        _organisationsformen = models.Organisationsform.objects.all()
        _lehrende = models.Lehrender.objects.all()
        _studiengaenge = models.Studiengang.objects.all()

        # for module, focusarea and lehrveranstaltungen: pass only
        # those objects into the rendered that actually pertain to the
        # desired studiengang
        # (the "all" versions are just to ease testing)
        
        _module = models.Modul.objects.filter(studiengang__id=studiengang.id)
        
        _focusareas=models.FocusArea.objects.filter(studiengang__id=studiengang.id)

        # more complicated for the lehrveranstaltungen,
        # since we have to go via the modules first
        _vlpsQs = models.VeranstaltungsLps.objects.filter(modul__in=_module)
        _lehrveranstaltungen = models.Lehrveranstaltung.objects.filter(veranstaltungslps__in=_vlpsQs).distinct()

        ##########################
        # call the renderer for all files in the list
        for texdateiObj in texdateien:
            try:
                f = codecs.open(
                    os.path.join(
                        tmpdir,
                        texdateiObj.filename),
                    'w', 'utf-8')

                ltemplate = latex_renderer.from_string(texdateiObj.tex)

                # stuff in all the relevant models so that the template
                # can iterate over it:

                # lehrveranstaltungen = [l for l in
                #                        models.lehrveranstaltungen.objects.all()]

                r = ltemplate.render(
                    lehreinheiten=_lehreinheiten,
                    fachgebiete=_fachgebiete,
                    pruefungsformen=_pruefungsformen,
                    organisationsformen=_organisationsformen,
                    lehrende=_lehrende,
                    module=_module,
                    focusareas=_focusareas,
                    lehrveranstaltungen=_lehrveranstaltungen,
                    studiengaenge=_studiengaenge,
                    studiengang=studiengang,
                    startdatei=startdatei,
                )


                f.write(r)
                f.close()

            except jinja2.TemplateSyntaxError as e:
                # print e.message
                # print e.lineno
                error.append(texdateiObj.filename +
                             ': Template Syntax Error, ' +
                             e.message + " at line " + str(e.lineno))
            except jinja2.TemplateAssertionError as e:
                error.append(texdateiObj.filename +
                             ': Template Assertion Error, ' +
                             e.message + " at line " + str(e.lineno))
            except Exception as e:
                error.append(texdateiObj.filename +
                             ': something went wrong; generic exception - ' +
                             str(e))

        return error

    def generatePdf(self, tmpdir, destDir, startdateien):
        """Take a list  texdatei object,
        run them though latex,
         and produce a PDF file. Copy the file to MEDIA_DIR.
         Return a path name/  link (?) to the produced file.
        """

        # we store all the produced paths in here:
        pdfs = []

        # a list of error messages, to render in the template:
        error = []

        # run pdflatex on the produced tex file
        for texdateiObj in startdateien:
            res = {'name': texdateiObj.filename}
            if texdateiObj.is_start_file():
                retval = self.runLatex(texdateiObj.filename, tmpdir)
            else:
                retval = {}
                retval['returncode'] = -1
                retval['cmd'] = "Keine Ausführung von pdflatex, da kein documentclass"
                retval['output'] = ""

            if retval['returncode'] is not 0:
                error = ("Command {} failed with returncode: {} and output {}"
                         .format(retval['cmd'],retval['returncode'],retval['output'],
                             ))
                res['pdf'] = ""
            else:
                # copy the produced PDF file to the destination
                shutil.copyfile(os.path.join(tmpdir, retval['pdf']),
                                os.path.join(destDir, retval['pdf']))
                res['pdf'] = settings.MEDIA_URL + "modulhandbuch/" + retval['pdf']

            pdfs.append(res)
        # as well as an archive
        tmp = os.path.splitext(os.path.basename(texdateiObj.filename))[0]
        archivename = os.path.join(
            destDir,
            tmp,
        )

        print "destDir: ", destDir
        print "archieve name: ", archivename

        archive = shutil.make_archive(
            base_name=archivename,
            format='zip',
            root_dir=tmpdir,
        )

        # TODO: make the URL to the archiv more meaningful
        archivepath = (settings.MEDIA_URL + "modulhandbuch/archiv.zip")
        
        return (pdfs, archivepath, error)

    def get_context_data(self, **kwargs):

        print "in generieren view", kwargs

        globalerror = []

        context = super(Generieren, self).get_context_data(**kwargs)

        # we need a studiengang and its desired start file;
        # it only makes sense together (typically, one-to-one,
        # but could be multiple


        # get the queryset for the texdatiener to look into

        try:
            studiengang = kwargs['sg']
            sgObj = models.Studiengang.objects.get(pk=int(studiengang))
        except Exception as e:
            print e
            globalerror += ["Studiengang nicht gefunden"]
            
        if globalerror:
            context['globalerror'] = globalerror
            return context
            
        try:
            texdatei = kwargs['td']
            startdateien = models.TexDateien.objects.filter(pk=int(texdatei))
        except Exception as e:
            # this is not necessarily an error; means the user
            # wants to run on all the startdatei of 
            startdateien = sgObj.startdateien.all()
            

        #######
        # we found all input data

        # find a temporary directory
        tmpdir = tempfile.mkdtemp(suffix="modulhandbuch")

        # make sure the desctination directory exists
        destDir = os.path.join(settings.MEDIA_ROOT, "modulhandbuch")
        try:
            os.makedirs(destDir)
        except:
            pass
            # TODO: check for file exists exception only

        ##########
        # generate all the latex files for that studiengang
        # actually, we simplify here: we just run the renderer
        # on ALL Texdateien. Not the most efficient thing to do,
        # but much easier than trying to figure out with
        # files are inlined by the startdateien
            
        globalerror += self.renderTexdateiObj(
            tmpdir,
            models.TexDateien.objects.all(),
            sgObj, startdateien,
        )

        if globalerror:
            context['globalerror'] = globalerror
            return context

        # run pdflatex on the chosen startfile and copy into media directory
        # limiting to files with documnetclass in them: mostly a debugging aid
        pdfs, archivepath, globalerror = self.generatePdf(tmpdir, destDir, startdateien)


        # delete temp directoy and content
        shutil.rmtree(tmpdir, ignore_errors=True)

        # collect all the results in context and return 
        context['globalerror'] = globalerror
        context['pdfs'] = pdfs
        context['tdObj'] = startdateien
        context['sgObj'] = sgObj
        context['archivepath'] = archivepath
        
        return context
