# Generated by Django 3.2.13 on 2022-11-05 11:21

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_qnacomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='images/%Y/%M/%D'),
        ),
    ]