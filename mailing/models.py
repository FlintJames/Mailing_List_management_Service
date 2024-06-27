from django.db import models

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(**NULLABLE, max_length=200, verbose_name="ФИО")
    comment = models.TextField(**NULLABLE, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.full_name}"


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    text = models.TextField(**NULLABLE, verbose_name="Тело письма")
    #owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.subject}"


class Mailing(models.Model):
    time_sending = models.DateTimeField(verbose_name="Дата и время отправки")
    time_end = models.DateTimeField(verbose_name="Дата и время окончания")
    periodicity = models.CharField(max_length=100, verbose_name="Периодичность")
    status = models.CharField(max_length=100, verbose_name="Статус")
    clients = models.ManyToManyField(Client, verbose_name="Клиент")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name="Сообщение")
    #owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.time_sending}"


class Attempt(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время последней попытки")
    status = models.CharField(max_length=100, verbose_name="Статус попытки")
    answer = models.TextField(**NULLABLE, verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"

    def __str__(self):
        return f"{self.date_time} {self.status}"
