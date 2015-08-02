# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0004_nichtfachlichekompetenz'),
    ]

    operations = [
        migrations.AddField(
            model_name='lehrveranstaltung',
            name='nfk',
            field=models.ManyToManyField(help_text='Welche nichtfachlichen Kompetenzen werden durch diese Lehrveranstaltung erworben?', to='modulhandbuch.NichtfachlicheKompetenz', verbose_name=b'Nichtfachliche Kompetenz', blank=True),
        ),
    ]
