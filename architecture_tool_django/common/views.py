import os
from datetime import datetime

from celery.result import AsyncResult
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse

from .tasks import export_data_task


@login_required(login_url="/accounts/login/")
def export(request):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    export_filename = "export-" + current_time
    task = export_data_task.delay(export_filename)
    return JsonResponse(
        {"task_id": task.id, "export_filename": export_filename}, status=202
    )


@login_required(login_url="/accounts/login/")
def download(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(
                fh.read(), content_type="application/force-download"
            )
            response[
                "Content-Disposition"
            ] = "attachment; filename=" + os.path.basename(file_path)
            return response
    raise Http404


@login_required(login_url="/accounts/login/")
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JsonResponse(result, status=200)
