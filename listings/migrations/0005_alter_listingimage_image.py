# Generated by Django 3.2 on 2021-04-16 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_alter_listingimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingimage',
            name='image',
            field=models.ImageField(upload_to='listings/%Y/%m/%d/'),
        ),
    ]
