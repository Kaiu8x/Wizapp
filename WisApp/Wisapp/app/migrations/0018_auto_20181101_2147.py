# Generated by Django 2.1.2 on 2018-11-02 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20181101_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='event',
            field=models.ForeignKey(blank=True, default=3, on_delete=django.db.models.deletion.CASCADE, to='app.Event'),
        ),
    ]
