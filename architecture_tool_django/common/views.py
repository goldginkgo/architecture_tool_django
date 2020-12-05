import os

from celery.result import AsyncResult
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse

from .tasks import export_data_task


@login_required(login_url="/accounts/login/")
def export(request):
    task = export_data_task.delay()
    return JsonResponse({"task_id": task.id}, status=202)


@login_required(login_url="/accounts/login/")
def download(request, path="test.zip"):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
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
