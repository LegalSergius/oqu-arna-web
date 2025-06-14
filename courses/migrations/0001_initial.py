# Generated by Django 5.2 on 2025-06-10 14:25

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название курса')),
                ('description', models.TextField(verbose_name='Описание курса')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('participants_count', models.IntegerField(verbose_name='Кол-во участников')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='common.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentored_courses', to=settings.AUTH_USER_MODEL)),
                ('guideline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.content', verbose_name='Методическое указание')),
                ('participants', models.ManyToManyField(related_name='enrolled_courses', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название занятия')),
                ('description', models.TextField(verbose_name='Описание занятия')),
                ('lesson_date', models.DateTimeField(verbose_name='Дата проведения')),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=3600), verbose_name='Продолжительность')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assignments', models.ManyToManyField(blank=True, related_name='lessons', to='common.content', verbose_name='Материалы')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'занятие',
                'verbose_name_plural': 'занятия',
            },
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zoom_id', models.CharField(max_length=64, unique=True, verbose_name='Zoom ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conferences', to='courses.lesson', verbose_name='Занятие')),
            ],
            options={
                'verbose_name': 'конференция',
                'verbose_name_plural': 'конференции',
            },
        ),
        migrations.CreateModel(
            name='LessonStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conference', models.BooleanField(default=False)),
                ('test', models.IntegerField(default=None, null=True)),
                ('task', models.IntegerField(default=None, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_statistic', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='lesson_statics',
            field=models.ManyToManyField(related_name='lesson_statics', to='courses.lessonstatistics'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='courses.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.test'),
        ),
    ]
