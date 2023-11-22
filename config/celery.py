from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')#이건 wsgi에도 같은 코드가있는데 해야하나?
app = Celery('config')

# 문자열로 등록은 Celery Worker가 자식 프로세스에게 설정객체가 직렬화가 필요없다고 알리게된다함
# namespace = 'CELERY'는 Celery관련 세팅 파일에서 변수 Prefix가 CELERY_ 라고 알림
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery가 task로 데코레이팅된 일들을 다 알아서 찾는다. 
# 실질적으로 celery 인스턴스가 만들어지는 code 이다!
app.autodiscover_tasks()

# debug 용 출력으로 하단 부분을 넣어준다!
@app.task(bind=True)
def debug_task(self):
   print('Request: {0!r}'.format(self.request))