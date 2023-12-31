# Generated by Django 4.2.5 on 2023-10-18 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0005_item_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_order',
            name='company',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='input_order',
            name='item',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='input_order',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='output_order',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
