# Generated by Django 4.2.6 on 2023-12-01 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_organizacao_docorganizacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizacao',
            name='cpf_cnpj',
            field=models.CharField(unique=True),
        ),
    ]
