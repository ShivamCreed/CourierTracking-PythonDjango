# Generated by Django 3.1.6 on 2021-05-27 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0004_auto_20210527_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcelrequest',
            name='request_date',
            field=models.CharField(max_length=50, null=True),
        ),
    ]