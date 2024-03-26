from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class AbstractProfile(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)
    # ФИО
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    middle_name = models.CharField('Отчество', max_length=32)
    birth_date = models.DateField('Дата рождения')
    # Идентификация, верификация
    is_identified = models.DateTimeField('Идентифицирован', null=True)
    is_verified = models.DateTimeField('Верифицирован', null=True)
    is_sign = models.DateTimeField('Личная подпись', null=True, help_text='Получена подпись при личном контакте')
    # Паспорт
    passport_serial = models.CharField('Серия', max_length=4)
    passport_number = models.CharField('Номер', max_length=6)
    passport_birth_place = models.CharField('Место рождения', max_length=256, blank=True)
    passport_issue_name = models.CharField('Кем выдан', max_length=256, blank=True)
    passport_code = models.CharField('Код паспорта', max_length=16)
    passport_date = models.DateField('Дата выдачи', )
    # Прочие документы
    snils = models.CharField('Снилс', max_length=64, null=True)
    # Адрес
    postal_code = models.CharField('Индекс', max_length=16, blank=True)
    state = models.CharField('Регион', max_length=256, blank=True)
    city = models.CharField('Город', max_length=256, blank=True)
    street = models.CharField('Улица', max_length=256, blank=True)
    house = models.CharField('Дом', max_length=8, blank=True)
    apt = models.CharField('Кв', max_length=8, blank=True)
    # Прочее
    income = models.PositiveIntegerField('Доход', blank=True, null=True, help_text='Ежемесячный доход')

    def __str__(self):
        return f'{self.user_id}'

    class Meta:
        abstract = True
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Profile(AbstractProfile):
    class Meta(AbstractProfile.Meta):
        managed = False


class PhoneNumber(models.Model):
    PERSONAL = 'PERSONAL'
    UNKNOWN = 'UNKNOWN'
    TYPE_CHOICES = (
        (PERSONAL, 'Личный'),
        (UNKNOWN, 'Неизвестно'),
    )
    created = models.DateTimeField('Создана', auto_now_add=True)
    updated = models.DateTimeField('Изменен', auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Профиль')
    is_active = models.BooleanField('Активный', default=True, help_text='Звонок идет')
    type = models.CharField('Тип', max_length=16, choices=TYPE_CHOICES)
    phonenumber = PhoneNumberField('Номер телефона', unique=True)
    comment = models.CharField('Комментарий', max_length=512, blank=True)

    def __str__(self):
        return f'{self.phonenumber}'

    class Meta:
        managed = False
        verbose_name = 'Номер телефона'
        verbose_name_plural = 'Номера телефонов'


class HistoryProfile(AbstractProfile):
    user_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        verbose_name = 'История изменений'
        verbose_name_plural = 'История изменений'
