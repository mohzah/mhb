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

    editors = models.ManyToManyField(User,
                                     related_name="%(app_label)s_%(class)s_editors",
                                     verbose_name=u"Editierrechte",
                                     help_text=u"Wer darf (ausser dem Eigentümer) diesen Eintrag editieren?",
                                     blank=True,
    )

    admin_fields = []

    def can_edit(self, user):
        """Every super user can edit,
        and the owner"""

        # print "can_edit: ", self, self.editors.all(), user
        # print("" + self.__class__.__name__)

        return (user.is_superuser or
                user == self.owner or
                user in self.editors.all()
                )

    class Meta:
        abstract = True


class URLEntity (OwnedEntity):
    kontaktdaten = models.CharField(max_length=200,
                                    blank=True,
                                    verbose_name="Kontaktdaten",
                                    help_text="Nicht immer sinnvoll, darf leer bleiben.")

    class Meta:
        abstract = True


class NamedEntity (URLEntity):
    nameDe = models.CharField(max_length=200,
                              # blank=True,
                              verbose_name="Name",
                              help_text="Name in Langform")

    nameEn = models.CharField(max_length=200,
                              # blank=True,
                              verbose_name="Name (engl.)",
                              help_text="Name, long version")

    # interneBemerkung = models.TextField(blank=True,
    #                                     verbose_name=u"Interne Bemerkungen",
    #                                     help_text=
    #                                     u"""Beliebige Bemerkung, taucht NICHT im
    #                                     Modulhandbuch auf. Sinnvoll kann Notiz
    #                                     zu intendierten Studiengängen sein.""",
    # )

    slug = AutoSlugField(populate_from='nameDe',
                         always_update=True,
                         unique=False)

    def pageref(self, english=False):
        if english:
            return ("(p.~\\pageref{" + self.__class__.__name__ +
                    ":" + self.slug + "})")
        else:
            return ("(S.~\\pageref{" + self.__class__.__name__ +
                    ":" + self.slug + "})")


    def __unicode__(self):
        r = self.nameDe + " / " + self.nameEn
        # if self.interneBemerkung:
        #     r += " ( " + self.interneBemerkung + " )"
        return r

    # end of class


class DescribedEntity(NamedEntity):
    # beschreibungDe = models.TextField(blank=True,
    #                                   verbose_name="Beschreibung",
    #                                   help_text=
    #                                   u"Ausführliche Beschreibung")
    # beschreibungEn = models.TextField(blank=True,
    #                                   verbose_name="Beschreibung (engl.)",
    #                                   help_text=
    #                                   "Extensive description")

    class Meta:
        abstract = True


class ResponsibleEntity(DescribedEntity):
    verantwortlicher = models.ForeignKey('Lehrender',
                                         verbose_name="Verantwortlicher Lehrender",
                                         help_text=u"Wer ist für die Durchführung/Organisation verantwortlich (muss nicht notwendig selbst durchführen)?")

    # note: class name here as a string, to avoid conflicts
    # with forward references not possible

    class Meta:
        abstract = True


class ExaminedEntity(ResponsibleEntity):
    pruefung = models.ForeignKey('Pruefungsform',
                                 blank=True,
                                 null=True,
                                 verbose_name=u"Prüfungsform",
                                 help_text=u"Prüfungsform; ggf. neu anlegen.")

    class Meta:
        abstract = True


class SWSEntity(ResponsibleEntity):
    swsVl = models.IntegerField(default=0,
                                verbose_name="SWS Vorlesung",
                                help_text=u"Anzahl SWS für Vorlesungsanteil")
    swsUe = models.IntegerField(default=0,
                                verbose_name=u"SWS Übung",
                                help_text=u"Anzahl SWS für Übungen")
    swsPraktikum = models.IntegerField(default=0,
                                   verbose_name="SWS Praktikum",
                                   help_text=u"Anzahl SWS für Praktikum")
    ects = models.IntegerField(default=0,
                               verbose_name="ECTS")
    # swsSonstBeschreibungDe = models.CharField(max_length=300, blank=True,
    #                                           verbose_name="Beschreibung",
    #                                           help_text="Beschreibung anderer Bestandteile")
    # swsSonstBeschreibungEn = models.CharField(max_length=300, blank=True,
    #                                           verbose_name="Beschreibung (engl.)",
    #                                           help_text="Description of other parts of the lecture")
    selbststudium = models.IntegerField(default=0,
                                        verbose_name="Selbststudium",
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
            15*(self.swsVl + self.swsUe + self.swsPraktikum) +
            self.selbststudium))

    sprache = models.CharField(max_length=5,
                               choices=(('DE', 'Deutsch'),
                                        ('EN', 'English'),
                                        ('Beide', 'Deutsch/English')),
                               default = 'DE',
                               verbose_name="Sprache",
                               help_text=u"Sprache der Durchführung")

    class Meta:
        abstract = True

