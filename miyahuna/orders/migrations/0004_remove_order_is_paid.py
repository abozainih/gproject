# Generated by Django 4.0.3 on 2022-04-06 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_made_by_alter_order_made_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
    ]