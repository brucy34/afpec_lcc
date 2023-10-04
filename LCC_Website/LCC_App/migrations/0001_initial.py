# Generated by Django 4.2.4 on 2023-09-21 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('code', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=100)),
                ('authors_in', models.CharField(blank=True, max_length=100)),
                ('volume', models.CharField(blank=True, max_length=50)),
                ('year', models.PositiveIntegerField()),
                ('edition', models.CharField(blank=True, max_length=50)),
                ('pages', models.CharField(blank=True, max_length=50)),
                ('nbPage', models.PositiveIntegerField(blank=True)),
                ('pdf', models.FileField(upload_to='pdfs/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('img', models.FileField(upload_to='cat_img/')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('vid', models.FileField(upload_to='videos/')),
                ('img', models.FileField(blank=True, upload_to='videos/img/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Concurrent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('concurrent_code', models.CharField(max_length=25, unique=True)),
                ('lastname', models.CharField(help_text='john', max_length=100)),
                ('firstname', models.CharField(help_text='doe', max_length=100)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('in_university', models.BooleanField(default=False, verbose_name='Are you in University right now?')),
                ('university', models.CharField(blank=True, max_length=100)),
                ('discipline', models.CharField(blank=True, max_length=100)),
                ('level', models.CharField(blank=True, max_length=100)),
                ('profession', models.CharField(blank=True, max_length=100)),
                ('last_login', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=128)),
                ('groups', models.ManyToManyField(blank=True, related_name='concurrents_groups', related_query_name='concurrent', to='auth.group', verbose_name='groups')),
                ('personal_library', models.ManyToManyField(blank=True, related_name='added_books', to='LCC_App.book')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='concurrents_permissions', related_query_name='concurrent', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='LCC_App.category'),
        ),
    ]