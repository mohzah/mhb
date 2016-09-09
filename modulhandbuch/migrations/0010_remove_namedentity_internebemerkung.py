# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulhandbuch', '0009_auto_20160909_0116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='namedentity',
            name='interneBemerkung',
        ),
    ]