##############
# concrete classes


# disaply_fields is an attribute picked up by the simple display views

# deleted, not needed
# class Lehreinheit(NamedEntity):
#     display_fields = ['nameDe', 'nameEn', 'kontaktdaten', 'editors']
#
#     class Meta:
#         verbose_name_plural = "Lehreinheiten (typisch: Institute)"
#         verbose_name = "Lehreinheit (typisch: Institut)"
#         ordering = ["nameDe", ]

class Lehrstuhl(NamedEntity):

    kuerzel = models.CharField(max_length=10,
                               blank=True,
                               verbose_name=u"Kürzel",
                               help_text=u"Kürzel des Lehrstühle")
    display_fields = ['nameDe', 'nameEn', 'kuerzel', 'kontaktdaten', 'editors']

    class Meta:
        verbose_name_plural = "Lehrstühle"
        verbose_name = "Lehrstuhl"
        ordering = ["nameDe", ]


class Pruefungsform(DescribedEntity):
    display_fields = ['nameDe', 'nameEn', 'beschreibungDe', 'beschreibungEn', 'editors']

    class Meta:
        verbose_name = u"Prüfungsform"
        verbose_name_plural = u"Prüfungsformen"
        ordering = ["nameDe", ]


class Organisationsform(DescribedEntity):
    display_fields = ['nameDe', 'nameEn', 'beschreibungDe', 'beschreibungEn', 'editors']
    class Meta:
        verbose_name_plural = "Organisationsformen der Module"
        verbose_name = "Organisationsform des Moduls"
        ordering = ["nameDe", ]


class NichtfachlicheKompetenz(DescribedEntity):
    display_fields = ['nameDe', 'nameEn',
                      'beschreibungDe', 'beschreibungEn',
                      'editors']

    class Meta:
        verbose_name_plural = "Nichtfachliche Kompetenzen"
        verbose_name = "Nichtfachliche Kompetenz"
        ordering = ["nameDe", ]


class Lehrender(URLEntity):
    display_fields = ['name', 'titel', 'kontaktdaten', 'lehrstuhl', 'editors']

    name = models.CharField(max_length=200,
                            help_text="Vor- und Nachname")
    titel = models.CharField(max_length=100,
                             blank=True,
                             help_text="Akademischer Titel")
    lehrstuhl = models.ForeignKey('Lehrstuhl',
                                   help_text=u"Welchem Lehrstuhl gehört Lehrende(r) an?")
    # lehreinheit = models.ForeignKey('Lehreinheit',
    #                                 help_text=u"Welcher Lehreinheit (typisch: Institut) gehört Lehrende(r) an?")

    class Meta:
        verbose_name_plural = "Lehrende"
        verbose_name = "Lehrende(r)"
        ordering = ["name", ]

    def __unicode__(self):
        return self.titel + ' ' + self.name


