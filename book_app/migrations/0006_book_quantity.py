# Generated by Django 5.1.1 on 2024-10-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0005_logintable_userregister'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(default=1234),
            preserve_default=False,
        ),
    ]
