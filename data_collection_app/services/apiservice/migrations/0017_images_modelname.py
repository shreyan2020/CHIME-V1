# Generated by Django 3.2.4 on 2022-06-18 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiservice', '0016_rename_filename_images_imagename'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='ModelName',
            field=models.CharField(default='default', max_length=100),
            preserve_default=False,
        ),
    ]