class Lehrveranstaltung(SWSEntity):
    display_fields = ['nameDe', 'nameEn',
                      'lv_nr',
                      'kontaktzeit',
                      'verantwortlicher',
                      # 'beschreibungDe', 'beschreibungEn',
                      'swsVl', 'swsUe', 'swsPraktikum',
                      'ects',
                      # 'swsSonstBeschreibungDe', 'swsSonstBeschreibungEn',
                      'termin',
                      'zielsemester',
                      'englishsprachige',
                      'inhaltDe', #'inhaltEn',
                      'lernergebnisDe', #'lernergebnisEn',
                      'voraussetzungen',
                      'sonstige_hinweise',
                      'vorkenntnisseDe', #'vorkenntnisseEn',
                      'literatur', #'materialEn',
                      'weiterfuehrende',
                      'lehrform',
                      'gruppengrosse',
                      # 'status',
                      # 'nfk',
                      # 'editors'
                  ]

    # admin_fields = ["nfk"]

    lv_nr = models.CharField(max_length=50,
                             # blank=True,
                             verbose_name="LV-NR",
                             )
    kontaktzeit = models.CharField(max_length=70,
                                         # blank=True,
                                         verbose_name='Kontaktzeit')
    termin = models.CharField(max_length=2,
                              verbose_name="Termin",
                              choices=(('WS', 'Wintersemester'),
                                       ('SS', 'Sommersemester'),
                                       ('NA', 'Nicht bekannt'), ),
                              default = 'NA',
                              help_text=u"Typischer Durchführungstermin")
    zielsemester = models.IntegerField(default=0,
                                       help_text="Sollsemester, 0: beliebig")

    englishsprachige = models.BooleanField(default=False,
                                           verbose_name="Aufnahme in die Liste englischsprachiger Veranstaltungen")
    # kurzbeschreibungDe = models.TextField(blank=True)
    # kurzbeschreibungEn = models.TextField(blank=True)
    inhaltDe = models.TextField(#blank=True,
                                verbose_name="Inhalt",
                                help_text="Stichpunkte zu Inhalten, wesentliche Kapitel")
    # inhaltEn = models.TextField(blank=True,
    #                             verbose_name="Inhalt (engl.)",
    # )
    lernergebnisDe = models.TextField(blank=True,
                                      verbose_name="Lernergebnis und Kompetenzen",
                                      help_text=
                                      "Kompetenzorientierte Beschreibung")
    # lernergebnisEn = models.TextField(blank=True,
    #                                   verbose_name="Lernergebnis (engl.)",
    #                                   help_text=
    #                                   "Kompetenzorientierte Beschreibung (engl.)")
    voraussetzungen = models.TextField(blank=True,
                                       verbose_name="Voraussetzungen für die Teilnahme an der Prüfung",
                                       help_text=u"Voraussetzungen für die Teilnahme an der Prüfung bzw. die Vergabe von ECTS")
    sonstige_hinweise = models.TextField(blank=True,
                                         verbose_name="Sonstige Hinweise")
    vorkenntnisseDe = models.TextField(blank=True,
                                       verbose_name="Empfohlene Vorkenntnisse",
                                       help_text="Sinnvolle Vorkenntnisse")
    # vorkenntnisseEn = models.TextField(blank=True,
    #                                    verbose_name="Vorkenntnisse (engl.)",
    #                                    help_text="Sinnvolle Vorkenntnisse (engl.)")
    # kombinationDe = models.TextField(blank=True)
    # kombinationEn = models.TextField(blank=True)
    literatur = models.TextField(blank=True,
                                  verbose_name="Literatur",
                                  help_text=u"Literatur für die Vorlesung")
    # materialEn = models.TextField(blank=True,
    #                               verbose_name="Material (engl.)",
    #                               help_text=u"Materialien für die Vorlesung (englische Beschreibung)")
    # ToDo: check if removing interneBemerkung doesn't cause any problem
    # remove it from parent class
    # don't want to inherit this field
    # django doesn't allow overriding Fields
    # https://docs.djangoproject.com/en/1.10/topics/db/models/
    # interneBemerkung = None

    # nfk = models.ManyToManyField(
    #     NichtfachlicheKompetenz,
    #     verbose_name="Nichtfachliche Kompetenz",
    #     help_text="Welche nichtfachlichen Kompetenzen werden durch diese Lehrveranstaltung erworben?",
    #     blank=True,
    # )
    #
    # def nfk_list(self):
    #     return self.nfk.all()

    # weiterfuehrende = models.ManyToManyField('self',
    #                                          verbose_name=u"Weiterführende Veranstaltungen",
    #                                          help_text="Courses that can be taken afterward"
    #                                          )
    weiterfuehrende = models.TextField(blank=True,
                                       verbose_name="Weiterführende Veranstaltungen",
                                       help_text="Courses that can be taken afterward")

    lehrform = models.CharField(max_length=200,
                                verbose_name="Lehrform")

    gruppengrosse = models.CharField(blank=False,
                                     max_length= 50,
                                     verbose_name="Gruppengröße (TN)")

    # status = models.CharField(blank=True,
    #                           max_length=10,
    #                           choices=(('P', 'P'),
    #                                    ('PW', 'WP')),
    #                           help_text='Status (P/WP)')

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

    def copyLV(self, orgObj):
        """copy the VeranstaltungsLps over from the
        Lehrveranstaltung orgObj"""

        # print "trying to copy VeranstaltungsLps"

        vlps = orgObj.veranstaltungslps_set.all()
        # print "vlps: ", vlps

        for x in vlps:
            # print x
            tmp = VeranstaltungsLps(
                veranstaltung=self,
                modul=x.modul,
                lp=x.lp,
                prufungsleistung = x.prufungsleistung,
                # studienleistung = x.studienleistung
            )
            tmp.save()

    class Meta:
        verbose_name_plural = "Lehrveranstaltungen"
        verbose_name = "Lehrveranstaltung"
        ordering = ['nameDe', ]


