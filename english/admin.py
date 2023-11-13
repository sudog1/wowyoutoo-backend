from django.contrib import admin
from .models import ReadingPassage, Difficulty, Select, Word

# Register your models here.
admin.site.register(ReadingPassage)
admin.site.register(Difficulty)
admin.site.register(Select)
admin.site.register(Word)
