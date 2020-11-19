from celery import shared_task


@shared_task
def sync_to_gitlab_task():
    print("==================test=================================================")
