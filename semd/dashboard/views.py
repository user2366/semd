from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Semd

def index(request):
    lines = [["Blue", 2],["orange", 4],["green", 3]]
    data = {
        "lines": lines
    }
    return render(request, "dashboard/index.html", context=data)

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
        # if file is too large - error
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB). " % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("dashboard:upload_csv"))
        file_data = csv_file.read().decode("windows-1251")
        lines = file_data.split("\n")
        # loop over the lines and save them to db via model
        for line in lines:
            fields = line.split(";")
            try:
                semd = Semd(
                    #eg_error = '',
                    otd = fields[0],
                    vid_semd = fields[1],
                    personal = fields[2],
                    lid = fields[3],
                    status = fields[5],
                    reg_error = fields[6] if len(fields) == 7 else '',
                )
                semd.save()
            except Exception as e:
                messages.error(request, "Unable to upload file. "+repr(e))
                pass
    except Exception as e:
        messages.error(request, "Unable to upload file. "+repr(e))
    return HttpResponseRedirect(reverse("upload_csv"))