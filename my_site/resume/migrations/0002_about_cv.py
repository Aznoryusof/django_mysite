# Generated by Django 3.0.3 on 2020-06-02 13:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='cv',
            field=models.FileField(default=django.utils.timezone.now, upload_to='about'),
            preserve_default=False,
        ),
    ]
