# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewflow', '0003_task_owner_permission_change'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subprocess',
            fields=[
                ('process_ptr', models.OneToOneField(to='viewflow.Process', serialize=False, parent_link=True, auto_created=True, primary_key=True, on_delete=models.CASCADE)),
                ('parent_task', models.ForeignKey(to='viewflow.Task', blank=True, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
    ]