# class Modul(SWSEntity):
class Modul(DescribedEntity):

    display_fields = ['nameDe',
                      'nummer', 'workload', 'credits',
                      'studiensemester', 'haufigkeit',
                      'dauer', 'lernzieleDe'
                      'inhalte', # 'lehrformen',
                      'gruppengrosse', 'verwendung',
                      # 'empfohlene',
                      # 'prufungs_explanation',
                      'voraussetzungen',
                      'voraussetzungen_vergabe',
                      'modulbeauftragter',
                      # 'beschreibungDe', 'beschreibungEn',
                      # 'lps',
                      # 'pflicht', 'anzahlLvs',
                      # 'organisation',
                      # 'lernzieleDe', 'lernzieleEn',
                      # 'bemerkungDe', 'bemerkungEn',
                      'editors',
                      'wahlmoeglichkeiten',
                      'teilnahmevoraussetzungen',
                      'pruefungsleistung',
                      'gewichtung',
                      'sonstige',
                      'above_table',
                      'module_type',
                  ]

    nummer = models.CharField(max_length=100,
                              verbose_name="Nummer")
    workload = models.IntegerField(default=0,
                              verbose_name="Workload")
    credits = models.IntegerField(default=0,
                              verbose_name="Credits")
    studiensemester = models.CharField(max_length=100,
                              verbose_name="Studiensemester")
    Turnus = models.CharField(max_length=100,
                              verbose_name="Turnus")
    dauer = models.CharField(max_length=100,
                              verbose_name=u"Dauer (in Sem.)")

    # lps = models.IntegerField(default=0,
    #                           verbose_name="Leistungspunkte",
    #                           help_text=
    #                           u"Anzahl Leistungspunkte.")


    lernzieleDe = models.TextField(verbose_name="Lernergebnisse (learning outcomes) / Kompetenzen")

    # lernzieleEn = models.TextField(blank=True,
    #                                verbose_name="Lernziele (engl.)",
    #                                help_text=
    #                                "Kurzbeschreibung der erworbenen Fertigkeiten, kompetenzorientiert (engl.).")

    inhalte = models.TextField(verbose_name="Inhalte")

    # lehrformen = models.CharField(max_length=200,
    #                               verbose_name="Lehrformen")

    # gruppengrosse = models.TextField(verbose_name="Gruppengröße")

    verwendung = models.CharField(max_length=200,
                                  verbose_name=u"Verwendung des Moduls in anderen Studiengängen")

    # empfohlene = models.TextField(blank=True,
    #                               verbose_name="Empfohlene Vorkenntniss")

    # prufungs_explanation = models.TextField(verbose_name=u"Prüfungsformen")

    voraussetzungen = models.TextField(blank=False,
                                       verbose_name=u"Voraussetzungen für die Teilnahme an Prüfungen")

    voraussetzungen_vergabe = models.TextField(blank=False,
                                       verbose_name=u"Voraussetzungen für die Vergabe von Credits")

    wahlmoeglichkeiten = models.TextField(blank=False,
                                          verbose_name=u'Wahlmöglichkeiten innerhalb des Moduls')

    teilnahmevoraussetzungen = models.TextField(verbose_name='Teilnahmevoraussetzungen')

    pruefungsleistung = models.CharField(blank=True,
                                         max_length=35,
                                         verbose_name=u'Prüfungsleistung',
                                         choices=((u'Modulabschlussprüfung (MAP)', u'Modulabschlussprüfung '),
                                                  ('Modulprufung (MP)', 'Modulprufung'),
                                                  ('Modulteilprufungen (MTP)', 'Modulteilprufungen')))

    gewichtung = models.TextField(blank=True,
                                  verbose_name=u'Gewichtung für Gesamtnote')

    sonstige = models.TextField(blank=False,
                                verbose_name='Sonstige Hinweise')

    above_table = models.TextField(blank=True,
                                   help_text="Text comming above module table in PDF")

    modulbeauftragter = models.ForeignKey('Lehrender',
                                         verbose_name="Modulbeauftragter")

    module_type = models.ForeignKey('Moduletype')
    # organisation = models.ForeignKey(Organisationsform,
    #                                  verbose_name="Organisationsform des Moduls",
    #                                  help_text=u"Art der Durchführung des Moduls")

    # pflicht = models.BooleanField(default=False,
    #                               help_text=
    #                               "Ist das eine Pflichtmodul?")

    # anzahlLvs = models.IntegerField(default=0,
    #                                 verbose_name="Anzahl Lehrveranstaltungen",
    #                                 help_text=u"Wie viele Lehrveranstaltungen müssen in diesem Modul belegt werden in diesem Modul? Zur Berechung des Arbeitsaufwandes notwendig.")

    # TODO: If it stays a responsible entity, then we need methods
    # to ask for the SWS both here and in SWSEntity, for uniform access
    # (or Python property)

    def nfk_list(self):
        """get the nfks of all encompassed lehrveranstaltungen"""
        nfkIds = VeranstaltungsLps.objects.filter(modul=self).values_list('veranstaltung__nfk').distinct()
        nfks = NichtfachlicheKompetenz.objects.filter(id__in=nfkIds)

        return nfks

    def getSWSText(self):
        """Produce a summary of the SWS texts of the contained Lehrveranstaltungen.
        Return it is a dictionary: hours of VL, UE, other, and list of other descriptions,
        and warnings.
        Do sanity-checking.
        """

        res = {'swsVl': 0,
               'swsUe': 0,
               'swsPraktikum': 0,
               # 'swsSonstBeschreibungDe': [],
               # 'swsSonstBeschreibungEn': [],
               'warnings': [],
        }

        actualAnzahlLVs = self.veranstaltungslps_set.count()

        if actualAnzahlLVs < self.anzahlLvs:
            res['warnings'].append(u"Warnung: nicht genügend Lehrveranstatungen im Modul")
        elif actualAnzahlLVs == self.anzahlLvs:
            # easy case: just collect all together
            for lvlps in self.veranstaltungslps_set.all():
                lv = lvlps.veranstaltung
                res['swsVl'] += lv.swsVl
                res['swsUe'] += lv.swsUe
                res['swsPraktikum'] += lv.swsPraktikum
                # if lv.swsSonstBeschreibungDe:
                #     res['swsSonstBeschreibungDe'].append(
                #         lv.swsSonstBeschreibungDe)
                # if lv.swsSonstBeschreibungEn:
                #     res['swsSonstBeschreibungEn'].append(
                #         lv.swsSonstBeschreibungEn)
        else:
            # complicated case, need to check whether
            # descipriotns are consistent
            # can only generate a plausible description if
            # - all LVs have the same VL, UE, sonst a
            # - and all descriptions are consistent
            # otherwise: just return a warning

            for attr in ['swsVl', 'swsUe', 'swsPraktikum',
                         # 'swsSonstBeschreibungDe', 'swsSonstBeschreibungEn'
                         ]:
                tmp = set([getattr(lvlps.veranstaltung, attr)
                           for lvlps in self.veranstaltungslps_set.all()])
                if len(tmp) != self.anzahlLvs:
                    try:
                        res['warnings'].append("Warnung: Inkonsistenz bei " +
                                               attr + ": " +
                                               ', '.join([str(x) for x in tmp]))
                    except Exception as e:
                        res['warnings'].append("Warnung: Inkonsistenz bei " +
                                               attr +
                                               "; Exception  " + e.strerror)
                else:
                    # if "Beschreibung" in attr:
                    #     res[attr] = [getattr(lvlps.veranstaltung, attr)]
                    # else:
                    res[attr] = getattr(lvlps.veranstaltung, attr)

        return res

    def copyLV(self, orgObj):
        """copy the VeranstaltungsLps over from the
        Module orgObj"""

        # print "trying to copy VeranstaltungsLps"

        vlps = orgObj.veranstaltungslps_set.all()
        # print "vlps: ", vlps

        for x in vlps:
            # print x
            tmp = VeranstaltungsLps(
                veranstaltung=x.veranstaltung,
                modul=self,
                lp=x.lp,
            )
            tmp.save()


    class Meta:
        verbose_name_plural = "Module"
        verbose_name = "Modul"
        ordering = ['nameDe', ]


