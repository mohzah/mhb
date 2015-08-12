# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0005_lehrveranstaltung_nfk'),
    ]

    operations = [
        migrations.AddField(
            model_name='namedentity',
            name='interneBemerkung',
            field=models.TextField(help_text='Beliebige Bemerkung, taucht NICHT im Modulhandbuch auf', verbose_name='Interne Bemerkungen', blank=True),
        ),
    ]
