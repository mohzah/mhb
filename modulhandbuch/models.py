# -*- coding: utf-8 -*-


from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User

import re
import math

############
# abstract base classes


class OwnedEntity(models.Model):
    owner = models.ForeignKey(User,
                              verbose_name=u"Eigentümer",
                              help_text=u"Eigentümer; darf editiern und löschen",
                              blank=True,
                              null=True)

    def can_edit(self, user):
        """Every super user can edit,
        and the owner"""

        return (user.is_superuser or
                user == self.owner)

    class Meta:
        abstract = True


class URLEntity (OwnedEntity):
    url = models.URLField(blank=True,
                          verbose_name="Weblink (URL)",
                          help_text="Nicht immer sinnvoll, darf leer bleiben.")

    class Meta:
        abstract = True


class NamedEntity (URLEntity):
    nameDe = models.CharField(max_length=200,
                              blank=True,
                              verbose_name="Name",
                              help_text="Name in Langform")

    nameEn = models.CharField(max_length=200,
                              blank=True,
                              verbose_name="Name (engl.)",
                              help_text="Name, long version")

    slug = AutoSlugField(populate_from='nameDe')

    def pageref(self, english=False):
        if english:
            return ("(p.~\\pageref{" + self.__class__.__name__ +
                    ":" + self.slug + "})")
        else:
            return ("(S.~\\pageref{" + self.__class__.__name__ +
                    ":" + self.slug + "})")


    def __unicode__(self):
        return self.nameDe + " / " + self.nameEn

    # end of class


class DescribedEntity(NamedEntity):
    beschreibungDe = models.TextField(blank=True,
                                      verbose_name="Beschreibung",
                                      help_text=
                                      u"Ausführliche Beschreibung")
    beschreibungEn = models.TextField(blank=True,
                                      verbose_name="Beschreibung (engl.)",
                                      help_text=
                                      "Extensive description")

    class Meta:
        abstract = True


class ResponsibleEntity(DescribedEntity):
    verantwortlicher = models.ForeignKey('Lehrender',
                                         help_text="Verantwortlicher Lehrerende(r)")

    # note: class name here as a string, to avoid conflicts
    # with forward references not possible

    class Meta:
        abstract = True


class ExaminedEntity(ResponsibleEntity):
    pruefung = models.ForeignKey('Pruefungsform',
                                 blank=True,
                                 null=True,
                                 help_text=u"Prüfungsform; ggf. neu anlegen.")

    class Meta:
        abstract = True


class SWSEntity(ResponsibleEntity):
    swsVl = models.IntegerField(default=0,
                                help_text=u"Anzahl SWS für Vorlesungsanteil")
    swsUe = models.IntegerField(default=0,
                                help_text=u"Anzahl SWS für Übungen")
    swsSonst = models.IntegerField(default=0,
                                   help_text=u"Anzahl SWS für andere Bestandteile")
    swsSonstBeschreibungDe = models.CharField(max_length=300, blank=True,
                                              help_text="Beschreibung anderer Bestandteile")
    swsSonstBeschreibungEn = models.CharField(max_length=300, blank=True,
                                              help_text="Description of other parts of the lecture")
    selbststudium = models.IntegerField(default=0,
                                        help_text=
                                        u"""Arbeitsaufwand für Selbststudium
                                        (in Stunden); für Berechnung des
                                        gesamten Arbeitsaufwandes.
                                        """,
    )

    @property
    def arbeitsaufwand(self):
        """Compute arbeitsaufwand in hours, based on SWS
        and selbststudium.
        """
        return int(math.ceil(
            15*1.5*(self.swsVl + self.swsUe + self.swsSonst) +
            self.selbststudium))

    sprache = models.CharField(max_length=2,
                               choices=(('DE', 'Deutsch'),
                                        ('EN', 'English'), ),
                               default = 'EN',
                               help_text=u"Sprache der Durchführung")

    class Meta:
        abstract = True

##############
# concrete classes


# disaply_fields is an attribute picked up by the simple display views

