from django.contrib import admin
from .models import ReadingPassage, Difficult, Select, Word

# Register your models here.
admin.site.register(ReadingPassage)
admin.site.register(Difficult)
admin.site.register(Select)
admin.site.register(Word)
