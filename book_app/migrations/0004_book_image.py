# Generated by Django 5.1.1 on 2024-10-05 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0003_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1234, upload_to='book_media'),
            preserve_default=False,
        ),
    ]