class Lehreinheit(NamedEntity):
    display_fields = ['nameDe', 'nameEn', 'url']

    class Meta:
        verbose_name_plural = "Lehreinheiten (typisch: Institute)"
        verbose_name = "Lehreinheit (typisch: Institut)"


class Fachgebiet(NamedEntity):

    kuerzel = models.CharField(max_length=10,
                               blank=True,
                               help_text=u"Kürzel des Fachgebiets")
    display_fields = ['nameDe', 'nameEn', 'kuerzel', 'url']

    class Meta:
        verbose_name_plural = "Fachgebiete"
        verbose_name = "Fachgebiet"


class Pruefungsform(DescribedEntity):
    display_fields = ['nameDe', 'nameEn', 'beschreibungDe', 'beschreibungEn']

    class Meta:
        verbose_name = u"Prüfungsform"
        verbose_name_plural = u"Prüfungsformen"


class Organisationsform(DescribedEntity):
    display_fields = ['nameDe', 'nameEn', 'beschreibungDe', 'beschreibungEn']
    class Meta:
        verbose_name_plural = "Organisationsformen der Module"
        verbose_name = "Organisationsform des Moduls"


class Lehrender(URLEntity):
    display_fields = ['name', 'titel', 'url', 'fachgebiet', 'lehreinheit']

    name = models.CharField(max_length=200)
    titel = models.CharField(max_length=100,
                             blank=True)
    fachgebiet = models.ForeignKey('Fachgebiet')
    lehreinheit = models.ForeignKey('Lehreinheit')

    class Meta:
        verbose_name_plural = "Lehrende"
        verbose_name = "Lehrende(r)"

    def __unicode__(self):
        return self.titel + ' ' + self.name


class Lehrveranstaltung(SWSEntity):
    display_fields = ['nameDe', 'nameEn',
                      'verantwortlicher',
                      'beschreibungDe', 'beschreibungEn',
                      'swsVl', 'swsUe', 'swsSonst',
                      'swsSonstBeschreibungDe', 'swsSonstBeschreibungEn',
                      'termin',
                      'zielsemester',
                      'inhaltDe', 'inhaltEn',
                      'lernergebnisDe', 'lernergebnisDe',
                      'methodikDe', 'methodikEn',
                      'vorkenntnisseDe', 'vorkenntnisseEn',
                      'materialDe', 'materialEn',
                  ]

    termin = models.CharField(max_length=2,
                              choices=(('WS', 'Wintersemester'),
                                       ('SS', 'Sommersemester'),
                                       ('NA', 'Nicht bekannt'), ),
                              default = 'NA',
                              help_text=u"Typischer Durchführungstermin")
    zielsemester = models.IntegerField(default=0,
                                       help_text="Sollsemester, 0: beliebig")

    # kurzbeschreibungDe = models.TextField(blank=True)
    # kurzbeschreibungEn = models.TextField(blank=True)
    inhaltDe = models.TextField(blank=True,
                                help_text="Stichpunkte zu Inhalten, wesentliche Kapitel")
    inhaltEn = models.TextField(blank=True)
    lernergebnisDe = models.TextField(blank=True,
                                      help_text=
                                      "Kompetenzorientierte Beschreibung")
    lernergebnisEn = models.TextField(blank=True)
    methodikDe = models.TextField(blank=True,
                                  help_text="Beschreibung der Lehrmethoden")
    methodikEn = models.TextField(blank=True)
    vorkenntnisseDe = models.TextField(blank=True)
    vorkenntnisseEn = models.TextField(blank=True)
    # kombinationDe = models.TextField(blank=True)
    # kombinationEn = models.TextField(blank=True)
    materialDe = models.TextField(blank=True)
    materialEn = models.TextField(blank=True)

    def in_modul(self, modul):
        """A little helper function: check if this
        LV is in the modul given an parameter.
        If yes, return the LPs, if no, return None
        """

        # print "-------"
        # print self, modul
        try:
            vlps = VeranstaltungsLps.objects.filter(
                modul=modul).filter(
                    veranstaltung=self)
            # print "vlps: ", vlps

            if vlps:
                lp = vlps[0].lp
            else:
                lp = None
        except Exception as e:
            # print "error: ", e, self, modul
            lp = None

        # print "Lp: ", lp
        # print "====="

        return lp

    class Meta:
        verbose_name_plural = "Lehrveranstaltungen"
        verbose_name = "Lehrveranstaltung"
        ordering = ['nameDe']


