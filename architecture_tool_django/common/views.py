from datetime import datetime

from celery.result import AsyncResult
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import export_data_task, import_data_task


@login_required(login_url="/accounts/login/")
def export(request):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    export_filename = "export-" + current_time
    task = export_data_task.delay(export_filename)
    return JsonResponse(
        {"task_id": task.id, "export_filename": export_filename}, status=202
    )


@login_required(login_url="/accounts/login/")
def download(request, filename):
    filepath = f"export/{filename}"
    if default_storage.exists(filepath):
        content = default_storage.open(filepath).read()
        response = HttpResponse(content, content_type="application/force-download")
        response["Content-Disposition"] = "attachment; filename=" + filename
        return response
    else:
        raise Http404


@login_required(login_url="/accounts/login/")
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
    }
    return JsonResponse(result, status=200)


@csrf_exempt
def import_data(request):
    if request.method == "POST":
        imported_file = request.FILES["file"]
        default_storage.save(f"import/{imported_file}", content=imported_file)
        task = import_data_task.delay(request.FILES["file"].name)
        return JsonResponse({"task_id": task.id}, status=202)
