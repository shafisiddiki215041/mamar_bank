# Generated by Django 5.0.6 on 2024-08-16 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userbankacoount_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_bankrupt', models.BooleanField(default=False)),
            ],
        ),
    ]