# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0006_namedentity_internebemerkung'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namedentity',
            name='interneBemerkung',
            field=models.TextField(help_text='Beliebige Bemerkung, taucht NICHT im\n                                        Modulhandbuch auf. Sinnvoll kann Notiz\n                                        zu intendierten Studieng\xe4ngen sein.', verbose_name='Interne Bemerkungen', blank=True),
        ),
        migrations.AlterField(
            model_name='namedentity',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'nameDe', editable=False),
        ),
    ]