class Prufungsleistung(OwnedEntity):
    prufungsform = models.CharField(#blank=True,
                                    max_length=60,
                                    verbose_name=u'Prüfungsform')
    dauer = models.CharField(#blank=True,
                             max_length=60,
                             verbose_name="Dauer bzw Umfang")
    gewichtung = models.IntegerField(default=50,
                                     verbose_name=u"Gewichtung für die Modulnote")

    def __unicode__(self):
        return '{:.10} - {:.10} - {}%'.format(self.prufungsform, self.dauer, self.gewichtung)


# class Studienleistung(OwnedEntity):
#     form = models.CharField(blank=True,
#                             max_length=40,
#                             verbose_name='Form')
#     dauer = models.CharField(blank=True,
#                              max_length=25,
#                              verbose_name='Dauer bzw Umfang')
#     sl_qt = models.CharField(max_length=10,
#                              verbose_name='SL / QT',
#                              choices=(('SL', 'SL'),
#                                       ('QT', 'QT'))
#                              )
#
#     def __unicode__(self):
#         return '{:.50} / {:.50} / {}'.format(self.form, self.dauer, self.sl_qt)


class VeranstaltungsLps(DescribedEntity):

    lp = models.IntegerField(verbose_name="Leistungspunkte",
                             help_text=
                             u"Anzahl LPs für diese Lehrveranstaltung in diesem Modul")
    veranstaltung = models.ForeignKey(Lehrveranstaltung)
    modul = models.ForeignKey(Modul)
    prufungsleistung = models.ForeignKey(Prufungsleistung,
                                         verbose_name=u"Prüfungsleistung")
    sl_qt = models.CharField(max_length=10,
                             verbose_name='SL / QT',
                             choices=(('SL', 'SL'),
                                      ('QT', 'QT'))
                             )
    form = models.CharField(blank=True,
                            max_length=40,
                            verbose_name='Form')
    dauer_umfang = models.CharField(blank=True,
                             max_length=25,
                             verbose_name='Dauer bzw Umfang')
    # studienleistung = models.ForeignKey(Studienleistung, verbose_name="Form / Dauer u. Umfang / Studienleistung")
    status = models.CharField(max_length=5,
                              choices=(('P', 'P'),
                                       ('PW', 'WP')),
                              help_text='Status (P/WP)')


    class Meta:
        verbose_name = "LP pro Veranstaltung"
        verbose_name_plural = "LPs pro Veranstaltungen"

    def __unicode__(self):
        return (self.modul.__unicode__() +
                " : " +
                self.veranstaltung.__unicode__())


