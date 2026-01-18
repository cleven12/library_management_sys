import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'l_m_s.settings')

app = Celery('l_m_s')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
