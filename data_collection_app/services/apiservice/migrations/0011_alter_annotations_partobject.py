# Generated by Django 3.2.4 on 2022-06-11 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiservice', '0010_alter_annotations_partobject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotations',
            name='PartObject',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
