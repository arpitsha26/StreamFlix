# Generated by Django 5.1.3 on 2024-11-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_remove_customuser_profiles_customuser_profile_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='movies/profile_photos/'),
        ),
    ]
