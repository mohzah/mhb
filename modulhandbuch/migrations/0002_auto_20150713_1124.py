# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modulhandbuch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lehrender',
            name='editors',
            field=models.ManyToManyField(help_text='Wer darf (ausser dem Eigent\xfcmer) diesen Eintrag editieren?', related_name='modulhandbuch_lehrender_editors', verbose_name='Editierrechte', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='namedentity',
            name='editors',
            field=models.ManyToManyField(help_text='Wer darf (ausser dem Eigent\xfcmer) diesen Eintrag editieren?', related_name='modulhandbuch_namedentity_editors', verbose_name='Editierrechte', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
