# Generated by Django 4.2.6 on 2023-12-04 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_projeto_fotosproj'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizacao',
            name='idProjeto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.projeto'),
        ),
    ]
