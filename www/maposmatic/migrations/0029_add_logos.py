# Generated by Django 2.2.12 on 2022-10-23 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maposmatic', '0028_add_indexer'),
    ]

    operations = [
        migrations.AddField(
            model_name='maprenderingjob',
            name='extra_logo',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='maprenderingjob',
            name='logo',
            field=models.CharField(blank=True, default='bundled:osm-logo.svg', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='maprenderingjob',
            name='indexer',
            field=models.CharField(blank=True, default='Street', max_length=256, null=True),
        ),
    ]
