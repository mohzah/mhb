# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages


from django.views.generic import View, TemplateView, FormView, ListView, DetailView

from django.db.models import Q

from django.shortcuts import redirect

import django.db.models.fields.related as fieldsRelated

from django.contrib.contenttypes.models  import ContentType

import models
import forms
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

        # print context
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


class NichtfachlicheKompetenzView(SimpleListView):
    model = models.NichtfachlicheKompetenz


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
                thisfield = self.model._meta.get_field(f)
            except FieldDoesNotExist:
                continue

            helptext = self.model._meta.get_field(f).help_text

            # let's get the value of this field.
            # We need to be mindful of many-to-many fields here,
            # as getattr seems to return a manager object here?


            try:
                val = None
                if isinstance(thisfield, fieldsRelated.ManyToManyField):
                    val = ', '.join([x.__unicode__() for x in  getattr(self.object, f).all()])
                else:
                    # print "ordinary field"
                    val = getattr(self.object, f)
            except Exception as e:
                print e
                val = ""

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


class NichtfachlicheKompetenzDetailView(SimpleDetailView):
    model = models.NichtfachlicheKompetenz


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
        # print "in contetx data von GenerierenAuswahl"
        context = super(GenerierenAuswahl, self).get_context_data(**kwargs)

        context['files'] = [
            (sg, [tex
                  for tex in sg.startdateien.all()
                  # if tex.is_start_file()
              ], )
            for sg in models.Studiengang.objects.all()]
        # print context['files']

        return context



def runLatex(fn, tempDir, twice=True):
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

        if twice:
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

    
class Generieren(TemplateView):
    template_name = "generatedPDFs.html"

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
        _lehrende = models.Lehrender.objects.all()
        _studiengaenge = models.Studiengang.objects.all()

        # for module, focusarea and lehrveranstaltungen: pass only
        # those objects into the rendered that actually pertain to the
        # desired studiengang
        # (the "all" versions are just to ease testing)
        
        _focusareas = models.FocusArea.objects.filter(
            studiengang__id=studiengang.id)

        # build the Q object for getting all the modules that either 
        # - are in the Studiengang itself, mentioned directly, or
        # - are part of one of the studiengang's focusareas
        q = Q(studiengang__id=studiengang.id)
        for fa in _focusareas:
            q = q | Q(focusarea=fa)
            
        _module = models.Modul.objects.filter(q).distinct()
        # old: _module = models.Modul.objects.filter(studiengang__id=studiengang.id)

        # more complicated for the lehrveranstaltungen,
        # since we have to go via the modules first
        _vlpsQs = models.VeranstaltungsLps.objects.filter(modul__in=_module)
        _lehrveranstaltungen = models.Lehrveranstaltung.objects.filter(
            veranstaltungslps__in=_vlpsQs).distinct()

        # and limit other entities:
        _pruefungsformen = models.Pruefungsform.objects.filter(
            modul__in=_module).distinct()
        _organisationsformen = models.Organisationsform.objects.filter(
            modul__in=_module).distinct()
        _nichtfachlichekompetenzen = models.NichtfachlicheKompetenz.objects.filter(
            lehrveranstaltung__in=_lehrveranstaltungen).distinct()
        
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
                    nichtfachlichekompetenzen=_nichtfachlichekompetenzen,
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

        os.symlink(os.path.join(settings.MEDIA_ROOT,
                                'figures'),
                   os.path.join(tmpdir,
                                'figures'))


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
                retval = runLatex(texdateiObj.filename, tmpdir)
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

        # print "destDir: ", destDir
        # print "archieve name: ", archivename

        archive = shutil.make_archive(
            base_name=archivename,
            format='zip',
            root_dir=tmpdir,
        )

        # TODO: make the URL to the archiv more meaningful
        archivepath = (settings.MEDIA_URL+
                       "modulhandbuch/" +
                       tmp+".zip")

        return (pdfs, archivepath, error)

    def get_context_data(self, **kwargs):

        # print "in generieren view", kwargs

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
            # print e
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

class AbbildungenView(ListView):
    """Display a list of figures from a directory.
    Allow delete, add new one. No database storage.
    """

    template_name = "abbildungen.html"

    def get_queryset(self):
        r = os.listdir(os.path.join(settings.MEDIA_ROOT,
                                       'figures',)
                      )
        # filter out the thumbnails
        r = [x
             for x in r
             if not x.endswith("-thumbnail.png")]
        
        # provide separate entries for the file itself and a thumbnail
        r = [ (x,
               x[:-4] + "-thumbnail.png" if x.endswith('.pdf') else x)
              for x in r
          ] 
        
        return r

