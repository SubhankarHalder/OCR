# Generated by Django 2.2.7 on 2019-12-01 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='extracted_date',
            field=models.DateField(blank=True, null=True, verbose_name='OCR Extracted Date'),
        ),
    ]