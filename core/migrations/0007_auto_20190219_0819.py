# Generated by Django 2.1.6 on 2019-02-19 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_customers_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='data_sheet',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DataSheet'),
        ),
    ]
