# Django Project Setup

Этот проект использует Django. Ниже приведены инструкции по первичной настройке окружения, созданию проекта и управлению зависимостями с использованием Git.

---

## 📁 Структура проекта

```
my_project/
├── .git/
├── .gitignore
├── manage.py
├── my_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app1/
├── requirements.txt
└── README.md
```

---

## ⚙️ Шаги по созданию проекта

### 1. Создание корневой папки и инициализация Git

```CMD / Powershell
mkdir oquArnaWeb
cd oquArnaWeb

git init
```

---

### 2. Настройка виртуального окружения

```CMD / Powershell
python -m venv .venv
```

- **Linux / macOS:**
  ```bash
  source venv/bin/activate
  ```

- **Windows:**
  ```Powershell
  .\.venv\Scripts\Activate
  ```
  ```CMD
  ".\.venv\Scripts\activate.bat"
  ```
---

### 3. Установка Django

```CMD / Powershell / Bash
pip install django
```

---

### 4. Создание Django-проекта в текущей директории

```bash
django-admin startproject oquArnaWeb .
```

> Обрати внимание на точку в конце команды — это важно, чтобы `manage.py` оказался в корне проекта.

---

### 5. Добавление `.gitignore`

Создай файл `.gitignore` со следующим содержимым:

```
# Python
*.pyc
__pycache__/

# Virtual env
venv/

# Django
db.sqlite3
/static/
media/

# Env
.env
```

---

### 6. Сохранение зависимостей

Выгрузи библиотеки из файла requirements.txt

```CMD / Powershell / Bash
pip install -r requirements.txt
```

---

## 🚀 Запуск проекта

```CMD / Powershell / Bash
python manage.py migrate
python manage.py runserver
```

---

## ✅ Готово!

Теперь ты можешь начать разработку Django-приложений и вести контроль версий с помощью Git.