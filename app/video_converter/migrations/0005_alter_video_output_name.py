# Generated by Django 4.1.5 on 2023-02-01 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_converter', '0004_video_output_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='output_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]