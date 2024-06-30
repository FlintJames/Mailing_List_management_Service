from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(**NULLABLE, max_length=200, verbose_name="ФИО")
    comment = models.TextField(**NULLABLE, verbose_name="Комментарий")

    owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.full_name}"


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    text = models.TextField(**NULLABLE, verbose_name="Тело письма")

    owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    CREATED = "created"
    COMPLETED = "completed"
    STARTED = "started"
    STATUS_VARIANTS = [
        (CREATED, "Создана"),
        (COMPLETED, "Завершена"),
        (STARTED, "Запущена"),
    ]

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    REGULARITY_VARIANTS = [
        (DAILY, "Один раз в день"),
        (WEEKLY, "Один раз в неделю"),
        (MONTHLY, "Один раз в месяц"),
    ]

    time_sending = models.DateTimeField(verbose_name="Дата и время отправки")
    time_end = models.DateTimeField(verbose_name="Дата и время окончания")
    periodicity = models.CharField(max_length=100, choices=REGULARITY_VARIANTS, verbose_name="Периодичность")
    status = models.CharField(max_length=100, choices=STATUS_VARIANTS, verbose_name="Статус")
    clients = models.ManyToManyField(Client, verbose_name="Клиент")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name="Сообщение")

    owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.time_sending}"


class Attempt(models.Model):
    ATTEMPT_SUCCESS = 'SUCCESS'
    ATTEMPT_FAIL = 'FAIL'

    ATTEMPT_CHOICES = [
        (ATTEMPT_SUCCESS, 'Успешно'),
        (ATTEMPT_FAIL, 'Неуспешно'),
    ]

    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время последней попытки")
    status = models.CharField(max_length=100, choices=ATTEMPT_CHOICES, verbose_name="Статус попытки")
    answer = models.TextField(**NULLABLE, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"

    def __str__(self):
        return f"{self.date_time} {self.status}"


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(
        upload_to="mailing/", **NULLABLE, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publication_sign = models.BooleanField(default=True, verbose_name="Публикация")
    number_of_views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    views_counter = models.PositiveIntegerField(verbose_name="Счётчик просмотров", default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
