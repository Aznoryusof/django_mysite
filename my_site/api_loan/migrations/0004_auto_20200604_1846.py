# Generated by Django 2.2.4 on 2020-06-04 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_loan', '0003_auto_20200604_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approvals',
            old_name='dependents',
            new_name='dependants',
        ),
    ]
