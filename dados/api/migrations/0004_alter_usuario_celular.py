# Generated by Django 4.2.6 on 2023-11-29 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_organizacao_cpf_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='celular',
            field=models.CharField(),
        ),
    ]
