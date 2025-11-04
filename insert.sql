-- Вставка картинок для категорий в БД

INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\category1.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'category1');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\category2.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'category2');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\category3.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'category3');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\category4.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'category4');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\category5.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'category5');

-- Вставка контента в виде плана обучения по курсу

INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline1');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline1');

INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline2');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline3');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline4');

INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline5');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline6');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline7');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline8');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline9');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline10');

INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline11');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline12');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline13');

INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline14');
INSERT INTO common_content (file, created_at, updated_at, file_name) VALUES ('D:\Projects\INTS\oqu-arna\oqu-arna-web\media\guideline.pdf', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'guideline15');

INSERT INTO common_category (name, created_at, image_id) VALUES ('Английский язык', CURRENT_TIMESTAMP, 1);
INSERT INTO common_category (name, created_at, image_id) VALUES ('Product-менеджмент', CURRENT_TIMESTAMP, 2);
INSERT INTO common_category (name, created_at, image_id) VALUES ('Программирование', CURRENT_TIMESTAMP, 3);
INSERT INTO common_category (name, created_at, image_id) VALUES ('Казахский язык', CURRENT_TIMESTAMP, 4);
INSERT INTO common_category (name, created_at, image_id) VALUES ('Математика', CURRENT_TIMESTAMP, 5);

INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Английский язык (Intermediate)', 'Курс направлен для людей с уровнем Intermediate', '2025-05-13', '2025-05-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 5, 2, 2, 15);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Профессиональный английский язык', 'Курс предназначен для изучения профессиональной специфики английского языка', '2025-11-13', '2025-11-25', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 7, 1, 1, 10);

INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Junior+ Product Manager', 'Курс для продакт-менеджеров уровня Junior+', '2025-05-13', '2025-05-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 8, 1, 1, 15);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Middle+ Product Manager', 'Курс для ', '2025-11-13', '2025-11-25', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 9, 1, 1, 20);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Data Analyst', 'Курс для прокачивания навыков для дата-аналитиков', '2025-11-12', '2025-11-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 10, 1, 1, 22);

INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Junior Java-разработчик', 'Курс для освоения Java-рзработки', '2025-05-13', '2025-05-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 11, 1, 1, 13);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Курс освоения OpenAPI', 'Курс для изучения стандартов OpenAPI', '2025-11-13', '2025-11-25', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 12, 1, 1, 8);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('CQRS-архитектура', 'Курс для применения совеременной архитектуры ради построения гигантских по масштабу проектв', '2025-10-24', '2025-11-31', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 13, 1, 1, 6);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Базы данных', 'Курс для тех, хочет проектировать базы данных', '2025-04-06', '2025-04-27', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 14, 1, 1, 15);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Основы ИИ', 'Курс для изчуения искусственного интеллекта', '2025-11-20', '2025-12-02', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 15, 1, 1, 12);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Веб-хранилища', 'Курс для создания веб-хранилищ', '2025-07-17', '2025-09-21', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 16, 1, 1, 14);

INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Математика начальных классов', 'Курс для школьников младшего звена', '2025-05-13', '2025-05-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 17, 1, 1, 18);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Евклидова геометрия', 'Курс полноценного освоения базовой геометрии', '2025-11-13', '2025-11-25', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 18, 1, 1, 12);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, , category_id, creator_id, participants_count) VALUES ('Высшая математика и мат.анализ', 'Курс продвинутого освоения понятий из вышмата', '2025-05-13', '2025-05-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 19, 1, 1, 16);

INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Полноценный курс прохождения казахского языка', 'Курс для ', '2025-11-13', '2025-11-25', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 20, 1, 1, 13);
INSERT INTO courses_course (name, description, start_date, end_date, created_at, updated_at, guideline_id, category_id, creator_id, participants_count) VALUES ('Казахская литература', 'Курс, раскрывающий творчество казахский писателей и поэтов', '2025-11-12', '2025-11-20', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 21, 1, 1, 15);


INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Beginning', 'Базовые основы изучения английского языка', 60, CURRENT_TIMESTAMP, 1, '2025-05-13 15:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Present Simple', 'Настоящее время глагола', 45, CURRENT_TIMESTAMP, 1, '2025-05-16 15:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Preparing to IELTS', 'Подготовка к экзамену IELTS', 90, CURRENT_TIMESTAMP, 1, '2025-05-19 15:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Английский в деловой среде', 'Термины, применяемые в деловой обстановке', 60, CURRENT_TIMESTAMP, 2, '2025-11-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Техническая документация на английском', 'Составление грамотной документации', 45, CURRENT_TIMESTAMP, 2, '2025-11-19 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Составление CV на английском', 'Подготовка резюме на английском', 90, CURRENT_TIMESTAMP, 2, '2025-11-24 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Понимание жизненного цикла продукта', 'Разбор стадий жизненного цикла продукта и роли менеджера', 60, CURRENT_TIMESTAMP, 4, '2025-05-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Переход состояния от желания заказчика до разработанного требования', 'Как находить и формулировать продуктовые гипотезы.', 45, CURRENT_TIMESTAMP, 4, '2025-05-15 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Важные метрики продукта', 'Введение в продуктовые метрики и принципы оценки успеха', 90, CURRENT_TIMESTAMP, 4, '2025-05-18 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Дорожная карта продукта', 'Как использовать аналитику и исследования для планирования фичей', 60, CURRENT_TIMESTAMP, 5, '2025-11-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Фреймворки приоритизации', 'Применение RICE, ICE, Kano и других методик приоритетов', 45, CURRENT_TIMESTAMP, 5, '2025-11-18 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Важные метрики продукта', 'Введение в продуктовые метрики и принципы оценки успеха', 90, CURRENT_TIMESTAMP, 5, '2025-11-25 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Формирование истории данных', 'Превращение чисел и графиков в понятные бизнес-выводы', 60, CURRENT_TIMESTAMP, 6, '2025-11-12 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Применение Python и SQL для изучения подробностей', 'Использование запросов и скриптов для анализа данных', 45, CURRENT_TIMESTAMP, 6, '2025-11-15 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Продуктовый анализ на практике', 'Как аналитика помогает принимать продуктовые решения и тестировать гипотезы', 90, CURRENT_TIMESTAMP, 6, '2025-11-19 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Основы синтаксиса Java', 'Изучение базового синтаксиса, типов данных и структуры программы', 60, CURRENT_TIMESTAMP, 7,'2025-05-14 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Работа с ООП в Java', 'Понимание принципов инкапсуляции, наследования и полиморфизма', 45, CURRENT_TIMESTAMP, 7, '2025-05-16 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Практика с коллекциями и потоками', 'Применение коллекций, потоков данных и базовых API Java', 90, CURRENT_TIMESTAMP, 7, '2025-05-19 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Принципы CQRS и Event Sourcing', 'Как использовать аналитику и исследования для планирования фичей', 60, CURRENT_TIMESTAMP, 8, '2025-10-24 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Разделение команд и запросов', 'Применение RICE, ICE, Kano и других методик приоритетов', 45, CURRENT_TIMESTAMP, 8, '2025-11-07 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('CQRS в микросервисах', 'Введение в продуктовые метрики и принципы оценки успеха', 90, CURRENT_TIMESTAMP, 8, '2025-11-21 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Реляционная модель и SQL', 'Изучение структуры таблиц, связей и базовых SQL-запросов', 60, CURRENT_TIMESTAMP, 9, '2025-04-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Нормализация данных', 'Оптимизация структуры таблиц для устранения избыточности', 45, CURRENT_TIMESTAMP, 9, '2025-04-18 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Оптимизация запросов', 'Повышение производительности с помощью индексов и анализа планов выполнения', 90, CURRENT_TIMESTAMP, 9, '2025-04-25 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Введение в искусственный интеллект', 'Понимание задач ИИ и его применения в реальных сценариях', 60, CURRENT_TIMESTAMP, 10, '2025-11-21 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Машинное обучение: базовые алгоритмы', 'Изучение принципов классификации, регрессии и кластеризации', 45, CURRENT_TIMESTAMP, 10, '2025-12-01 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Практика с Python и библиотеками ИИ', 'Применение scikit-learn и TensorFlow для решения задач', 90, CURRENT_TIMESTAMP, 10, '2025-12-02 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Архитектура и принципы работы хранилищ', 'Разбор типов веб-хранилищ и принципов распределённого доступа', 60, CURRENT_TIMESTAMP, 11, '2025-07-21 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Работа с объектными и файловыми хранилищами', 'Использование S3, Google Cloud Storage и аналогов', 45, CURRENT_TIMESTAMP, 11, '2025-08-15 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Безопасность и резервное копирование', 'Настройка прав доступа, шифрования и бэкапов данных', 90, CURRENT_TIMESTAMP, 11, '2025-09-14 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Сложение и вычитание в пределах 100', 'Отработка базовых арифметических действий и логики счёта', 60, CURRENT_TIMESTAMP, 12, '2025-05-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Решение текстовых задач', 'Развитие аналитического мышления и умения извлекать данные из условий', 45, CURRENT_TIMESTAMP, 12, '2025-05-18 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Работа с геометрическими фигурами', 'Знакомство с формами, периметром и площадью', 90, CURRENT_TIMESTAMP, 12, '2025-05-20 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Аксиомы и постулаты Евклида', 'Основы построения геометрической системы и взаимосвязь аксиом', 60, CURRENT_TIMESTAMP, 13, '2025-11-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Параллельные прямые и углы', 'Практическое применение свойств параллельных линий и теорем', 45, CURRENT_TIMESTAMP, 13, '2025-11-18 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Построения и доказательства', 'Навыки решения геометрических задач с использованием циркуля и линейки', 90, CURRENT_TIMESTAMP, 13, '2025-11-25 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Пределы и непрерывность функций', 'Освоение базовых понятий анализа и их графическая интерпретация.', 60, CURRENT_TIMESTAMP, 14, '2025-05-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Дифференцирование и интегрирование', 'Применение производных и интегралов к практическим задачам', 45, CURRENT_TIMESTAMP, 14, '2025-05-17 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Ряды и приближения функций', 'Изучение степенных рядов и методов аппроксимации', 90, CURRENT_TIMESTAMP, 14, '2025-05-20 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Основы грамматики и произношения', 'Освоение базовых правил языка и звуковой системы', 60, CURRENT_TIMESTAMP, 15, '2025-11-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Построение предложений и диалогов', 'Развитие разговорной речи и понимания синтаксиса', 45, CURRENT_TIMESTAMP, 15, '2025-11-18 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Чтение и перевод текстов', 'Работа с аутентичными текстами для расширения словарного запас8', 90, CURRENT_TIMESTAMP, 15, '2025-11-25 17:00:00');

INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Фольклор и эпос казахского народа', 'Изучение традиционных форм устного народного творчества', 60, CURRENT_TIMESTAMP, 16, '2025-11-13 14:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Классическая литература XIX века', 'Анализ творчества Абая, Шокана, Ыбрайя и их влияния на культуру', 45, CURRENT_TIMESTAMP, 16, '2025-11-18 16:00:00');
INSERT INTO courses_lesson (name, description, duration, created_at, course_id, lesson_date) VALUES ('Современная казахская проза и поэзия', 'Рассмотрение тем идентичности и модернизации в литературе XX–XXI веков', 90, CURRENT_TIMESTAMP, 16, '2025-11-20 17:00:00');

