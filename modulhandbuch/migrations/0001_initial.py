# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lehrender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'Nicht immer sinnvoll, darf leer bleiben.', verbose_name=b'Weblink (URL)', blank=True)),
                ('name', models.CharField(help_text=b'Vor- und Nachname', max_length=200)),
                ('titel', models.CharField(help_text=b'Akademischer Titel', max_length=100, blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Eigent\xfcmer; darf editiern und l\xf6schen', null=True, verbose_name='Eigent\xfcmer')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Lehrende(r)',
                'verbose_name_plural': 'Lehrende',
            },
        ),
        migrations.CreateModel(
            name='NamedEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text=b'Nicht immer sinnvoll, darf leer bleiben.', verbose_name=b'Weblink (URL)', blank=True)),
                ('nameDe', models.CharField(help_text=b'Name in Langform', max_length=200, verbose_name=b'Name', blank=True)),
                ('nameEn', models.CharField(help_text=b'Name, long version', max_length=200, verbose_name=b'Name (engl.)', blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'nameDe', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TexDateien',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('tex', models.TextField()),
            ],
            options={
                'ordering': ['filename'],
                'verbose_name': 'Tex-Datei/allgemeines Template',
                'verbose_name_plural': 'Tex-Dateien/allgemeine Templates',
            },
        ),
        migrations.CreateModel(
            name='Fachgebiet',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('kuerzel', models.CharField(help_text='K\xfcrzel des Fachgebiets', max_length=10, verbose_name='K\xfcrzel', blank=True)),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Fachgebiet',
                'verbose_name_plural': 'Fachgebiete',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='FocusArea',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Studienrichtung  (Focus Area)',
                'verbose_name_plural': 'Studienrichtungen  (Focus Areas)',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='Lehreinheit',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Lehreinheit (typisch: Institut)',
                'verbose_name_plural': 'Lehreinheiten (typisch: Institute)',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='Lehrveranstaltung',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
                ('swsVl', models.IntegerField(default=0, help_text='Anzahl SWS f\xfcr Vorlesungsanteil', verbose_name=b'SWS Vorlesung')),
                ('swsUe', models.IntegerField(default=0, help_text='Anzahl SWS f\xfcr \xdcbungen', verbose_name='SWS \xdcbung')),
                ('swsSonst', models.IntegerField(default=0, help_text='Anzahl SWS f\xfcr andere Bestandteile', verbose_name=b'Sonstige SWS')),
                ('swsSonstBeschreibungDe', models.CharField(help_text=b'Beschreibung anderer Bestandteile', max_length=300, verbose_name=b'Beschreibung', blank=True)),
                ('swsSonstBeschreibungEn', models.CharField(help_text=b'Description of other parts of the lecture', max_length=300, verbose_name=b'Beschreibung (engl.)', blank=True)),
                ('selbststudium', models.IntegerField(default=0, help_text='Arbeitsaufwand f\xfcr Selbststudium\n                                        (in Stunden); f\xfcr Berechnung des\n                                        gesamten Arbeitsaufwandes.\n                                        ', verbose_name=b'Selbststudium')),
                ('sprache', models.CharField(default=b'EN', help_text='Sprache der Durchf\xfchrung', max_length=2, verbose_name=b'Sprache', choices=[(b'DE', b'Deutsch'), (b'EN', b'English')])),
                ('termin', models.CharField(default=b'NA', help_text='Typischer Durchf\xfchrungstermin', max_length=2, choices=[(b'WS', b'Wintersemester'), (b'SS', b'Sommersemester'), (b'NA', b'Nicht bekannt')])),
                ('zielsemester', models.IntegerField(default=0, help_text=b'Sollsemester, 0: beliebig')),
                ('inhaltDe', models.TextField(help_text=b'Stichpunkte zu Inhalten, wesentliche Kapitel', blank=True)),
                ('inhaltEn', models.TextField(blank=True)),
                ('lernergebnisDe', models.TextField(help_text=b'Kompetenzorientierte Beschreibung', blank=True)),
                ('lernergebnisEn', models.TextField(help_text=b'Kompetenzorientierte Beschreibung (engl.)', blank=True)),
                ('methodikDe', models.TextField(help_text=b'Beschreibung der Lehrmethoden', blank=True)),
                ('methodikEn', models.TextField(help_text=b'Beschreibung der Lehrmethoden (engl.)', blank=True)),
                ('vorkenntnisseDe', models.TextField(help_text=b'Sinnvolle Vorkenntnisse', blank=True)),
                ('vorkenntnisseEn', models.TextField(help_text=b'Sinnvolle Vorkenntnisse (engl.)', blank=True)),
                ('materialDe', models.TextField(help_text=b'Materialien f\xc3\xbcr die Vorlesung', blank=True)),
                ('materialEn', models.TextField(help_text=b'Materialien f\xc3\xbcr die Vorlesung (englische Beschreibung)', blank=True)),
                ('verantwortlicher', models.ForeignKey(verbose_name=b'Verantwortlicher Lehrerende(r)', to='modulhandbuch.Lehrender', help_text='Wer ist f\xfcr die Durchf\xfchrung/Organisation verantwortlich (muss nicht notwendig selbst durchf\xfchren)?')),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Lehrveranstaltung',
                'verbose_name_plural': 'Lehrveranstaltungen',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='Modul',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
                ('lps', models.IntegerField(default=0, help_text='Anzahl Leistungspunkte.')),
                ('lernzieleDe', models.TextField(help_text=b'Kurzbeschreibung der erworbenen Fertigkeiten, kompetenzorientiert.', blank=True)),
                ('lernzieleEn', models.TextField(help_text=b'Kurzbeschreibung der erworbenen Fertigkeiten, kompetenzorientiert (engl.).', blank=True)),
                ('bemerkungDe', models.TextField(help_text=b'Sonstige Bemerkungen', blank=True)),
                ('bemerkungEn', models.TextField(help_text=b'Sonstige Bemerkungen (engl.)', blank=True)),
                ('pflicht', models.BooleanField(default=False, help_text=b'Ist das eine Pflichtmodul?')),
                ('anzahlLvs', models.IntegerField(default=0, help_text='Wie viele Lehrveranstaltungen m\xfcssen in diesem Modul belegt werden in diesem Modul? Zur Berechung des Arbeitsaufwandes notwendig.')),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Modul',
                'verbose_name_plural': 'Module',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='Organisationsform',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Organisationsform des Moduls',
                'verbose_name_plural': 'Organisationsformen der Module',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='Pruefungsform',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Pr\xfcfungsform',
                'verbose_name_plural': 'Pr\xfcfungsformen',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='Studiengang',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
                ('focusareas', models.ManyToManyField(to='modulhandbuch.FocusArea')),
                ('module', models.ManyToManyField(to='modulhandbuch.Modul')),
                ('startdateien', models.ManyToManyField(help_text=b'Welche Tex-Dateien werden f\xc3\xbcr dieesen Studiengang ben\xc3\xb6tigt?', to='modulhandbuch.TexDateien', verbose_name=b'Benutzte Dateien')),
                ('verantwortlicher', models.ForeignKey(verbose_name=b'Verantwortlicher Lehrerende(r)', to='modulhandbuch.Lehrender', help_text='Wer ist f\xfcr die Durchf\xfchrung/Organisation verantwortlich (muss nicht notwendig selbst durchf\xfchren)?')),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Studiengang',
                'verbose_name_plural': 'Studieng\xe4nge',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.CreateModel(
            name='VeranstaltungsLps',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
                ('lp', models.IntegerField(default=0, help_text='Anzahl LPs f\xfcr diese Lehrveranstaltung in diesem Modul')),
                ('modul', models.ForeignKey(to='modulhandbuch.Modul')),
                ('veranstaltung', models.ForeignKey(to='modulhandbuch.Lehrveranstaltung')),
            ],
            options={
                'verbose_name': 'LP pro Veranstaltung',
                'verbose_name_plural': 'LPs pro Veranstaltungen',
            },
            bases=('modulhandbuch.namedentity',),
        ),
        migrations.AddField(
            model_name='namedentity',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Eigent\xfcmer; darf editiern und l\xf6schen', null=True, verbose_name='Eigent\xfcmer'),
        ),
        migrations.AddField(
            model_name='modul',
            name='organisation',
            field=models.ForeignKey(help_text='Art der Durchf\xfchrung des Moduls', to='modulhandbuch.Organisationsform'),
        ),
        migrations.AddField(
            model_name='modul',
            name='pruefung',
            field=models.ForeignKey(blank=True, to='modulhandbuch.Pruefungsform', help_text='Pr\xfcfungsform; ggf. neu anlegen.', null=True, verbose_name='Pr\xfcfungsform'),
        ),
        migrations.AddField(
            model_name='modul',
            name='verantwortlicher',
            field=models.ForeignKey(verbose_name=b'Verantwortlicher Lehrerende(r)', to='modulhandbuch.Lehrender', help_text='Wer ist f\xfcr die Durchf\xfchrung/Organisation verantwortlich (muss nicht notwendig selbst durchf\xfchren)?'),
        ),
        migrations.AddField(
            model_name='lehrender',
            name='fachgebiet',
            field=models.ForeignKey(help_text='Welchem Fachgebiet geh\xf6rt Lehrende(r) an?', to='modulhandbuch.Fachgebiet'),
        ),
        migrations.AddField(
            model_name='lehrender',
            name='lehreinheit',
            field=models.ForeignKey(help_text='Welcher Lehreinheit (typisch: Institut) geh\xf6rt Lehrende(r) an?', to='modulhandbuch.Lehreinheit'),
        ),
        migrations.AddField(
            model_name='focusarea',
            name='module',
            field=models.ManyToManyField(to='modulhandbuch.Modul'),
        ),
        migrations.AddField(
            model_name='focusarea',
            name='verantwortlicher',
            field=models.ForeignKey(verbose_name=b'Verantwortlicher Lehrerende(r)', to='modulhandbuch.Lehrender', help_text='Wer ist f\xfcr die Durchf\xfchrung/Organisation verantwortlich (muss nicht notwendig selbst durchf\xfchren)?'),
        ),
    ]
