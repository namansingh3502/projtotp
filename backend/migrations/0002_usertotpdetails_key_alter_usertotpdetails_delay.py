# Generated by Django 4.1.7 on 2023-03-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertotpdetails',
            name='key',
            field=models.CharField(blank=True, max_length=128, verbose_name='Key'),
        ),
        migrations.AlterField(
            model_name='usertotpdetails',
            name='delay',
            field=models.IntegerField(default=1, verbose_name='Time delay'),
            preserve_default=False,
        ),
    ]
