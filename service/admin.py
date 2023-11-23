from django.contrib import admin
from .models import Announcement,Qna,QnaResponse
# Register your models here.
admin.site.register(Announcement)
admin.site.register(Qna)
admin.site.register(QnaResponse)

