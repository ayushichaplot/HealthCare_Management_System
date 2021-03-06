# Generated by Django 3.0.4 on 2020-03-15 11:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pfname', models.CharField(default='Enter First Name', max_length=100)),
                ('plname', models.CharField(default='Enter Last Name', max_length=100)),
                ('paddress', models.CharField(default='Enter Address', max_length=100)),
                ('pphone_number', models.CharField(blank=True, default='Enter number', max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{10,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_start_date', models.DateField()),
                ('visit_end_date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furst.Patient')),
            ],
        ),
    ]