# class Modul(SWSEntity):
class Modul(ExaminedEntity):

    display_fields = ['nameDe', 'nameEn',
                      'verantwortlicher',
                      'pruefung',
                      'beschreibungDe', 'beschreibungEn',
                      'lps', 'pflicht', 'anzahlLvs',
                      'organisation',
                      'lernzieleDe', 'lernzieleEn',
                      'bemerkungDe', 'bemerkungEn',
                  ]
    lps = models.IntegerField(default=0,
                              help_text=
                              u"Anzahl Leistungspunkte. Wird gegen Anzahl LVs und LPs pro LV geprüft.")

    organisation = models.ForeignKey(Organisationsform,
                                     help_text=u"Art der Durchführung des Moduls")

    lernzieleDe = models.TextField(blank=True,
                                   help_text=
                                   "Kurzbeschreibung der erworbenen Fertigkeiten, kompetenzorientiert.")
    lernzieleEn = models.TextField(blank=True)

    bemerkungDe = models.TextField(blank=True,
                                   help_text=
                                   "Sonstige Bemerkungen")
    bemerkungEn = models.TextField(blank=True)

    pflicht = models.BooleanField(default=False)

    anzahlLvs = models.IntegerField(default=0,
                                    help_text=u"Wie viele Lehrveranstaltungen müssen in diesem Modul belegt werden in diesem Modul? Zur Berechung des Arbeitsaufwandes notwendig.")

    # TODO: If it stays a responsible entity, then we need methods
    # to ask for the SWS both here and in SWSEntity, for uniform access
    # (or Python property)

    class Meta:
        verbose_name_plural = "Module"
        verbose_name = "Modul"
        ordering = ['nameDe']


class VeranstaltungsLps(DescribedEntity):

    lp = models.IntegerField(default=0,
                             help_text=
                             u"Anzahl LPs für diese Lehrveranstaltung in diesem Modul")
    veranstaltung = models.ForeignKey(Lehrveranstaltung)
    modul = models.ForeignKey(Modul)

    class Meta:
        verbose_name = "LP pro Veranstaltung"
        verbose_name_plural = "LPs pro Veranstaltungen"

    def __unicode__(self):
        return (self.modul.__unicode__() +
                " : " +
                self.veranstaltung.__unicode__())


class FocusArea(ResponsibleEntity):

    display_fields = [
        'nameDe', 'nameEn',
        'url',
        'verantwortlicher',
        'beschreibungDe', 'beschreibungEn']

    module = models.ManyToManyField(Modul)

    class Meta:
        verbose_name = "Studienrichtung  (Focus Area)"
        verbose_name_plural = "Studienrichtungen  (Focus Areas)"


class Studiengang(ResponsibleEntity):
    module = models.ManyToManyField(Modul)
    focusareas = models.ManyToManyField(FocusArea)
    startdateien = models.ManyToManyField("TexDateien",
                                          verbose_name="Benutzte Dateien",
                                          help_text="Welche Tex-Dateien werden für dieesen Studiengang benötigt?")
    # TODO: de, en , both Versionen der Startdateien?

    class Meta:
        verbose_name = "Studiengang"
        verbose_name_plural = u"Studiengänge"


class TexDateien (models.Model):
    # add description, make filename unique!
    filename = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    tex = models.TextField()

    class Meta:
        verbose_name = "Tex-Datei/allgemeines Template"
        verbose_name_plural = "Tex-Dateien/allgemeine Templates"

    def is_start_file(self):
        """check whether the tex code contains
        documentclass command. We assume that this means
        it should be translated by pdflatex.
        """

        return "documentclass" in self.tex

    def __unicode__(self):
        return self.filename
