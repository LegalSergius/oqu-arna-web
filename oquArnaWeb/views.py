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

    return render(request, "custom_admin/home.html", {
        "users": user_data,
        "filter": filter_type,
        "title": title,
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