# Generated by Django 3.1.3 on 2021-11-17 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('showpping', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='voter',
            field=models.ManyToManyField(related_name='voter_review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='Author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
