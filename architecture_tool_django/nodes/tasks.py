import time

from celery import shared_task


@shared_task
def node_post_save_task():
    time.sleep(3)
    print("Node updated!")


@shared_task
def sample_task():
    print("The sample task just ran.")
