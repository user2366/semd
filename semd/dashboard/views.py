from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from pandas import read_csv

from .models import Semd

def index(request):
    status = Semd.get_semd_by_status(Semd)
    data = {
        "status": status,
    }
    return render(request, "dashboard/index.html", context=data)

def upload_csv_test(request):
    data = {}
    if "GET" == request.method:
        return render(request, "dashboard/upload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not a CSV')
            return HttpResponseRedirect(reverse("dashboard:upload_csv"))
        #if file is too large - error
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB). " % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("dashboard:upload_csv"))
        #csv = read_csv(csv_file, sep="\n", encoding="windows-1251")
        #print(csv)
        file_data = csv_file.read().decode("windows-1251")
        lines = file_data.split("\n")
        # loop over the lines and save them to db via model
        for line in lines:
            fields = line.split(";")
            if fields[0] != '№':
                is_present = Semd.objects.filter(lid = fields[11]).exists()
                if not(is_present):
                    try:
                        semd = Semd(
                            otd = fields[2],
                            vid_semd = fields[4],
                            personal = fields[9],
                            lid = fields[11],
                            status = fields[16],
                            reg_error = fields[18]
                        )
                        semd.save()
                    except Exception as e:
                        messages.error(request, "Unable to upload file. "+repr(e))
                        pass
                else:
                    print('Запись', fields[11], 'с номером уже существует!')
    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("upload_csv"))

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "dashboard/upload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not a CSV')
            return HttpResponseRedirect(reverse("dashboard:upload_csv"))
        #if file is too large - error
        csv = read_csv(csv_file, skiprows=0, sep=";")
        #print(csv)
        #file_data = csv_file.read().decode("windows-1251")
        #lines = csv.split("\n")
        # loop over the lines and save them to db via model
        '''for line in lines:
            fields = line.split(";")
            if fields[0] != '№':
                is_present = Semd.objects.filter(lid = fields[11]).exists()
                if not(is_present):
                    try:
                        semd = Semd(
                            otd = fields[2],
                            vid_semd = fields[4],
                            personal = fields[9],
                            lid = fields[11],
                            status = fields[16],
                            reg_error = fields[18]
                        )
                        semd.save()
                    except Exception as e:
                        messages.error(request, "Unable to upload file. "+repr(e))
                        pass
                else:
                    print('Запись', fields[11], 'с номером уже существует!')'''
    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("upload_csv")) 