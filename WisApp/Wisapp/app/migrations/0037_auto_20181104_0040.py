# Generated by Django 2.1.2 on 2018-11-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20181104_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='image',
            field=models.FileField(blank=True, default=None, null=True, upload_to='pic_folder/'),
        ),
    ]