# class FocusArea(ResponsibleEntity):
#
#     display_fields = [
#         'nameDe', 'nameEn',
#         'kontaktdaten',
#         'verantwortlicher',
#         'module',
#         'beschreibungDe', 'beschreibungEn', 'editors']
#
#     admin_fields = ['module', ]
#
#     module = models.ManyToManyField(Modul)
#
#     class Meta:
#         verbose_name = "Studienrichtung  (Focus Area)"
#         verbose_name_plural = "Studienrichtungen  (Focus Areas)"
#         ordering = ["nameDe", ]


class Studiengang(DescribedEntity):

    display_fields = [
        'nameDe', 'nameEn',
        'kontaktdaten',
        # 'verantwortlicher', not inherited from ResponsibleEntity anymore
        'module',
        # 'focusareas',
        'startdateien',
        'beschreibungDe', 'beschreibungEn', 'editors']

    admin_fields = ['startdateien', ]

    module = models.ManyToManyField(Modul)
    # focusareas = models.ManyToManyField(FocusArea)
    startdateien = models.ManyToManyField("TexDateien",
                                          verbose_name="Benutzte Dateien",
                                          help_text=u"Welche Tex-Dateien werden für dieesen Studiengang benötigt?")
    # TODO: de, en , both Versionen der Startdateien?

    class Meta:
        verbose_name = "Studiengang"
        verbose_name_plural = u"Studiengänge"
        ordering = ["nameDe", ]


class Moduletype(models.Model):
    type_of_module = models.CharField(max_length=100)
    # relevant_studiengang = models.ForeignKey('Studiengang')
    class Meta:
        verbose_name = "Module Type"
        verbose_name_plural = "Module Types"

    def __unicode__(self):
        return self.type_of_module

class TexDateien (models.Model):
    # add description, make filename unique!
    filename = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    tex = models.TextField()

    display_fields = ['filename',
                      'description',
                      'tex', ]

    class Meta:
        verbose_name = "Tex-Datei/allgemeines Template"
        verbose_name_plural = "Tex-Dateien/allgemeine Templates"
        ordering = ["filename", ]

    def is_start_file(self):
        """check whether the tex code contains
        documentclass command. We assume that this means
        it should be translated by pdflatex.
        """

        return "documentclass" in self.tex

    def __unicode__(self):
        return self.filename
