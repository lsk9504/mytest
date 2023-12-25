# Generated by Django 4.2.5 on 2023-10-16 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_input_order_output_order_company_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output_order',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.company'),
        ),
        migrations.AlterField(
            model_name='output_order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='erp.item'),
        ),
    ]
