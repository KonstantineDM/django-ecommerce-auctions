# Generated by Django 3.2.5 on 2021-11-09 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210927_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(default='', help_text='Provide a URL-link to Image', max_length=500),
        ),
    ]