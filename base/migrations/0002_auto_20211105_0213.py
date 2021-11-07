# Generated by Django 3.2.9 on 2021-11-05 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='teams',
        ),
        migrations.AddField(
            model_name='contribution',
            name='selectionProcess',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.selectionprocess'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='selectionprocess',
            name='candidates',
            field=models.ManyToManyField(through='base.Contribution', to='base.Candidate'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='selectionprocess',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together={('selectionProcess', 'team', 'candidate')},
        ),
    ]