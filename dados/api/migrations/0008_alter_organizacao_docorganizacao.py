# Generated by Django 4.2.6 on 2023-12-01 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_organizacao_idorganizador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizacao',
            name='docOrganizacao',
            field=models.BinaryField(null=True),
        ),
    ]