from django.db import models
from django.urls import reverse


class Semd(models.Model):
    otd = models.CharField(max_length=255, verbose_name="Отделение", default='')
    vid_semd = models.CharField(max_length=255, verbose_name="Вид СЭМДа", default='')
    personal = models.CharField(max_length=255, verbose_name="Сотрудник", default='')
    lid = models.CharField(max_length=255, verbose_name="Локальный идентификатор документа", blank=True)
    status = models.CharField(max_length=255, verbose_name="Статус передачи", default='')
    reg_error = models.CharField(max_length=4000, verbose_name="Ошибка", blank=True)

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
