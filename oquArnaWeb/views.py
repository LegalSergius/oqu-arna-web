from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from users.models import CustomUser
from django.utils.timesince import timesince
from django.utils import timezone
import csv
from django.http import HttpResponse
import io
import os
import zipfile
from courses.models import Course
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

@login_required
def home_view(request):
    return redirect('users:profile')

@staff_member_required
def custom_admin_home_view(request):
    filter_type = request.GET.get("filter", "student")  # default student

    # Фильтруем пользователей
    if filter_type == "teacher":
        users = CustomUser.objects.filter(is_educator=True)
        title = "Обучающий – список"
    elif filter_type == "all":
        users = CustomUser.objects.all()
        title = "Все пользователи – список"
    else:  # student
        users = CustomUser.objects.filter(
            is_educator=False,
            is_staff=False,
            is_superuser=False
        )
        title = "Обучающийся – список"

    # Получаем последние действия пользователей через LogEntry
    log_entries = LogEntry.objects.filter(
        user__in=users
    ).order_by('-action_time')

    # Словарь: user_id -> последнее действие LogEntry
    last_actions = {}
    for log in log_entries:
        if log.user_id not in last_actions:
            last_actions[log.user_id] = log

    # Собираем данные для таблицы
    user_data = []
    for user in users:
        last_action = last_actions.get(user.id)
        action_text = None
        action_type = None
        if last_action:
            # Краткая информация о действии
            action_type = last_action.get_action_flag_display()
            if last_action.action_flag == 1:
                action_text = f"Добавление: {last_action.object_repr}"
            elif last_action.action_flag == 2:
                action_text = f"Изменение: {last_action.object_repr}"
            elif last_action.action_flag == 3:
                action_text = f"Удаление: {last_action.object_repr}"
            else:
                action_text = last_action.change_message
        user_data.append({
            "fio": user.full_name,
            "phone": user.phone_number,
            "email": user.email,
            "action_text": action_text,
            "action_flag": action_type,
        })
    
    courses = Course.objects.all().order_by('-start_date')

    return render(request, "custom_admin/home.html", {
        "users": user_data,
        "filter": filter_type,
        "title": title,
        "courses": courses,
    })

@staff_member_required
def actions_history_view(request):
    log_entries = LogEntry.objects.select_related("user").order_by("-action_time")[:100]  # последние 100
    actions = []
    for log in log_entries:
        if log.action_flag == 1:
            action_flag = "Добавлен"
            action_text = f"Добавление: {log.object_repr}"
        elif log.action_flag == 2:
            action_flag = "Изменён"
            action_text = f"Изменение: {log.object_repr}"
        elif log.action_flag == 3:
            action_flag = "Удалён"
            action_text = f"Удаление: {log.object_repr}"
        else:
            action_flag = "Другое"
            action_text = log.change_message
        when_ago = timesince(log.action_time, timezone.now())
        actions.append({
            "user": log.user,
            "action_flag": action_flag,
            "action_text": action_text,
            "action_time": log.action_time,
            "when_ago": f"{when_ago} назад",
        })
    return render(request, "custom_admin/actions_history.html", {"actions": actions})

def users_report_download(request):
    users = CustomUser.objects.all().order_by('full_name')
    actions = LogEntry.objects.all()

    report_data = []
    for user in users:
        user_actions = actions.filter(user_id=user.id)
        add_count = user_actions.filter(action_flag=1).count()
        change_count = user_actions.filter(action_flag=2).count()
        del_count = user_actions.filter(action_flag=3).count()
        total_actions = add_count + change_count + del_count
        last_action = user_actions.order_by('-action_time').first()
        last_time = last_action.action_time.strftime('%d.%m.%Y %H:%M') if last_action else '-'
        last_action_desc = ''
        if last_action:
            if last_action.action_flag == 1:
                last_action_desc = f'Добавление: {last_action.object_repr}'
            elif last_action.action_flag == 2:
                last_action_desc = f'Изменение: {last_action.object_repr}'
            elif last_action.action_flag == 3:
                last_action_desc = f'Удаление: {last_action.object_repr}'
        role = (
            "Админ" if user.is_superuser or user.is_staff else
            "Обучающий" if user.is_educator else
            "Обучающийся"
        )
        status = "Активен" if user.is_active else "Неактивен"
        reg_date = user.date_joined.strftime('%d.%m.%Y')
        last_login = user.last_login.strftime('%d.%m.%Y %H:%M') if user.last_login else '-'
        inactivity_days = (timezone.now().date() - (last_action.action_time.date() if last_action else user.date_joined.date())).days
        report_data.append([
            user.full_name, user.email, user.phone_number,
            reg_date, status, role,
            add_count, change_count, del_count, total_actions,
            last_login, last_time, last_action_desc, inactivity_days
        ])

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="users_report.csv"'
    response.write('\ufeff')  # BOM

    # Используем ; как разделитель!
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'ФИО', 'E-mail', 'Телефон', 'Дата регистрации', 'Статус', 'Роль',
        'Добавлений', 'Изменений', 'Удалений', 'Всего действий',
        'Последний вход', 'Последнее действие (дата)', 'Описание последнего действия',
        'Дней бездействия'
    ])
    for row in report_data:
        writer.writerow(row)
    return response

@staff_member_required
def download_course_certificates(request, course_id):
    import os  # добавь импорт если его ещё нет
    course = Course.objects.get(pk=course_id)
    org_name = "OquArna"
    background_path = Path("assets/bg.png")
    # logo_path = Path("assets/logo.png")  # если нужен логотип

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        for idx, participant in enumerate(course.participants.all(), start=1):
            pdf_buffer = io.BytesIO()
            pdfmetrics.registerFont(TTFont("DejaVu", str(Path("fonts/DejaVuSans.ttf"))))
            c = canvas.Canvas(pdf_buffer, pagesize=letter)

            # Добавление фона (опционально)
            if background_path.exists():
                bg_img = Image.open(background_path)
                bg_img.thumbnail((letter[0], letter[1]))
                temp_bg_path = "temp_bg_for_reportlab.png"
                bg_img.save(temp_bg_path)
                c.drawImage(temp_bg_path, 0, 0, width=letter[0], height=letter[1])
                os.remove(temp_bg_path)

            x = 2 * inch
            c.setFont("DejaVu", 24)
            c.drawString(x, 10 * inch, "СЕРТИФИКАТ")
            c.setFont("DejaVu", 18)
            c.drawString(x, 9 * inch, org_name)
            c.setFont("DejaVu", 16)
            c.drawString(x, 8 * inch, f"Настоящий сертификат выдан {participant.get_full_name()}")
            c.setFont("DejaVu", 12)
            c.drawString(x, 7.5 * inch, f"за успешное завершение курса «{course.name}».")
            c.drawString(x, 7 * inch, f"с {course.start_date} по {course.end_date}.")
            c.setFont("DejaVu", 10)
            c.drawString(x, 1.5 * inch, "Выдано организацией OquArna")
            c.save()

            pdf_buffer.seek(0)
            # Добавляем порядковый номер после нижнего подчеркивания
            filename = f"certificate_{idx}_{participant.get_full_name().replace(' ', '_')}.pdf"
            zf.writestr(filename, pdf_buffer.read())

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename=certificates_{course_id}.zip'
    return response
