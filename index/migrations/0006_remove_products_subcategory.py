# Generated by Django 3.1 on 2021-01-11 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20210111_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='subcategory',
        ),
    ]
