# Generated by Django 3.1 on 2021-01-11 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20210110_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=11, upload_to='catimg'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default='', upload_to='proimg'),
        ),
    ]