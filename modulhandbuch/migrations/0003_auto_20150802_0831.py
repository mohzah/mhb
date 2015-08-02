# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0002_auto_20150713_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='inhaltDe',
            field=models.TextField(help_text=b'Stichpunkte zu Inhalten, wesentliche Kapitel', verbose_name=b'Inhalt', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='inhaltEn',
            field=models.TextField(verbose_name=b'Inhalt (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='lernergebnisDe',
            field=models.TextField(help_text=b'Kompetenzorientierte Beschreibung', verbose_name=b'Lernergebnis', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='lernergebnisEn',
            field=models.TextField(help_text=b'Kompetenzorientierte Beschreibung (engl.)', verbose_name=b'Lernergebnis (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='materialDe',
            field=models.TextField(help_text='Materialien f\xfcr die Vorlesung', verbose_name=b'Material', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='materialEn',
            field=models.TextField(help_text='Materialien f\xfcr die Vorlesung (englische Beschreibung)', verbose_name=b'Material (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='methodikDe',
            field=models.TextField(help_text=b'Beschreibung der Lehrmethoden', verbose_name=b'Methodik', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='methodikEn',
            field=models.TextField(help_text=b'Beschreibung der Lehrmethoden (engl.)', verbose_name=b'Methodik (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='termin',
            field=models.CharField(default=b'NA', help_text='Typischer Durchf\xfchrungstermin', max_length=2, verbose_name=b'Termin', choices=[(b'WS', b'Wintersemester'), (b'SS', b'Sommersemester'), (b'NA', b'Nicht bekannt')]),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='vorkenntnisseDe',
            field=models.TextField(help_text=b'Sinnvolle Vorkenntnisse', verbose_name=b'Vorkenntnisse', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='vorkenntnisseEn',
            field=models.TextField(help_text=b'Sinnvolle Vorkenntnisse (engl.)', verbose_name=b'Vorkenntnisse (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='modul',
            name='anzahlLvs',
            field=models.IntegerField(default=0, help_text='Wie viele Lehrveranstaltungen m\xfcssen in diesem Modul belegt werden in diesem Modul? Zur Berechung des Arbeitsaufwandes notwendig.', verbose_name=b'Anzahl Lehrveranstaltungen'),
        ),
        migrations.AlterField(
            model_name='modul',
            name='bemerkungDe',
            field=models.TextField(help_text=b'Sonstige Bemerkungen', verbose_name=b'Bemerkungen', blank=True),
        ),
        migrations.AlterField(
            model_name='modul',
            name='bemerkungEn',
            field=models.TextField(help_text=b'Sonstige Bemerkungen (engl.)', verbose_name=b'Bemerkungen (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='modul',
            name='lernzieleDe',
            field=models.TextField(help_text=b'Kurzbeschreibung der erworbenen Fertigkeiten, kompetenzorientiert.', verbose_name=b'Lernziele', blank=True),
        ),
        migrations.AlterField(
            model_name='modul',
            name='lernzieleEn',
            field=models.TextField(help_text=b'Kurzbeschreibung der erworbenen Fertigkeiten, kompetenzorientiert (engl.).', verbose_name=b'Lernziele (engl.)', blank=True),
        ),
        migrations.AlterField(
            model_name='modul',
            name='lps',
            field=models.IntegerField(default=0, help_text='Anzahl Leistungspunkte.', verbose_name=b'Leistungspunkte'),
        ),
        migrations.AlterField(
            model_name='modul',
            name='organisation',
            field=models.ForeignKey(verbose_name=b'Organisationsform des Moduls', to='modulhandbuch.Organisationsform', help_text='Art der Durchf\xfchrung des Moduls'),
        ),
        migrations.AlterField(
            model_name='studiengang',
            name='startdateien',
            field=models.ManyToManyField(help_text='Welche Tex-Dateien werden f\xfcr dieesen Studiengang ben\xf6tigt?', to='modulhandbuch.TexDateien', verbose_name=b'Benutzte Dateien'),
        ),
        migrations.AlterField(
            model_name='veranstaltungslps',
            name='lp',
            field=models.IntegerField(default=0, help_text='Anzahl LPs f\xfcr diese Lehrveranstaltung in diesem Modul', verbose_name=b'Leistungspunkte'),
        ),
    ]
