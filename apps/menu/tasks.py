from celery import shared_task




@shared_task
def test_task():
    print("Celery is up and running!")
    return "Success"