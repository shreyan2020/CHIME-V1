from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiservice', '0013_auto_20220616_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='Status',
            field=models.IntegerField(default=0),
        ),
    ]
