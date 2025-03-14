from django.db import models
from django.db.models import Q
from django.urls import reverse


class Semd(models.Model):
    semd_status = {
            0: "Зарегистрирован в РЭМД",
            1: "Отказано в регистрации",
            2: "Отправлен на регистрацию",
            3: "Не отправлен на регистрацию в РЭМД",
            4: "Синхронная ошибка при отправке от внешней ИС в РЭМД",
        }
    month_str = {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
    }
    otd         = models.CharField(max_length=255, verbose_name="Отделение", default='')
    vid_semd    = models.CharField(max_length=255, verbose_name="Вид СЭМДа", default='')
    personal    = models.CharField(max_length=255, verbose_name="Сотрудник", default='')
    lid         = models.CharField(max_length=255, verbose_name="Локальный идентификатор документа", blank=True)
    semd_date   = models.DateField(verbose_name='Дата регистрации', blank=True, null=True)
    status      = models.CharField(max_length=255, verbose_name="Статус передачи", default='')
    month       = models.IntegerField(verbose_name='Месяц', blank=True, null=True)
    year        = models.IntegerField(verbose_name='Год', blank=True, null=True)
    reg_error   = models.CharField(max_length=4000, verbose_name="Ошибка", blank=True)

    class Meta:
        verbose_name = "СЭМД"
        verbose_name_plural = "СЭМДы"

    def __str__(self):
        return self.lid

    def get_absolute_url(self):
        return reverse("semd_detail", kwargs={"pk": self.pk})
    
    def get_all_month(self):
        return self.objects.order_by('month').values_list('month', flat=True).distinct()
    
    def get_all_year(self):
        return self.objects.values_list('year', flat=True).distinct()

    def get_semd_by_status(self, month, year):
        data = {}
        data["all"]                         = len(self.objects.filter(month=month, year=year))
        data["all_last_month"]              = 100 - (len(self.objects.filter(month=month-1, year=year))/len(self.objects.filter(month=month, year=year)))*100 if len(self.objects.filter(month=month, year=year)) != 0 else 0
        data["registered"]                  = len(self.objects.filter(status=self.semd_status[0], month=month, year=year))
        data["registered_last_month"]       = 100 - (len(self.objects.filter(status=self.semd_status[0], month=month-1, year=year))/len(self.objects.filter(status=self.semd_status[0], month=month, year=year)))*100 if len(self.objects.filter(status=self.semd_status[0], month=month, year=year)) != 0 else 0
        data["not_registered"]              = len(self.objects.filter(status=self.semd_status[1], month=month, year=year)) 
        data["not_registered_last_month"]   = 100 - (len(self.objects.filter(status=self.semd_status[1], month=month-1, year=year))/len(self.objects.filter(status=self.semd_status[1], month=month, year=year)))*100 if len(self.objects.filter(status=self.semd_status[1], month=month, year=year)) != 0 else 0
        data["sent"]                        = len(self.objects.filter(status=self.semd_status[2], month=month, year=year))
        data["sent_last_month"]             = 100 - (len(self.objects.filter(status=self.semd_status[2], month=month-1, year=year))/len(self.objects.filter(status=self.semd_status[2], month=month, year=year)))*100 if len(self.objects.filter(status=self.semd_status[2], month=month, year=year)) != 0 else 0
        data["not_sent"]                    = len(self.objects.filter(status=self.semd_status[3], month=month, year=year))
        data["not_sent_last_month"]         = 100 - (len(self.objects.filter(status=self.semd_status[3], month=month-1, year=year))/len(self.objects.filter(status=self.semd_status[3], month=month, year=year)))*100 if len(self.objects.filter(status=self.semd_status[3], month=month, year=year)) != 0 else 0
        data["error"]                       = len(self.objects.filter(status=self.semd_status[4], month=month, year=year))
        data["error_last_month"]            = 100 - (len(self.objects.filter(status=self.semd_status[4], month=month-1, year=year))/len(self.objects.filter(status=self.semd_status[4], month=month, year=year)))*100 if len(self.objects.filter(status=self.semd_status[4], month=month, year=year)) != 0 else 0
        return data

    def get_all_semd(self):
        return self.objects.count()

    def get_list_of_otd(self):
        return self.objects.values_list('otd', flat=True).distinct()
    
    def get_semd_by_otd(self, otd, month, year):
        data = {       
                'all_semd': self.objects.filter(otd=otd, month=month, year=year).count(),
                'registered': self.objects.filter(otd=otd, status=self.semd_status[0], month=month, year=year).count(),
                'not_registered': self.objects.filter(otd=otd, status=self.semd_status[1], month=month, year=year).count(),
                'sent': self.objects.filter(otd=otd, status=self.semd_status[2], month=month, year=year).count(),
                'not_sent': self.objects.filter(otd=otd, status=self.semd_status[3], month=month, year=year).count(),
                'error': self.objects.filter(otd=otd, status=5, month=month, year=year).count(),
                
        }
        return data
    def get_error_semd(self, otd, month, year):
        data = {
                'error_module': self.objects.filter(otd=otd, reg_error__contains='Ошибка модуля', month=month, year=year).count(),
                'error_registration': self.objects.filter(otd=otd, reg_error__contains='Документ с идентификатором', month=month, year=year).count(),
                'error_dul': self.objects.filter(otd=otd,reg_error__in=['не соответствует данным ГИП', 'Указанное значение [Имя пациента]', 'Пол пациента в ЭМД' ], month=month, year=year).count(),
                'error_version': self.objects.filter(otd=otd, reg_error__contains='запрещена регистрация новых версий', month=month, year=year).count(),
                'error_sign': self.objects.filter(otd=otd, reg_error__contains='Несоответствие данных подписанта в запросе и в сертификате', month=month, year=year).count(),
                'error_technical': self.objects.filter(otd=otd, reg_error__contains='Справочник OID', month=month, year=year).count(),
                'error_else': self.objects.filter(otd=otd, reg_error__contains='Справочник OID', month=month, year=year).count(),
                'all_register' : self.objects.filter(otd=otd, status=self.semd_status[0], month=month, year=year).count(),
                'all_items' : self.objects.filter(otd=otd, month=month, year=year).count(),
        }
       
        return data
    
