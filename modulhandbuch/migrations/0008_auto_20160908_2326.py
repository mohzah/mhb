# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0007_auto_20160817_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lehrveranstaltung',
            name='swsSonst',
        ),
        migrations.RemoveField(
            model_name='lehrveranstaltung',
            name='swsSonstBeschreibungDe',
        ),
        migrations.RemoveField(
            model_name='lehrveranstaltung',
            name='swsSonstBeschreibungEn',
        ),
        migrations.AddField(
            model_name='lehrveranstaltung',
            name='swsPraktikum',
            field=models.IntegerField(default=0, help_text='Anzahl SWS f\xfcr Praktikumteile', verbose_name=b'Praktikum SWS'),
        ),
    ]
