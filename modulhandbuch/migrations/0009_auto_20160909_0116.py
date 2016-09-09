# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0008_auto_20160908_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lehrveranstaltung',
            name='lernergebnisEn',
        ),
        migrations.RemoveField(
            model_name='lehrveranstaltung',
            name='vorkenntnisseEn',
        ),
        migrations.AddField(
            model_name='lehrveranstaltung',
            name='contact_time_hour',
            field=models.CharField(max_length=70, verbose_name=b'Contact time hour', blank=True),
        ),
        migrations.AddField(
            model_name='lehrveranstaltung',
            name='ects',
            field=models.IntegerField(default=0, verbose_name=b'ECTS'),
        ),
        migrations.AddField(
            model_name='lehrveranstaltung',
            name='lv_nr',
            field=models.CharField(max_length=50, verbose_name=b'LV-NR', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='lernergebnisDe',
            field=models.TextField(help_text=b'Kompetenzorientierte Beschreibung', verbose_name=b'Lernergebnis und Kompetenzen', blank=True),
        ),
        migrations.AlterField(
            model_name='lehrveranstaltung',
            name='vorkenntnisseDe',
            field=models.TextField(help_text=b'Sinnvolle Vorkenntnisse', verbose_name=b'Empfohlene Vorkenntnisse', blank=True),
        ),
    ]
