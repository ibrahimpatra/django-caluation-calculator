# Generated by Django 3.2.6 on 2022-02-01 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcf_form', '0002_constants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry_Beta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('industry', models.CharField(max_length=50, null=True)),
                ('beta', models.FloatField(null=True)),
                ('unlevered_beta', models.FloatField(null=True)),
            ],
        ),
    ]