class AbbildungenAddView(FormView):

    form_class = forms.UploadAbbildung
    template_name = "abbildungAdd.html"
    # TODO: check why reversing hte URL does not work
    # success_url = reverse_lazy("abbildungenList")
    success_url = "modulhandbuch/abbildung"

    def form_valid(self, form):
        f = self.request.FILES['file']

        # write the file to disk:
        destname = os.path.join(settings.MEDIA_ROOT,
                                'figures',
                                f.name)
        with open(destname,
                  'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        # should we convert a PDF to a bitmap for previews?
        if f.name.endswith('.pdf'):
            thumbname = os.path.join(
                settings.MEDIA_ROOT,
                'figures',
                f.name[:-4] + "-thumbnail.png")

            # call convert
            try:
                r = subprocess.check_output(
                    ['convert',
                     destname,
                     thumbname],
                    stderr=subprocess.STDOUT,
                )
            except subprocess.CalledProcessError as e:
                print "convert failed: ", e
                pass

        return super(AbbildungenAddView, self).form_valid(form)

class AbbildungenDeleteView(View):
    """Simple, direct delete. Change this to a confirmation dialog"""

    def get(self, request, filename):
        """delete filename in media root, figures"""
        fullfilename = os.path.join(
            settings.MEDIA_ROOT,
            'figures',
            filename
        )

        os.remove(fullfilename)
        
        return redirect("modulhandbuch/abbildung")


class LatexCheckView(View):
    """Go over all relevant objects and run a simple latex check on them"""


    def run_latex(self, element, tmpdir):
        """Write to temporary directory, run latex, 
        grab the result."""

        # which fields to write? lket's try the display_fields
        tmpbody = []
        for l in element.display_fields:
            val = getattr(element, l) 
            try:
                val = val.__unicode__()
            except:
                val = unicode(val)

            tmpbody.append(u"Feld: {} \n\n{}".format(l, val))
                
        body = u'\n\n'.join(tmpbody)

        # create the actual tex document:
        tex = (r"""
\documentclass{article}
\usepackage{booktabs}
\usepackage{paralist}
\usepackage{xtab}
\usepackage{calc}
\usepackage{url}
\usepackage[utf8]{inputenc}
\usepackage[table]{xcolor}
\usepackage[ngerman]{babel}
\usepackage{graphicx}
\usepackage{mdframed}
\usepackage[export]{adjustbox}
\begin{document}
""" + body +
"""
\end{document}
""")

        print tmpdir 
        f = codecs.open(
                    os.path.join(
                        tmpdir,
                        'main.tex'),
                    'w', 'utf-8')
        f.write(tex)
        f.close()

        retval = runLatex ('main.tex', tmpdir, twice=False)
        
        return (retval['returncode'],
                retval['output'])
        
    def get(self, request):

        tmpdir = tempfile.mkdtemp(suffix="modulhandbuch")
        
        result = {}
        classes_to_check = [
            models.Lehrveranstaltung,
            models.Modul,
            models.FocusArea,
            models.Studiengang,
        ]

        for c in classes_to_check:
            elements = []
            for el in c.objects.all():
                returncode, error = self.run_latex (el, tmpdir)
                elements.append({
                    'el': el,
                    'returncode': returncode,
                    'error': error,
                })
                
            result[c.__name__] = elements

        return render(request,
                      'latexCheck.html',
                      {'result': result})
    

class CopyView(View):
    """Make a copy of an object 
    for a given model name"""

    def get(self, request, model, pk):
        # print "in copy view"
        # print model, pk


        # get the class:
        try:
            user_type = ContentType.objects.get(
                app_label="modulhandbuch",
                model=model)
        except:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Klasse nicht bekannt")
            print "class not found"
            r = redirect('modulhandbuchansehen')
            return r

        # get the object:
        try:
            o = user_type.get_object_for_this_type(
                pk=int(pk))
        except:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Objekt nicht bekannt")
            print "object not found"
            return redirect(model+'List')

        # make the copy:
        o.pk = None
        o.id = None
        # set the owner to the copier:
        o.owner = request.user
        
        try: 
            o.nameDe += " COPY"
            o.nameEn += " COPY"
        except AttributeError:
            o.name += " COPY"

        try:
            # print "now saving"
            o.save()
            # print "saved"
            messages.add_message(request,
                                 messages.INFO,
                                 'Kopie angelegt, bitte editieren.')
        except:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Anlegen der Kopie gescheitert")
            return redirect(model+'List')
            

        return redirect("/admin/modulhandbuch/{}/{}"
                        .format(model, o.pk))
