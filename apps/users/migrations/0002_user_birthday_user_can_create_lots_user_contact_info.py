# Generated by Django 4.0.2 on 2022-03-17 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Birthday'),
        ),
        migrations.AddField(
            model_name='user',
            name='can_create_lots',
            field=models.BooleanField(default=True, verbose_name='Can user create lots or not'),
        ),
        migrations.AddField(
            model_name='user',
            name='contact_info',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Links or mobile phone to connect with person'),
        ),
    ]
