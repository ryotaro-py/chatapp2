# Generated by Django 3.1 on 2022-03-14 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20220314_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
