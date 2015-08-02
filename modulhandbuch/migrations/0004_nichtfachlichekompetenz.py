# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0003_auto_20150802_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='NichtfachlicheKompetenz',
            fields=[
                ('namedentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='modulhandbuch.NamedEntity')),
                ('beschreibungDe', models.TextField(help_text='Ausf\xfchrliche Beschreibung', verbose_name=b'Beschreibung', blank=True)),
                ('beschreibungEn', models.TextField(help_text=b'Extensive description', verbose_name=b'Beschreibung (engl.)', blank=True)),
            ],
            options={
                'ordering': ['nameDe'],
                'verbose_name': 'Nichtfachliche Kompetenz',
                'verbose_name_plural': 'Nichtfachliche Kompetenzen',
            },
            bases=('modulhandbuch.namedentity',),
        ),
    ]
