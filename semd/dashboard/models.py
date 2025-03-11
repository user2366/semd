from django.db import models
from django.urls import reverse


class Semd(models.Model):
    '''
    id              = models.IntegerField(
                        verbose_name='№', 
                        primary_key=True, 
                        unique=True, 
                        blank=False, 
                        auto_created=True
    )
    mo_name         = models.CharField(
                        verbose_name='Наименование МО',
                        max_length=255,
                        default=''
    )
    deportament     = models.CharField(
                        verbose_name='Структурное подразделение МО',
                        max_length=255,
                        default=''
    )
    oid_deportament = models.CharField(
                        verbose_name='OID Структурного подразделения МО',
                        max_length=255,
                        default=''
    )
    semd            = models.CharField(
                        verbose_name='Вид СЭМД',
                        max_length=255,
                        default=''
    )
    semd_version    = models.CharField(
                        verbose_name='Версия СЭМД',
                        max_length=255,
                        default=''
    )
    fio_pacient     = models.CharField(
                        verbose_name='ФИО пациента',
                        max_length=255,
                        blank=False
    )
    birthdate       = models.DateField()
    Дата рождения;
    СНИЛС;
    Сотрудник, сформировавший СЭМД;
    Номер документа в региональной МИС;
    Локальный идентификатор документа;
    Дата создания СЭМД;
    Дата отправки на регистрацию в РЭМД;
    Дата отказа регистрации в РЭМД;
    Дата и время регистрации в РЭМД;
    Статус передачи СЭМД;
    Статус подписания;
    Ошибки
    '''

    otd         = models.CharField(max_length=255, verbose_name="Отделение", default='')
    vid_semd    = models.CharField(max_length=255, verbose_name="Вид СЭМДа", default='')
    personal    = models.CharField(max_length=255, verbose_name="Сотрудник", default='')
    lid         = models.CharField(max_length=255, verbose_name="Локальный идентификатор документа", blank=True)
    status      = models.CharField(max_length=255, verbose_name="Статус передачи", default='')
    reg_error   = models.CharField(max_length=4000, verbose_name="Ошибка", blank=True)

    class Meta:
        verbose_name = "СЭМД"
        verbose_name_plural = "СЭМДы"

    def __str__(self):
        return self.lid

    def get_absolute_url(self):
        return reverse("semd_detail", kwargs={"pk": self.pk})
    
    def get_semd_by_status(self):
        semd_status = {
            0: "Зарегистрирован в РЭМД",
            1: "Ошибка регистрации в РЭМД",
            2: "Отправлен на регистрацию в РЭМД",
            3: "Подписан. Не отправлен на регистрацию в РЭМД",
            4: "Синхронная ошибка при отправке от внешней ИС в РЭМД",
        }
        status = []
        for i in range(5):
            status.append(len(self.objects.filter(status=semd_status[i])))
        return status
