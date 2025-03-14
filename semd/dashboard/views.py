from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from datetime import datetime


from .models import Semd

def index(request, q_month=datetime.now().month, q_year=datetime.now().year):
    try:
        q_month = int(q_month)
        q_year = int(q_year)
        if not (1 <= q_month <= 12):
            raise ValueError
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Некорректные параметры")
    month = Semd.get_all_month(Semd)
    print(month)
    list_month = []
    for i in month:
        list_month.append({i: Semd.month_str[i]})
    year = Semd.get_all_year(Semd)
    status = Semd.get_semd_by_status(Semd, q_month, q_year)
    otd_list = Semd.get_list_of_otd(Semd)
    semd_by_otd = {otd: Semd.get_semd_by_otd(Semd, otd, q_month, q_year) for otd in otd_list}
    error_by_otd = {otd: Semd.get_error_semd(Semd, otd, q_month, q_year) for otd in otd_list}
    
    data = {
        "status": status,
        #"data": semd_by_otd,
        "error": error_by_otd,
        "month": list_month,
        "year": year,
        "current_month": q_month,
        "current_year": q_year
    }
    return render(request, "dashboard/index.html", context=data)

def delete_all_semd(request):
    print("delete_all_semd")
    if request.method == 'GET':
        Semd.objects.all().delete()
        messages.success(request, "Все записи успешно удалены")
        return redirect('dashboard:upload_csv')  # или другая страница
    return redirect('dashboard:upload_csv')

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "dashboard/upload.html", data)
    
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Файл не является CSV')
            return HttpResponseRedirect(reverse("dashboard:upload_csv"))
        
        # Проверка размера файла
        if csv_file.multiple_chunks():
            messages.error(request, "Файл слишком большой. Максимальный размер: 10 МБ.")
            return HttpResponseRedirect(reverse("dashboard:upload_csv"))
        
        # Читаем файл для подсчета строк
        csv_file.seek(0)  # Возвращаем курсор в начало файла
        total_lines = len(csv_file.read().decode("windows-1251").split("\n"))
        processed = 0
        
        # Возвращаем курсор в начало файла
        csv_file.seek(0)
        file_data = csv_file.read().decode("windows-1251")
        lines = file_data.split("\n")
        
        # Обработка строк
        for line in lines:
            fields = line.split(";")
            if fields[0] != '№' and len(fields) == 19:
                is_present = Semd.objects.filter(lid=fields[11]).exists()
                if not is_present:
                    try:
                        if fields[13] == '':
                            correct_format = None
                        else:
                            date_object = datetime.strptime(fields[13], '%d.%m.%Y')
                            correct_format = date_object.date().isoformat() 
                            month_number = date_object.month
                            year_number = date_object.year
                        semd = Semd(
                            otd=fields[2],
                            vid_semd=fields[4],
                            personal=fields[9],
                            lid=fields[11],
                            status=fields[16],
                            reg_error=fields[18],
                            semd_date=correct_format,
                            month=month_number,
                            year=year_number,
                        )
                        print(semd)
                        semd.save()
                        # Обновляем прогресс
                        processed += 1
                        
                    except Exception as e:
                        messages.error(request, "Невозможно загрузить файл. " + repr(e))
                        pass
                else:
                    print('Запись', fields[11], 'с номером уже существует!') 
                # Обновляем страницу с прогрессом
        messages.info(request, f"Обработано записей: {processed}")
        return render(request, "dashboard/upload.html", {
            "processed": processed
        })
                
    except Exception as e:
        messages.error(request, "Невозможно загрузить файл. " + repr(e))
    return HttpResponseRedirect(reverse("dashboard:upload_csv"))