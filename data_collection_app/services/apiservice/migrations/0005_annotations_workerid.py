# Generated by Django 3.1.2 on 2022-05-07 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiservice', '0004_auto_20220507_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotations',
            name='WorkerId',
            field=models.CharField(max_length=700, null=True),
        ),
    ]
