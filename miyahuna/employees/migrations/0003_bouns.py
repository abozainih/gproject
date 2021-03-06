# Generated by Django 4.0.4 on 2022-05-26 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_remove_employee_address_1_remove_employee_address_2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bouns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bouns_desc', models.CharField(max_length=255, verbose_name='bouns description')),
                ('bouns_amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='bouns amount')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_bouns', to='employees.employee')),
            ],
        ),
    ]
