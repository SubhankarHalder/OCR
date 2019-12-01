# Generated by Django 2.2.7 on 2019-12-01 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('picture', models.ImageField(upload_to='images/')),
                ('actual_date', models.DateField(blank=True, help_text='Enter in YYYY-MM-DD format', null=True, verbose_name='Actual Date of Receipts')),
            ],
        ),
    ]
